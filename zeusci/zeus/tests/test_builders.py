from __future__ import unicode_literals
from django.test import SimpleTestCase
from zeus.models import Project
from zeus.builders import PythonBuilder


class TestPythonBuildseter(SimpleTestCase):

    def setUp(self):
        self.builder = PythonBuilder()

    def test_build(self):
        #self.builder
        pass

