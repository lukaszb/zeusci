from monolith.cli import SimpleExecutionManager
from monolith.cli import SingleLabelCommand
from monolith.cli import BaseCommand
import os
import subprocess
import sys


abspath = lambda *p: os.path.abspath(os.path.join(*p))


class InitCommand(SingleLabelCommand):

    def handle_label(self, label, namespace):
        print(" => zci init %r | %s" % (label, namespace))
        print(" => this is just a stub ...")


def get_project_root(this=None):
    this = this or abspath(os.path.curdir)
    if os.path.isdir(abspath(this, '.zci')):
        return this
    else:
        parent = abspath(this, os.path.pardir)
        if parent == this:
            return None
        return get_project_root(parent)


class PrepareCommand(BaseCommand):

    def info(self, msg):
        print("=> %s" % msg)

    def error(self, msg, code=1):
        print("[ERROR] %s" % msg)
        sys.exit(code)

    def get_python_exec(self):
        # TODO: Let user specify this
        return '/usr/local/bin/python3.3'

    def handle(self, namespace):
        ROOT_DIR = get_project_root()
        if ROOT_DIR is None:
            self.error('No zeusci project could be found! Tried to find .zci dir')

        VENV_DIR = abspath(ROOT_DIR, 'venv')
        self.info("ROOT_DIR = %r" % ROOT_DIR)
        self.create_venv(VENV_DIR)

    def create_venv(self, venv_dir):
        self.info("Creating virtualenv at %s" % venv_dir)
        cmd_args = [
            'virtualenv',
            venv_dir,
            '--python',
            self.get_python_exec(),
            '--no-site-packages',
        ]
        cmd = ' '.join(cmd_args)
        self.info("Running command: %r" % cmd)
        subprocess.call(cmd, shell=True)
        self.info('Done')


def main():
    app = SimpleExecutionManager('zci', commands={
        'init': InitCommand,
        'prepare': PrepareCommand,
    })
    app.execute()

