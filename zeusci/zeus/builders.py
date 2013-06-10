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

    def build(self, project):
        self.info("Building %s" % project.name)
        build = Build.objects.create(project=project)
        #runcmd('git clone %s' % project.repo_url)
        dirname = '%s.%s' % (project.name, build.number)
        build_dir = abspath(settings.BUILDS_ROOT, dirname)
        build.build_dir = build_dir
        build.save()

        self.info("Fetching %s -> %s" % (project.repo_url, build_dir))
        fetcher = GitFetcher()
        fetcher.fetch(project.repo_url, build_dir)

        tox_ini_path = abspath(build_dir, 'tox.ini')
        from tox._cmdline import Session
        config = self.get_tox_config(tox_ini_path)
        for step_no, env in enumerate(config.envlist, 1):
            self.info(" TOX | %s" % env)
            step = BuildStep.objects.create(build=build, number=step_no)
            step_config = self.get_tox_config(tox_ini_path, env)
            Session(step_config).runcommand()
            step.finished_at = datetime.datetime.now()
            step.save()

        build.finished_at = datetime.datetime.now()
        build.save()
        # Clean after build
        #import shutil
        #shutil.rmtree(build_dir)

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

