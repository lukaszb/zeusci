from zeus.utils.choices import Choices
import unittest


class TestChoices(unittest.TestCase):

    def test_choices(self):
        status = Choices('pending', 'running', 'passed', 'failed')
        self.assertEqual(status.pending, 'pending')
        self.assertEqual(status.running, 'running')
        self.assertEqual(status.passed, 'passed')
        self.assertEqual(status.failed, 'failed')

    def test_with_kwargs(self):
        choices = Choices('foo', Bar=2, baz='Baz')
        self.assertEqual(choices.foo, 'foo')
        self.assertEqual(choices.Bar, 2)
        self.assertEqual(choices.baz, 'Baz')

    def test_as_dict(self):
        status = Choices('pending', 'running', passed='success')
        self.assertDictEqual(status.as_dict(), {
            'pending': 'pending',
            'running': 'running',
            'passed': 'success',
        })

