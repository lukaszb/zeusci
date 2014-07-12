from click.testing import CliRunner
from unittest import mock
from zeusci.cli import create_venv
from zeusci.cli import get_builder
from zeusci.cli import init_cmd
from zeusci.cli import start_cmd
from zeusci.cli import status_cmd
from zeusci.cli import stop_cmd
import pytest


@mock.patch('zeusci.cli.venv')
def test_get_builder(venv):
    builder = mock.Mock()
    venv.EnvBuilder.return_value = builder
    assert get_builder(force=True) == builder


@pytest.mark.parametrize('force', [False, True])
def test_get_builder_respects_force_argument(force):
    builder = get_builder(force=force)
    assert builder.clear is force


@mock.patch('zeusci.cli.get_builder')
@mock.patch('zeusci.cli.get_venv_dir')
def test_create_env(get_venv_dir, get_builder):
    get_venv_dir.return_value = '/tmp/foo'
    get_builder.return_value = builder = mock.Mock()

    create_venv('/tmp', force=False)
    builder.create.assert_called_once_with('/tmp/foo')


@pytest.fixture
def runner():
    return CliRunner()


@mock.patch('zeusci.cli.bootstrap_cmd')
@mock.patch('zeusci.cli.init_existing_dir')
@mock.patch('zeusci.cli.init_new_dir')
def test_init_cmd(init_new_dir, init_existing_dir, bootstrap_cmd, runner):
    result = runner.invoke(init_cmd)
    assert not result.exception

    init_existing_dir.assert_called_once_with('.')
    bootstrap_cmd.assert_called_once_with(project_path='.', force=False)


@mock.patch('zeusci.cli.get_project_root')
@mock.patch('zeusci.cli.run_supervisor_daemon')
@mock.patch('zeusci.cli.prepare_db')
@mock.patch('zeusci.cli.init_cmd')
@mock.patch('zeusci.cli.os.path')
def test_start_cmd(os_path, init_cmd, prepare_db, run_supervisor_daemon,
                   get_project_root, runner):
    get_project_root.return_value = '/tmp/foo'
    os_path.exists.return_value = False

    result = runner.invoke(start_cmd)
    assert not result.exception

    init_cmd.assert_called_once_with(project_path='/tmp/foo', bootstrap=True)
    prepare_db.assert_called_once_with('/tmp/foo')
    run_supervisor_daemon('/tmp/foo')


@mock.patch('zeusci.cli.get_project_root')
@mock.patch('zeusci.cli.run_supervisor_ctl')
@mock.patch('zeusci.cli.stop_supervisor_daemon')
def test_stop_cmd(stop_supervisor_daemon, run_supervisor_ctl, get_project_root,
                  runner):
    project_root = get_project_root.return_value = '/tmp/foo'

    result = runner.invoke(stop_cmd)
    assert not result.exception

    run_supervisor_ctl.assert_called_once_with(project_root, 'stop all')
    stop_supervisor_daemon.assert_called_once_with(project_root)


@mock.patch('zeusci.cli.get_project_root')
@mock.patch('zeusci.cli.run_supervisor_ctl')
def test_status_cmd(run_supervisor_ctl, get_project_root, runner):
    project_root = get_project_root.return_value = '/tmp/foo'

    result = runner.invoke(status_cmd)
    assert not result.exception

    run_supervisor_ctl.assert_called_once_with(project_root, 'status')
