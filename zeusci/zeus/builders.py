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

    def build(self, project):
        raise NotImplementedError

    def clean(self, build):
        if settings.REMOVE_BUILD_DIRS:
            shutil.rmtree(build.build_dir)


def get_tox_config(tox_ini_path):
    from tox._config import parseconfig
    args = ['-c', tox_ini_path]
    return parseconfig(args)


class PythonBuilder(BaseBuilder):

    def fetch(self, buildset):
        msg = "Fetching %s -> %s" % (buildset.project.repo_url, buildset.build_repo_dir)
        self.info(msg)
        fetcher = GitFetcher()
        fetcher.fetch(buildset.project.repo_url, buildset.build_repo_dir)

    def build_project(self, project):
        self.info("Buildseting %s" % project.name)
        buildset = Buildset.objects.create(project=project)
        buildset_no = str(buildset.number)
        build_dir = abspath(settings.BUILDS_ROOT, project.name, buildset_no)
        makedirs(build_dir)

        buildset.build_dir = build_dir
        buildset.save()

        self.fetch(buildset)
        self.pre_builds(buildset)
        self.builds(buildset)
        self.clean(buildset)

    def pre_builds(self, buildset):
        self.tox_ini_path = abspath(buildset.build_repo_dir, 'tox.ini')

    def builds(self, buildset):
        results = []
        tox_config = get_tox_config(self.tox_ini_path)
        venvs = tox_config.envlist
        total = len(venvs)
        for build_no, env in enumerate(venvs, 1):
            self.info("Buildset step %d / %d | tox:%s" % (build_no, total, env))
            from .tasks import do_build
            build = Build.objects.create(
                buildset=buildset,
                number=build_no,
                options={'toxenv': env},
            )
            build.clear_output_cache()
            shutil.copytree(buildset.build_repo_dir, build.build_repo_dir)
            ar = do_build.delay(build, self.__class__)
            results.append(ar)
        for ar in results:
            ar.wait()

        now = datetime.datetime.now()
        Buildset.objects.filter(pk=buildset.pk).update(finished_at=now)

    def build(self, build):
        for step in self.get_build_commands(build):
            self.execute_command(build, step)
        Build.objects.filter(pk=build.pk).update(
            finished_at=datetime.datetime.now(),
        )

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
        )
        command = execute_command(cmd)
        print "Running command: %r\n\traw: %s" % (' '.join(cmd), str(cmd))
        for chunk in command.iter_output():
            cache.set(build_command.cache_key_output, command.data)
        print "Finished command with code: %s" % command.returncode
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

