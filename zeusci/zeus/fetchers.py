from .exceptions import FetcherError
from .utils.runcmd import runcmd


class Fetcher(object):
    fetch_cmd = 'curl {url} > {dst}'

    def get_fetch_cmd(self, url, dst, **options):
        return self.fetch_cmd.format(url=url, dst=dst)

    def fetch(self, url, dst, **options):
        cmd = self.get_fetch_cmd(url, dst, **options)
        return self.run_cmd(cmd)

    def run_cmd(self, cmd):
        if not isinstance(cmd, list):
            raise FetcherError('cmd must be a list but %r is a %s' %
                (cmd, type(cmd)))
        return runcmd(cmd)


class DummyFetcher(Fetcher):
    def fetch(self, url, dst, **options):
        return None


class GitFetcher(Fetcher):
    git_bin = 'git'

    def get_git_bin(self):
        return self.git_bin

    def get_fetch_cmd(self, url, dst, **options):
        branch = options.get('branch', None)
        depth = options.get('depth', 1)
        cmd = [self.get_git_bin(), 'clone', '--depth=%s' % depth]
        if branch:
            cmd.append('--branch=%s' % branch)
        cmd.extend([url, dst])
        return cmd


