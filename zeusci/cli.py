from monolith.cli import SimpleExecutionManager
from monolith.cli import SingleLabelCommand
from monolith.cli import BaseCommand
from monolith.cli import arg
import os
import subprocess
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
        #return '/usr/local/bin/python3.3'
        venv_dir = self.get_venv_dir()
        return abspath(venv_dir, 'bin', 'python')

    def get_venv_dir(self):
        ROOT_DIR = get_project_root()
        if ROOT_DIR is None:
            self.error('No zeusci project could be found! Tried to find .zci dir')

        return abspath(ROOT_DIR, 'venv')

    def handle(self, namespace):
        self.info("ROOT_DIR = %r" % get_project_root())
        #self.create_venv(namespace)
        #self.install_setuptools(namespace)
        ##self.install_pip(namespace)
        self.install_packages(namespace)

    def get_builder(self, namespace):
        return venv.EnvBuilder(
            system_site_packages=False,
            clear=namespace.force,
            symlinks=True,
            upgrade=False,
        )

    def create_venv(self, namespace):
        venv_dir = self.get_venv_dir()
        if os.path.isdir(venv_dir) and not namespace.force:
            self.info('Virtualenv exists at %s' % venv_dir)
            return
        self.info("Creating virtualenv at %s" % venv_dir)
        builder = self.get_builder(namespace)
        builder.create(venv_dir)
        self.info('Done')

    def install_setuptools(self, namespace):
        py_exec = self.get_python_exec()
        ez_setup = abspath(get_project_root(), 'config', 'ez_setup.py')
        cmd = ' '.join([py_exec, ez_setup])
        subprocess.call(cmd, shell=True)

    def install_pip(self, namespace):
        py_exec = self.get_python_exec()
        get_pip = abspath(get_project_root(), 'config', 'get-pip.py')
        cmd = ' '.join([py_exec, get_pip])
        subprocess.call(cmd, shell=True)

    def install_packages(self, namespace):
        root_dir = get_project_root()
        venv_dir = self.get_venv_dir()
        requirements_path = abspath(root_dir, 'config', 'requirements.txt')
        pip_exec = abspath(venv_dir, 'bin', 'pip')
        cmd_args = [pip_exec, 'install', '-r', requirements_path]
        cmd = ' '.join(cmd_args)
        subprocess.call(cmd, shell=True)


def main():
    app = SimpleExecutionManager('zci', commands={
        'init': InitCommand,
        'prepare': PrepareCommand,
    })
    app.execute()

