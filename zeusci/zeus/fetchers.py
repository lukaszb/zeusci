from .utils.runcmd import runcmd

class Fetcher(object):
    fetch_cmd = 'curl {url} > {dst}'

    def get_fetch_cmd(self, url, dst, **options):
        return self.fetch_cmd.format(url=url, dst=dst)

    def fetch(self, url, dst, **options):
        cmd = self.get_fetch_cmd(url, dst, **options)
        return self.run_cmd(cmd)

    def run_cmd(self, cmd):
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
        cmd_list = ['{git_bin} clone --depth={depth}']
        if branch:
            cmd_list.append('--branch={branch}')
        cmd_list.append('{url} {dst}')
        git_bin = self.get_git_bin()
        cmd = ' '.join(cmd_list).format(git_bin=git_bin, url=url, dst=dst,
            branch=branch, depth=depth)
        return cmd


