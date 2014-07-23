import click
import os
import shutil
import subprocess
import venv
import zeusci


abspath = lambda *p: os.path.abspath(os.path.join(*p))


CI_TEMPLATE_PATH = abspath(zeusci.__path__[0], 'conf', 'citemplate')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DEFAULT_PROJECT_ROOT = os.path.expanduser('~/.zeusci')


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    project_root = get_project_root()
    click.echo(" => Using zeus-ci instance at %s" % project_root)


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
            return DEFAULT_PROJECT_ROOT
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


def get_manage_py(root_dir):
    return abspath(root_dir, 'app', 'manage.py')


def run_django_cmd(root_dir, cmd):
    python = get_python_exec(root_dir)
    manage = get_manage_py(root_dir)

    cmd = [python, manage] + cmd
    return subprocess.call(cmd)


def prepare_db(root_dir):
    run_django_cmd(root_dir, ['syncdb', '--noinput'])


@click.command(name='bootstrap')
@click.option('-f', '--force', is_flag=True, default=False)
def bootstrap_cmd(project_path, force):
    root_dir = get_project_root(project_path)
    click.echo("ROOT_DIR = %r" % root_dir)
    create_venv(root_dir, force=force)
    install_setuptools(root_dir)
    install_pip()
    install_packages(root_dir)
    prepare_db(root_dir)


def get_supervisor_daemon():
    return shutil.which('supervisord')


def get_supervisor_ctl():
    return shutil.which('supervisorctl')


def get_supervisor_config(project_root):
    return abspath(project_root, 'config/supervisord.conf')


def run_supervisor(project_root, executable, cmd):
    config = get_supervisor_config(project_root)
    if isinstance(cmd, str):
        cmd = [cmd]
    return subprocess.call([executable, '-c', config] + cmd)


def run_supervisor_daemon(project_root, args=None):
    args = args or []
    return run_supervisor(project_root, get_supervisor_daemon(), args)


def run_supervisor_ctl(project_root, cmd):
    return run_supervisor(project_root, get_supervisor_ctl(), cmd)


@click.command(name='start')
@click.pass_context
def start_cmd(ctx):
    project_path = get_project_root()
    if not os.path.exists(project_path):
        ctx.invoke(init_cmd, project_path=project_path, bootstrap=True)
    prepare_db(project_path)
    run_supervisor_daemon(project_path)
    click.echo(" => Webserver started at: http://127.0.0.1:23115")


@click.command(name='status')
def status_cmd():
    project_root = get_project_root()
    run_supervisor_ctl(project_root, 'status')


def stop_supervisor_daemon(project_root):
    run_supervisor_ctl(project_root, 'shutdown')


@click.command(name='stop')
def stop_cmd():
    project_root = get_project_root()
    run_supervisor_ctl(project_root, 'stop all')
    stop_supervisor_daemon(project_root)


cli.add_command(init_cmd)
cli.add_command(bootstrap_cmd)
cli.add_command(start_cmd)
cli.add_command(status_cmd)
cli.add_command(stop_cmd)


def main():
    cli()
