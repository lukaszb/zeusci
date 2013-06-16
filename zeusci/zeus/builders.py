from __future__ import unicode_literals
from .fetchers import GitFetcher
from .conf import settings
from .utils.general import abspath
from .models import Build
from .models import BuildStep
from tox._cmdline import Session
from toxic import Tox
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


class PythonBuilder(BaseBuilder):

    def fetch(self, build):
        msg = "Fetching %s -> %s" % (build.project.repo_url, build.build_dir)
        self.info(msg)
        fetcher = GitFetcher()
        fetcher.fetch(build.project.repo_url, build.build_dir)

    def build(self, project):
        self.info("Building %s" % project.name)
        build = Build.objects.create(project=project)
        dirname = '%s.%s' % (project.name, build.number)
        build_dir = abspath(settings.BUILDS_ROOT, dirname)
        build.build_dir = build_dir
        build.save()

        self.fetch(build)
        self.pre_build_steps(build)
        self.build_steps(build)
        self.clean(build)

    def pre_build_steps(self, build):
        tox_ini_path = abspath(build.build_dir, 'tox.ini')
        self.tox = Tox(tox_ini_path)
        self.tox.sdist()

    def build_steps(self, build):
        results = []
        venvs = self.tox.get_venvs()
        for step_no, env in enumerate(venvs, 1):
            self.info("Build step %d | tox:%s" % (step_no, env))
            from .tasks import build_step
            step = BuildStep.objects.create(
                build=build,
                number=step_no,
                options={'toxenv': env},
            )
            ar = build_step.delay(self, step)
            results.append(ar)
        for ar in results:
            ar.wait()

        now = datetime.datetime.now()
        Build.objects.filter(pk=build.pk).update(finished_at=now)

    def build_step(self, step):
        venv = step.options.get('toxenv')
        self.tox.run_for_venv(venv)
        BuildStep.objects.filter(pk=step.pk).update(
            finished_at=datetime.datetime.now())

    def get_tox_config(self, inipath, venv=None):
        from tox._config import parseconfig
        args = ['-c', abspath(inipath)]
        if venv is not None:
            args += ['-e', venv]
        config = parseconfig(args, 'tox')
        return config


def build(project):
    print "Building project: %s" % project

    builder = PythonBuilder()
    builder.build(project)

