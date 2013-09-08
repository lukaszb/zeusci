from __future__ import unicode_literals
from .fetchers import GitFetcher
from .conf import settings
from .utils.general import abspath
from .utils.general import makedirs
from .models import Buildset
from .models import Build
from .models import Command
from .models import Output
from .execution import execute_command
from django.core.cache import cache
import datetime
import shutil


class BaseBuilder(object):

    def info(self, message):
        print(" => %s" % message)

    def get_buildset(self, project):
        """
        Returns :model:`Buildset` instance with properly ``build_dir``
        attribute set. We also ensure that ``build_dir`` directory exists.
        """
        # we're creating buildset first in order to prepare it's number
        buildset = Buildset.objects.create(project=project)
        buildset_no = str(buildset.number)
        # now we can set build_dir
        build_dir = abspath(settings.BUILDS_ROOT, project.name, buildset_no)
        buildset.build_dir = build_dir
        buildset.save()
        makedirs(build_dir)
        return buildset

    def build_project(self, project):
        """
        This method will prepare :model:`Buildset` instance and run following
        methods:

        * :meth:`fetch`
        * :meth:`pre_builds`
        * :meth:`run_builds`
        * :meth:`post_builds`
        * :meth:`clean`
        """
        self.info("Creating buildset for project: %r" % project.name)
        buildset = self.get_buildset(project)

        self.fetch(buildset)
        self.pre_builds(buildset)
        self.run_builds(buildset)
        self.post_builds(buildset)
        self.clean(buildset)

    def get_fetcher(self, buildset):
        return GitFetcher()

    def fetch(self, buildset):
        msg = "Fetching %s -> %s" % (buildset.project.repo_url, buildset.build_repo_dir)
        self.info(msg)
        fetcher = self.get_fetcher(buildset)
        fetcher.fetch(buildset.project.repo_url, buildset.build_repo_dir)

    def pre_builds(self, buildset):
        """
        This method is called *before* any build is run.
        """

    def get_prepared_builds(self, buildset):
        """
        Returns list of :model:`Buildset` instances. They should already be
        flushed to the database and have (alternatively) ``options`` prepared.
        """
        return []

    def get_build_commands(self, buildset):
        return []

    def run_builds(self, buildset):
        results = []
        for build in self.get_prepared_builds(buildset):
            async_result = self.run_build(build)
            results.append(async_result)
        for ar in results:
            ar.wait()

        now = datetime.datetime.now()
        Buildset.objects.filter(pk=buildset.pk).update(finished_at=now)

    def run_build(self, build):
        """
        Returns Celery's ``AsyncResult`` instance (task instance pushed to the
        queue, waiting to be finished).

        This method actually simply runs :meth:`build` as a background job.
        """
        # XXX: Needs to import here as trying to import at the global scope
        # raises errors
        from .tasks import do_build
        return do_build.delay(build, self.__class__)

    def build(self, build):
        build.clear_output_cache()
        shutil.copytree(build.buildset.build_repo_dir, build.build_repo_dir)
        for step in self.get_build_commands(build):
            self.execute_command(build, step)
        Build.objects.filter(pk=build.pk).update(
            finished_at=datetime.datetime.now(),
        )

    def post_builds(self, buildset):
        """
        This method is called *after* all builds are completed.
        """

    def clean(self, build):
        if settings.REMOVE_BUILD_DIRS:
            shutil.rmtree(build.build_dir)


class PythonBuilder(BaseBuilder):

    def get_tox_parseconfig(self):
        from tox._config import parseconfig as tox_parseconfig
        return tox_parseconfig

    def get_tox_config(self, buildset):
        """
        Returns parsed tox config for given ``buildset``.
        """
        tox_ini_path = abspath(buildset.build_repo_dir, 'tox.ini')
        args = ['-c', tox_ini_path]
        tox_parseconfig = self.get_tox_parseconfig()
        return tox_parseconfig(args)

    def get_prepared_builds(self, buildset):
        tox_config = self.get_tox_config(buildset)
        venvs = tox_config.envlist
        return [Build.objects.create(
            buildset=buildset,
            number=number,
            options={'toxenv': env},
        ) for number, env in enumerate(venvs, 1)]

    def get_build_commands(self, build):
        venv = build.options['toxenv']
        tox_ini_path = abspath(build.build_repo_dir, 'tox.ini')
        step = {
            'number': 1,
            'title': 'tox',
            'cmd': ['tox', '-c', tox_ini_path, '-e', venv],
        }
        return [step]

    def execute_command(self, build, step):
        cmd = step['cmd']
        build_command = Command.objects.create(
            build=build,
            number=step['number'],
            title=step['title'],
            cmd=' '.join(cmd),
            started_at=datetime.datetime.now(),
            returncode=None,
        )
        command = execute_command(cmd)
        print "Running command: %r\n\traw: %s" % (' '.join(cmd), str(cmd))
        for chunk in command.iter_output():
            cache.set(build_command.cache_key_output, command.data)
        print "Finished command with code: %s" % command.returncode
        build_command.returncode = command.returncode
        build_command.finished_at = datetime.datetime.now()
        build_command.save()

        try:
            filters = {'command': build_command}
            Output.objects.only('command').get(**filters)
            Output.objects.filter(**filters).update(output=command.data)
            build.clear_output_cache()
        except Output.DoesNotExist:
            output = Output.objects.create(output=command.data)
            build_command.command_output = output
            build_command.save(update_fields=['command_output'])


def build(project):
    print "Building project: %s" % project

    builder = PythonBuilder()
    builder.build_project(project)

