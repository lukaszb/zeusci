from __future__ import unicode_literals
from django.test import TestCase
from unittest import mock
from zeusci.zeus.models import Build
from zeusci.zeus.models import Buildset
from zeusci.zeus.models import Command
from zeusci.zeus.models import Project
from zeusci.zeus.models import Status
from zeusci.zeus.builders import BaseBuilder
from zeusci.zeus.builders import PythonBuilder
import datetime
import os
import tempfile


class TestBaseBuilder(TestCase):

    def setUp(self):
        self.builder = BaseBuilder()

    @mock.patch('zeusci.zeus.builders.makedirs')
    def test_build_runs_proper_methods(self, makedirs):
        project = mock.Mock()
        buildset = project.buildsets.create.return_value = mock.Mock()

        self.builder.fetch = mock.Mock()
        self.builder.pre_builds = mock.Mock()
        self.builder.run_builds = mock.Mock()
        self.builder.post_builds = mock.Mock()
        self.builder.clean = mock.Mock()
        # TODO this does NOT check the proper order!
        self.builder.build_project(project)

        project.buildsets.create.assert_called_once_with(branch=None)
        makedirs.assert_called_once_with(buildset.build_dir)

        self.builder.fetch.assert_called_once_with(buildset)
        self.builder.pre_builds.assert_called_once_with(buildset)
        self.builder.run_builds.assert_called_once_with(buildset)
        self.builder.post_builds.assert_called_once_with(buildset)
        self.builder.clean.assert_called_once_with(buildset)

    def test_fetch(self):
        buildset = mock.Mock()
        buildset.build_repo_dir = '/tmp/build/dir'
        buildset.project.repo_url = 'repo/url'
        buildset.branch = None

        cmd = mock.Mock()
        cmd.returncode = 0
        fetcher = mock.Mock()
        fetcher.fetch = mock.Mock(return_value=cmd)
        self.builder.get_fetcher = mock.Mock(return_value=fetcher)

        self.assertTrue(self.builder.fetch(buildset))
        self.builder.get_fetcher.assert_called_once_with(buildset)
        fetcher.fetch.assert_called_once_with('repo/url', '/tmp/build/dir',
            branch=None)

    def test_fetch_respects_branch(self):
        buildset = mock.Mock()
        buildset.build_repo_dir = '/tmp/build/dir'
        buildset.project.repo_url = 'repo/url'
        buildset.branch = 'develop'

        cmd = mock.Mock()
        cmd.returncode = 0
        fetcher = mock.Mock()
        fetcher.fetch = mock.Mock(return_value=cmd)
        self.builder.get_fetcher = mock.Mock(return_value=fetcher)

        self.assertTrue(self.builder.fetch(buildset))
        self.builder.get_fetcher.assert_called_once_with(buildset)
        fetcher.fetch.assert_called_once_with('repo/url', '/tmp/build/dir',
            branch='develop')

    def test_fetch_failed(self):
        # NOTE: The easiest way to test it manually is to make fetcher run
        # command with shell flag set to True (set default True at runcmd)
        buildset = mock.Mock()
        buildset.build_repo_dir = '/tmp/build/dir'
        buildset.project.repo_url = 'repo/url'
        buildset.errors = []
        buildset.branch = None

        cmd = mock.Mock()
        cmd.returncode = 12
        cmd.stdout = b'output'
        cmd.stderr = b'some error'
        fetcher = mock.Mock()
        fetcher.fetch = mock.Mock(return_value=cmd)
        self.builder.get_fetcher = mock.Mock(return_value=fetcher)

        self.assertFalse(self.builder.fetch(buildset))
        self.builder.get_fetcher.assert_called_once_with(buildset)
        fetcher.fetch.assert_called_once_with('repo/url', '/tmp/build/dir',
            branch=None)

        self.assertEqual(buildset.errors, [{
            'reason': 'Fetch failed',
            'stdout': 'output',
            'stderr': 'some error',
            'returncode': 12,
        }])
        buildset.save.assert_called_once_with()

    def test_run_builds(self):
        project = Project.objects.create(name='foobar')
        buildset = Buildset.objects.create(project=project)

        build1 = mock.Mock()
        build2 = mock.Mock()
        builds = [build1, build2]
        self.builder.get_builds = mock.Mock(return_value=builds)
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

    @mock.patch('zeusci.zeus.builders.do_build')
    def test_run_build(self, do_build):
        build = mock.Mock()
        self.builder.run_build(build)
        do_build.delay.assert_called_once_with(build, self.builder.__class__)

    @mock.patch('zeusci.zeus.builders.shutil')
    def test_build(self, shutil):
        project = Project.objects.create(name='foobar')
        build_dir = '/tmp/foobar/builds/'
        buildset = Buildset.objects.create(project=project, build_dir=build_dir)
        build = Build.objects.create(buildset=buildset, number=1)
        self.assertIsNone(build.finished_at)

        build_cmd = mock.Mock()
        self.builder.run_command = mock.Mock()
        self.builder.get_commands = mock.Mock(return_value=[build_cmd])

        self.builder.build(build)

        # check if repo is properly copied
        args = buildset.build_repo_dir, build.build_repo_dir
        shutil.copytree.assert_called_once_with(*args)

        # check if execute_command method was called
        self.builder.run_command.assert_called_once_with(build_cmd)

        # check if build has properly finished_at attribute set
        fetched = Build.objects.get(pk=buildset.pk)
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=0.1)
        self.assertAlmostEqual(fetched.finished_at, now, delta=delta)

    @mock.patch('zeusci.zeus.builders.execute_command')
    def test_run_command(self, execute_command):
        project = Project.objects.create(name='foobar')
        build_dir = '/tmp/foobar/builds/'
        buildset = Buildset.objects.create(project=project, build_dir=build_dir)
        build = Build.objects.create(buildset=buildset, number=1)
        command = Command.objects.create(build=build, number=1, cmd=['make'])

        command.clear_output_cache()

        class DummyCommand(object):
            returncode = 0
            def iter_output(self):
                yield 'line1\n'
                yield 'line2'

        execute_command.return_value = DummyCommand()

        self.builder.run_command(command)

        # check if command has properly set returncode attribute
        self.assertEqual(command.returncode, 0)

        # check if command has properly set status attribute
        self.assertEqual(command.status, Status.PASSED)

        # check if command has properly set finished_at attribute
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=0.1)
        self.assertAlmostEqual(command.finished_at, now, delta=delta)

        # check if command and cache has properly set output
        self.assertEqual(command.command_output.output, 'line1\nline2')
        self.assertEqual(command.output, 'line1\nline2')

        # check if output is overridden
        command.clear_output_cache()
        command.command_output.output = 'foo1bar2'
        command.command_output.save()
        self.builder.run_command(command)
        self.assertEqual(command.command_output.output, 'foo1bar2')
        self.assertEqual(command.output, 'foo1bar2')

    @mock.patch('zeusci.zeus.builders.settings')
    def test_clean(self, settings):
        build = mock.Mock()
        build.build_dir = tempfile.mkdtemp()

        settings.REMOVE_BUILD_DIRS = False
        self.builder.clean(build)
        self.assertTrue(os.path.isdir(build.build_dir))

        settings.REMOVE_BUILD_DIRS = True
        self.builder.clean(build)
        self.assertFalse(os.path.isdir(build.build_dir))


class TestPythonBuildseter(TestCase):

    def setUp(self):
        self.builder = PythonBuilder()

    def test_get_tox_ini_path(self):
        buildset = mock.Mock()
        buildset.build_repo_dir = '/t/r'
        self.assertEqual(self.builder.get_tox_ini_path(buildset), '/t/r/tox.ini')

    def test_get_tox_config(self):
        config = mock.Mock()
        tox_parseconfig = mock.Mock(return_value=config)
        self.builder.get_tox_parseconfig = mock.Mock(return_value=tox_parseconfig)

        buildset = mock.Mock()
        buildset.build_repo_dir = '/tmp/build/dir'

        self.assertEqual(self.builder.get_tox_config(buildset), config)
        expected_args = ['-c', '/tmp/build/dir/tox.ini']
        tox_parseconfig.assert_called_once_with(expected_args)

    @mock.patch.object(Buildset, 'build_dir', '/tmp/foobar/builds/')
    def test_get_builds(self):
        project = Project.objects.create(name='foobar')
        buildset = Buildset.objects.create(project=project)
        build = Build.objects.create(buildset=buildset, number=1, options={
            'toxenv': 'py27'})
        commands = self.builder.get_commands(build)
        self.assertEqual(len(commands), 1)

        command = commands[0]
        command.clear_output_cache()
        self.assertEqual(command.number, 1)
        self.assertEqual(command.title, 'tox')
        cmd = [
            'tox',
            '-c',
            '/tmp/foobar/builds/builds/1/repo/tox.ini',
            '-e', 'py27',
        ]
        self.assertEqual(command.cmd, cmd)
        self.assertEqual(command.output, '')
        self.assertIsNone(command.returncode)

