from __future__ import unicode_literals
from django.test import SimpleTestCase
from django.test.utils import override_settings
from zeus.models import Project
from zeus.builders import BaseBuilder
from zeus.builders import PythonBuilder
import mock
import os
import tempfile


class TestBaseBuilder(SimpleTestCase):

    def setUp(self):
        self.builder = BaseBuilder()

    def test_build_method_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.builder.build('project')

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

