from __future__ import unicode_literals
from .fetchers import GitFetcher
from .conf import settings
from .utils.general import abspath
from .models import Build


class BaseBuilder(object):

    def info(self, message):
        print(" => %s" % message)

    def build(self, project):
        raise NotImplementedError


class PythonBuilder(BaseBuilder):

    #def __init__(self, build_dir):
        #self.build_dir = abspath(settings.BUILDS_ROOT, 

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

        # Clean after build
        #import shutil
        #shutil.rmtree(build_dir)


def build(project):
    print "Building project: %s" % project

    builder = PythonBuilder()
    builder.build(project)

