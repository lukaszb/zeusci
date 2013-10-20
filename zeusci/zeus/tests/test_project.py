from django.db import models
from django.test import SimpleTestCase
from zeus.project import get_project_model
from zeus.project import Project
import mock


class DummyProject(models.Model):
    name = models.CharField(max_length=128)



class TestGetProject(SimpleTestCase):

    @mock.patch('zeus.project.settings')
    def test_get_project_model(self, settings):
        settings.PROJECT_MODEL = 'zeus.tests.test_project.DummyProject'
        self.assertEqual(get_project_model(), DummyProject)

    def test_get_project_model_defualt(self):
        self.assertEqual(get_project_model(), Project)

