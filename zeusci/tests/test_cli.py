from zeusci.cli import BootstrapCommand
from unittest import mock
import argparse
import unittest


class TestPrepareCommand(unittest.TestCase):

    def setUp(self):
        self.command = BootstrapCommand()

    @mock.patch('zeusci.cli.venv')
    def test_get_builder(self, venv):
        namespace = argparse.Namespace(force=False)

        builder = mock.Mock()
        venv.EnvBuilder.return_value = builder
        self.assertEqual(self.command.get_builder(namespace), builder)

    def test_get_builder_respects_force_argument(self):
        namespace = argparse.Namespace(force=False)
        builder = self.command.get_builder(namespace)

        self.assertFalse(builder.clear)

        namespace = argparse.Namespace(force=True)
        builder = self.command.get_builder(namespace)

        self.assertTrue(builder.clear)

    def test_create_env(self):
        builder = mock.Mock()
        self.command.get_builder = mock.Mock(return_value=builder)
        self.command.get_venv_dir = mock.Mock(return_value='/tmp/foo')
        namespace = argparse.Namespace(force=False)

        self.command.create_venv(namespace)
        builder.create.assert_called_once_with('/tmp/foo')

