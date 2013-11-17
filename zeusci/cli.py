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
        # TODO: Actually implement this
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


class BootstrapCommand(BaseCommand):

    args = [
        arg('-f', '--force', default=False, action='store_true'),
        arg('--use-local-zeusci', default=None, dest='local_zeusci'),
    ]

    def info(self, msg):
        print("=> %s" % msg)

    def error(self, msg, code=1):
        print("[ERROR] %s" % msg)
        sys.exit(code)

    def get_python_exec(self):
        # TODO: Let user specify this
        venv_dir = self.get_venv_dir()
        return abspath(venv_dir, 'bin', 'python')


    def get_venv_dir(self):
        ROOT_DIR = get_project_root()
        if ROOT_DIR is None:
            self.error('No zeusci project could be found! Tried to find .zci dir')

        return abspath(ROOT_DIR, 'venv')

    def handle(self, namespace):
        self.info("ROOT_DIR = %r" % get_project_root())
        self.create_venv(namespace)
        self.install_setuptools(namespace)
        self.install_pip(namespace)
        self.install_packages(namespace)

    def get_builder(self, namespace):
        return venv.EnvBuilder(
            # XXX: We use global site-pacckages as we don't want to re-install
            # zeusci at virtualenv; if there is an obvious way to do this, we
            # will NOT use global site-packages
            system_site_packages=True,
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
        # TODO: put setuptools source distribution at some temporary path
        py_exec = self.get_python_exec()
        ez_setup = abspath(get_project_root(), 'config', 'ez_setup.py')
        cmd = [py_exec, '-E', ez_setup]
        subprocess.call(cmd)

    def install_pip(self, namespace):
        easy_install = abspath(self.get_venv_dir(), 'bin', 'easy_install')
        cmd = [easy_install, 'pip']
        subprocess.call(cmd)

    def install_packages(self, namespace):
        self.info('Installing packages ...')
        root_dir = get_project_root()
        venv_dir = self.get_venv_dir()
        requirements_path = abspath(root_dir, 'config', 'requirements.txt')
        pip_exec = abspath(venv_dir, 'bin', 'pip')
        cmd = [pip_exec, 'install', '-r', requirements_path]
        subprocess.call(cmd)
        self.info('Done')


def main():
    app = SimpleExecutionManager('zci', commands={
        'init': InitCommand,
        'bootstrap': BootstrapCommand,
    })
    app.execute()

