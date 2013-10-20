"""
TODO: Consider using gevent-subprocess for non-blocking io commands execution.
"""
from subprocess import Popen
from subprocess import PIPE
from collections import namedtuple


FinishedCommand = namedtuple('FinishedCommand', 'stdout stderr returncode')


def runcmd(cmd, **opts):
    opts.setdefault('stderr', PIPE)
    opts.setdefault('stdout', PIPE)
    opts.setdefault('shell', False)
    popen = Popen(cmd, **opts)
    so, se = popen.communicate()
    return FinishedCommand(stdout=so, stderr=se, returncode=popen.returncode)

