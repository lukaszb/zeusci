import unittest
from zeus.utils.general import lookup_value


class Object(object):
    pass


class TestLookupValue(unittest.TestCase):

    def setUp(self):
        self.obj = Object()
        self.obj.project = Object()
        self.obj.project.name = 'zeus'

    def test_lookup_value(self):
        self.assertEqual(lookup_value(self.obj, 'project'), self.obj.project)
        self.assertEqual(lookup_value(self.obj, 'project__name'), 'zeus')

    def test_lookup_value_not_exist(self):
        with self.assertRaises(AttributeError):
            lookup_value(self.obj, 'project__id')

        with self.assertRaises(AttributeError):
            lookup_value(self.obj, 'foo')

