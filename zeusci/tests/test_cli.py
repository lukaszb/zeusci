from click.testing import CliRunner
from unittest import mock
from zeusci.cli import create_venv
from zeusci.cli import get_builder
from zeusci.cli import init_cmd
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
