from __future__ import unicode_literals
from django.test import SimpleTestCase
from zeus.models import Build
from zeus.models import Buildset
from zeus.models import Project
from zeus.builders import BaseBuilder
from zeus.builders import PythonBuilder
import datetime
import mock
import os
import tempfile


class TestBaseBuilder(SimpleTestCase):

    def setUp(self):
        self.builder = BaseBuilder()

    @mock.patch('zeus.builders.makedirs')
    @mock.patch('zeus.builders.settings')
    def test_get_buildset(self, settings, makedirs):
        settings.BUILDS_ROOT = '/tmp/ci/builds'
        project = Project.objects.create(name='foobar-project')
        buildset = self.builder.get_buildset(project)

        self.assertEqual(buildset.build_dir, '/tmp/ci/builds/foobar-project/1')
        makedirs.assert_called_once_with(buildset.build_dir)

    def test_build_runs_proper_methods(self):
        project = mock.Mock()
        buildset = mock.Mock()
        self.builder.get_buildset = mock.Mock(return_value=buildset)
        self.builder.fetch = mock.Mock()
        self.builder.pre_builds = mock.Mock()
        self.builder.run_builds = mock.Mock()
        self.builder.post_builds = mock.Mock()
        self.builder.clean = mock.Mock()
        # TODO this does NOT check the proper order!
        self.builder.build_project(project)

        self.builder.get_buildset.assert_called_once_with(project)
        self.builder.fetch.assert_called_once_with(buildset)
        self.builder.pre_builds.assert_called_once_with(buildset)
        self.builder.run_builds.assert_called_once_with(buildset)
        self.builder.post_builds.assert_called_once_with(buildset)
        self.builder.clean.assert_called_once_with(buildset)

    def test_fetch(self):
        buildset = mock.Mock()
        buildset.build_repo_dir = '/tmp/build/dir'
        buildset.project.repo_url = 'repo/url'

        fetcher = mock.Mock()
        self.builder.get_fetcher = mock.Mock(return_value=fetcher)

        self.builder.fetch(buildset)
        self.builder.get_fetcher.assert_called_once_with(buildset)
        fetcher.fetch.assert_called_once_with('repo/url', '/tmp/build/dir')

    def test_run_builds(self):
        project = Project.objects.create(name='foobar')
        buildset = Buildset.objects.create(project=project)

        build1 = mock.Mock()
        build2 = mock.Mock()
        builds = [build1, build2]
        self.builder.get_prepared_builds = mock.Mock(return_value=builds)
        async_result = mock.Mock()
        self.builder.run_build = mock.Mock(return_value=async_result)
        self.builder.run_builds(buildset)

        # check if run_build was called twice with proper parameters
        calls = [mock.call(build1), mock.call(build2)]
        self.assertEqual(self.builder.run_build.call_args_list, calls)

        # check if async results' wait method were called
        calls = [mock.call(), mock.call()]
        self.assertEqual(async_result.wait.call_args_list, calls)

        # check if buildset has properly finished_at attribute set
        buildset = Buildset.objects.get(pk=buildset.pk)
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=0.1)
        self.assertAlmostEqual(buildset.finished_at, now, delta=delta)

    @mock.patch('zeus.builders.do_build')
    def test_run_build(self, do_build):
        build = mock.Mock()
        self.builder.run_build(build)
        do_build.delay.assert_called_once_with(build, self.builder.__class__)

    @mock.patch('zeus.builders.shutil')
    def test_build(self, shutil):
        project = Project.objects.create(name='foobar')
        build_dir = '/tmp/foobar/builds/'
        buildset = Buildset.objects.create(project=project, build_dir=build_dir)
        build = Build.objects.create(buildset=buildset, number=1)
        self.assertIsNone(build.finished_at)

        build_cmd = mock.Mock()
        self.builder.execute_command = mock.Mock()
        self.builder.get_build_commands = mock.Mock(return_value=[build_cmd])

        self.builder.build(build)

        # check if repo is properly copied
        args = buildset.build_repo_dir, build.build_repo_dir
        shutil.copytree.assert_called_once_with(*args)

        # check if execute_command method was called
        self.builder.execute_command.assert_called_once_with(build, build_cmd)

        # check if build has properly finished_at attribute set
        fetched = Build.objects.get(pk=buildset.pk)
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=0.1)
        self.assertAlmostEqual(fetched.finished_at, now, delta=delta)

    @mock.patch('zeus.builders.settings')
    def test_clean(self, settings):
        build = mock.Mock()
        build.build_dir = tempfile.mkdtemp()

        settings.REMOVE_BUILD_DIRS = False
        self.builder.clean(build)
        self.assertTrue(os.path.isdir(build.build_dir))

        settings.REMOVE_BUILD_DIRS = True
        self.builder.clean(build)
        self.assertFalse(os.path.isdir(build.build_dir))

    # TODO: test execute_command method


class TestPythonBuildseter(SimpleTestCase):

    def setUp(self):
        self.builder = PythonBuilder()

    def test_get_tox_config(self):
        config = mock.Mock()
        tox_parseconfig = mock.Mock(return_value=config)
        self.builder.get_tox_parseconfig = mock.Mock(return_value=tox_parseconfig)

        buildset = mock.Mock()
        buildset.build_repo_dir = '/tmp/build/dir'

        self.assertEqual(self.builder.get_tox_config(buildset), config)
        expected_args = ['-c', '/tmp/build/dir/tox.ini']
        tox_parseconfig.assert_called_once_with(expected_args)

    def test_build(self):
        pass

