from monolith.cli import SimpleExecutionManager
from monolith.cli import SingleLabelCommand
from monolith.cli import BaseCommand
from monolith.cli import arg
import os
import sys
import venv


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

    args = [
        arg('-f', '--force', default=False, action='store_true'),
    ]

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
        self.create_venv(namespace, VENV_DIR)

    def get_builder(self, namespace):
        return venv.EnvBuilder(
            system_site_packages=False,
            clear=namespace.force,
            symlinks=True,
            upgrade=False,
        )

    def create_venv(self, namespace, venv_dir):
        self.info("Creating virtualenv at %s" % venv_dir)
        builder = self.get_builder(namespace)
        builder.create(venv_dir)
        self.info('Done')


def main():
    app = SimpleExecutionManager('zci', commands={
        'init': InitCommand,
        'prepare': PrepareCommand,
    })
    app.execute()

