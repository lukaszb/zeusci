from __future__ import unicode_literals
from .fetchers import GitFetcher
from .conf import settings
from .utils.general import abspath
from .models import Build
from .models import BuildStep
import datetime


class BaseBuilder(object):

    def info(self, message):
        print(" => %s" % message)

    def build(self, project):
        raise NotImplementedError


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
        self.build_steps(build)
        #self.clean(build)

    def build_steps(self, build):
        tox_ini_path = abspath(build.build_dir, 'tox.ini')
        config = self.get_tox_config(tox_ini_path)
        results = []
        for step_no, env in enumerate(config.envlist, 1):
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
        from tox._cmdline import Session
        inipath = abspath(step.build.build_dir, 'tox.ini')
        env = step.options.get('toxenv')
        config = self.get_tox_config(inipath, env)
        Session(config).runcommand()
        BuildStep.objects.filter(pk=step.pk).update(
            finished_at=datetime.datetime.now())

    def get_tox_config(self, inipath, venv=None):
        from tox._config import parseconfig
        args = ['-c', abspath(inipath)]
        if venv is not None:
            args += ['-e', venv]
        config = parseconfig(args, 'tox')
        return config

    def clean(self, build):
        import shutil
        shutil.rmtree(build.build_dir)


def build(project):
    print "Building project: %s" % project

    builder = PythonBuilder()
    builder.build(project)

