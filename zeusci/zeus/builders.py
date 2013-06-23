from __future__ import unicode_literals
from .fetchers import GitFetcher
from .conf import settings
from .utils.general import abspath
from .utils.general import makedirs
from .models import Build
from .models import BuildStep
import datetime
import os
import shutil
import subprocess


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
    return parseconfig(tox_ini_path)


class PythonBuilder(BaseBuilder):

    def fetch(self, build):
        msg = "Fetching %s -> %s" % (build.project.repo_url, build.build_repo_dir)
        self.info(msg)
        fetcher = GitFetcher()
        fetcher.fetch(build.project.repo_url, build.build_repo_dir)

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
        self.tox_ini_path = abspath(build.build_dir, 'tox.ini')

    def build_steps(self, build):
        results = []
        tox_config = get_tox_config(self.tox_ini_path)
        venvs = tox_config.envlist
        for step_no, env in enumerate(venvs, 1):
            self.info("Build step %d | tox:%s" % (step_no, env))
            from .tasks import build_step
            output_path = os.path.join(settings.BUILDS_OUTPUT_DIR, build.project.name, str(build.number), str(step_no))
            makedirs(os.path.dirname(output_path))
            step = BuildStep.objects.create(
                build=build,
                number=step_no,
                options={'toxenv': env},
                output_path=output_path,
            )
            shutil.copytree(build.build_repo_dir, step.build_step_repo_dir)
            ar = build_step.delay(self, step)
            results.append(ar)
        for ar in results:
            ar.wait()

        now = datetime.datetime.now()
        Build.objects.filter(pk=build.pk).update(finished_at=now)

    def build_step(self, step):
        venv = step.options['toxenv']
        with open(step.output_path, 'w') as stream:
            tox_ini_path = abspath(step.build_step_repo_dir, 'tox.ini')
            cmd = ['tox', '-c', tox_ini_path, '-e', venv]
            print "Running command: %s" % str(cmd)
            popen = subprocess.Popen(cmd, stdout=stream, stderr=stream)
            popen.communicate()
            print "Finished step with code: %s" % popen.returncode
            print "Output is at: %s" % step.output_path
        BuildStep.objects.filter(pk=step.pk).update(
            finished_at=datetime.datetime.now(),
            returncode=popen.returncode,
        )


def build(project):
    print "Building project: %s" % project

    builder = PythonBuilder()
    builder.build(project)

