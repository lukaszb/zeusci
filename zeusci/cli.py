from monolith.cli import CommandError
from monolith.cli import SimpleExecutionManager
from monolith.cli import SingleLabelCommand
from monolith.cli import arg
import os
import shutil
import subprocess
import sys
import venv
import zeusci


abspath = lambda *p: os.path.abspath(os.path.join(*p))


CI_TEMPLATE_PATH = abspath(zeusci.__path__[0], 'conf', 'citemplate')


class InitCommand(SingleLabelCommand):

    args = SingleLabelCommand.args + [
        arg('--no-bootstrap', dest='bootstrap', default=True,
            action='store_false', help='Do not bootstrap the project.')
    ]

    def handle_label(self, label, namespace):
        label = label or '.'
        dirname = abspath(label)
        print(" ==> Initializing zeus-ci project at %r" % dirname)
        if os.path.isdir(dirname):
            self.handle_existing_dir(dirname, namespace)
        else:
            self.handle_new_dir(dirname, namespace)
        if namespace.bootstrap:
            self.manager.call_command('bootstrap', dirname)

    def handle_existing_dir(self, dirname, namespace):
        for name in os.listdir(CI_TEMPLATE_PATH):
            src = abspath(CI_TEMPLATE_PATH, name)
            dst = abspath(dirname, name)
            if os.path.exists(dst):
                msg = 'Seems like %r was already initialized. Path %r exists'
                msg = msg % (dirname, dst)
                raise CommandError(message=msg, code=1)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

    def handle_new_dir(self, dirname, namespace):
        shutil.copytree(CI_TEMPLATE_PATH, dirname)


def get_project_root(this=None):
    this = this or abspath(os.path.curdir)
    if os.path.isdir(abspath(this, '.zci')):
        return this
    else:
        parent = abspath(this, os.path.pardir)
        if parent == this:
            return None
        return get_project_root(parent)


class BootstrapCommand(SingleLabelCommand):
    label_default_value = None

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
        if self.root_dir is None:
            self.error('No zeusci project could be found! Tried to find .zci dir')

        return abspath(self.root_dir, 'venv')

    def handle_label(self, label, namespace):
        self.root_dir = get_project_root(label)
        self.info("ROOT_DIR = %r" % self.root_dir)
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
        ez_setup = abspath(self.root_dir, 'config', 'ez_setup.py')
        cmd = [py_exec, '-E', ez_setup]
        subprocess.call(cmd)

    def install_pip(self, namespace):
        easy_install = abspath(self.get_venv_dir(), 'bin', 'easy_install')
        cmd = [easy_install, 'pip']
        subprocess.call(cmd)

    def install_packages(self, namespace):
        self.info('Installing packages ...')
        venv_dir = self.get_venv_dir()
        requirements_path = abspath(self.root_dir, 'config', 'requirements.txt')
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

