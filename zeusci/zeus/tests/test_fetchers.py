from django.test import SimpleTestCase
from unittest import mock
from zeusci.zeus.exceptions import FetcherError
from zeusci.zeus.fetchers import Fetcher
from zeusci.zeus.fetchers import GitFetcher


class TestFetcher(SimpleTestCase):

    def setUp(self):
        self.fetcher = Fetcher()

    @mock.patch('zeusci.zeus.fetchers.runcmd')
    def test_run_cmd(self, runcmd):
        finished_command = mock.Mock()
        runcmd.return_value = finished_command
        self.assertEqual(self.fetcher.run_cmd(['mycmd']), finished_command)
        runcmd.assert_called_once_with(['mycmd'])

    @mock.patch('zeusci.zeus.fetchers.runcmd')
    def test_run_cmd_accepts_only_list_as_cmd(self, runcmd):
        finished_command = mock.Mock()
        runcmd.return_value = finished_command
        with self.assertRaises(FetcherError):
            self.fetcher.run_cmd('my cmd')

    def test_get_fetch_cmd(self):
        self.fetcher.fetch_cmd = 'foo {url} | bar {dst}'
        cmd = self.fetcher.get_fetch_cmd(url='URL', dst='DST')
        self.assertEqual(cmd, 'foo URL | bar DST')

    def test_fetch(self):
        self.fetcher.get_fetch_cmd = mock.Mock(return_value=['cmd'])
        finished_command = mock.Mock()
        self.fetcher.run_cmd = mock.Mock(return_value=finished_command)

        cmd = self.fetcher.fetch(url='URL', dst='DST')
        self.assertEqual(cmd, finished_command)
        self.fetcher.get_fetch_cmd.assert_called_once_with('URL', 'DST')
        self.fetcher.run_cmd.assert_called_once_with(['cmd'])


class TestGitFetcher(SimpleTestCase):

    def setUp(self):
        self.fetcher = GitFetcher()

    def test_get_git_bin(self):
        self.assertEqual(self.fetcher.get_git_bin(), 'git')

    def test_get_fetch_cmd(self):
        self.fetcher.get_git_bin = mock.Mock(return_value='git')
        cmd = self.fetcher.get_fetch_cmd('http://xmp.com/foo', '/tmp/foo')
        self.assertEqual(cmd, [
            'git',
            'clone',
            '--depth=1',
            'http://xmp.com/foo',
            '/tmp/foo',
        ])

    def test_get_fetch_cmd_respects_depth(self):
        self.fetcher.get_git_bin = mock.Mock(return_value='git')
        cmd = self.fetcher.get_fetch_cmd('http://xmp.com/foo', '/tmp/foo',
            depth=3)
        self.assertEqual(cmd, [
            'git',
            'clone',
            '--depth=3',
            'http://xmp.com/foo',
            '/tmp/foo',
        ])

    def test_get_fetch_cmd_respects_branch(self):
        self.fetcher.get_git_bin = mock.Mock(return_value='git')
        cmd = self.fetcher.get_fetch_cmd('http://xmp.com/foo', '/tmp/foo',
            branch='devel')
        self.assertEqual(cmd, [
            'git',
            'clone',
            '--depth=1',
            '--branch=devel',
            'http://xmp.com/foo',
            '/tmp/foo',
        ])

