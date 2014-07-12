import click
import os
import shutil
import subprocess
import sys
import venv
import zeusci


abspath = lambda *p: os.path.abspath(os.path.join(*p))


CI_TEMPLATE_PATH = abspath(zeusci.__path__[0], 'conf', 'citemplate')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


DirPath = click.types.Path(file_okay=False, writable=True)

def copy(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy(src, dst)


def init_existing_dir(project_path):
    for name in os.listdir(CI_TEMPLATE_PATH):
        src = abspath(CI_TEMPLATE_PATH, name)
        dst = abspath(project_path, name)
        if os.path.exists(dst):
            msg = 'Seems like %r was already initialized. Path %r exists'
            msg = msg % (project_path, dst)
            raise click.UsageError(message=msg)
        copy(src, dst)


def init_new_dir(project_path):
    # TODO: Randomize SECRET_KEY at settings.py
    copy(CI_TEMPLATE_PATH, project_path)


@click.command(name='init')
@click.argument('project_path', type=DirPath, default='.')
@click.option('--bootstrap/--no-bootstrap', default=True,
              help='Do not bootstrap the project.')
@click.pass_context
def init_cmd(ctx, project_path, bootstrap):
    click.echo(" ==> Initializing zeus-ci project at %r" % project_path)

    if os.path.isdir(project_path):
        init_existing_dir(project_path)
    else:
        init_new_dir(project_path)
    if bootstrap:
        ctx.invoke(bootstrap_cmd, project_path=project_path, force=False)


def get_project_root(this=None):
    this = this or abspath(os.path.curdir)
    if os.path.isdir(abspath(this, '.zci')):
        return this
    else:
        parent = abspath(this, os.path.pardir)
        if parent == this:
            return None
        return get_project_root(parent)


def get_builder(force):
    return venv.EnvBuilder(
        # XXX: We use global site-packages as we don't want to re-install
        # zeusci at virtualenv; if there is an obvious way to do this, we
        # will NOT use global site-packages
        system_site_packages=True,
        clear=force,
        symlinks=True,
        upgrade=False,
    )


def get_venv_dir(root_dir):
    if root_dir is None:
        msg = 'No zeusci project could be found! Tried to find .zci dir'
        raise click.UsageError(msg)
    return abspath(root_dir, 'venv')


def create_venv(root_dir, force):
    venv_dir = get_venv_dir(root_dir)
    if os.path.isdir(venv_dir) and not force:
        click.echo('Virtualenv exists at %s' % venv_dir)
        return
    click.echo("Creating virtualenv at %s" % venv_dir)
    builder = get_builder(force)
    builder.create(venv_dir)
    click.echo('Done')


def get_python_exec(root_dir):
    # TODO: Let user specify this
    venv_dir = get_venv_dir(root_dir)
    return abspath(venv_dir, 'bin', 'python')


def install_setuptools(root_dir):
    # TODO: put setuptools source distribution at some temporary path
    py_exec = get_python_exec(root_dir)
    ez_setup = abspath(root_dir, 'config', 'ez_setup.py')
    cmd = [py_exec, '-E', ez_setup]
    subprocess.call(cmd)


def install_pip():
    easy_install = shutil.which('easy_install')
    cmd = [easy_install, 'pip']
    subprocess.call(cmd)


def install_packages(root_dir):
    click.echo('Installing packages ...')
    requirements_path = abspath(root_dir, 'config', 'requirements.txt')
    pip = shutil.which('pip')
    cmd = [pip, 'install', '-r', requirements_path]
    subprocess.call(cmd)
    click.echo('Done')



@click.command(name='bootstrap')
@click.option('-f', '--force', is_flag=True, default=False)
def bootstrap_cmd(project_path, force):
    root_dir = get_project_root(project_path)
    click.echo("ROOT_DIR = %r" % root_dir)
    create_venv(root_dir, force=force)
    install_setuptools(root_dir)
    install_pip()
    install_packages(root_dir)


cli.add_command(init_cmd)
cli.add_command(bootstrap_cmd)


def main():
    cli()
