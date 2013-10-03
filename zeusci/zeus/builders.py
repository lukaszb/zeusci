from __future__ import unicode_literals
from .fetchers import GitFetcher
from .conf import settings
from .utils.general import abspath
from .utils.general import makedirs
from .models import Buildset
from .models import Build
from .models import Command
from .models import Output
from .models import Status
from .execution import execute_command
from .tasks import do_build
from django.core.cache import cache
import datetime
import os
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

    def get_builds(self, buildset):
        """
        Returns list of :model:`Buildset` instances. They should already be
        flushed to the database and have (alternatively) ``options`` prepared.
        """
        return []

    def run_builds(self, buildset):
        results = []
        for build in self.get_builds(buildset):
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
        return do_build.delay(build, self.__class__)

    def build(self, build):
        if os.path.isdir(build.build_repo_dir):
            shutil.rmtree(build.build_repo_dir)
        shutil.copytree(build.buildset.build_repo_dir, build.build_repo_dir)
        for command in self.get_commands(build):
            self.run_command(command)
        Build.objects.filter(pk=build.pk).update(
            finished_at=datetime.datetime.now(),
        )

    def get_commands(self, build):
        """
        Returns list of :model:`Command` instances. They should already be
        flushed to the database.

        :param build: An :model:`Build` instance.
        """
        return []

    def run_command(self, command):
        """
        Runs given ``command``.
        """
        Command.objects.filter(pk=command.pk).update(status=Status.RUNNING)
        executed_cmd = execute_command(command.cmd)
        print "Running command: %r\n\traw: %s" % (command.get_cmd_string(),
                                                  str(command.cmd))
        data = ''
        for chunk in executed_cmd.iter_output():
            data += chunk
            cache.set(command.cache_key_output, data)
        print "Finished command with code: %s" % executed_cmd.returncode
        command.returncode = executed_cmd.returncode
        if executed_cmd.returncode == 0:
            command.status = Status.PASSED
        else:
            command.status = Status.FAILED
        command.finished_at = datetime.datetime.now()
        command.save()

        try:
            command.clear_output_cache()
            filters = {'command': command}
            Output.objects.only('command').get(**filters)
            Output.objects.filter(**filters).update(output=data)
        except Output.DoesNotExist:
            output = Output.objects.create(output=data)
            command.command_output = output
            command.save()

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

    def get_tox_ini_path(self, buildset):
        return abspath(buildset.build_repo_dir, 'tox.ini')

    def get_tox_config(self, buildset):
        """
        Returns parsed tox config for given ``buildset``.
        """
        tox_ini_path = self.get_tox_ini_path(buildset)
        args = ['-c', tox_ini_path]
        tox_parseconfig = self.get_tox_parseconfig()
        return tox_parseconfig(args)

    def get_builds(self, buildset):
        tox_config = self.get_tox_config(buildset)
        venvs = tox_config.envlist
        return [Build.objects.create(
            buildset=buildset,
            number=number,
            options={'toxenv': env},
        ) for number, env in enumerate(venvs, 1)]

    def get_commands(self, build):
        venv = build.options['toxenv']
        tox_ini_path = abspath(build.build_repo_dir, 'tox.ini')
        command = Command.objects.create(
            build=build,
            number=1,
            title='tox',
            cmd=['tox', '-c', tox_ini_path, '-e', venv],
            started_at=datetime.datetime.now(),
            returncode=None,
            status=Status.PENDING,
        )
        return [command]

