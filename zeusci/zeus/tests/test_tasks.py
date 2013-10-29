from __future__ import unicode_literals
from django.test import SimpleTestCase
from unittest import mock
from zeusci.zeus.tasks import do_build
from zeusci.zeus.tasks import do_build_project


class DummyBuilder(object):
    def build(self, build):
        self.builded_with = build


class TestDoBuild(SimpleTestCase):

    def test_do_build(self):
        build = mock.Mock()
        builder = mock.Mock()
        do_build(build, builder)
        builder.build.assert_called_once_with(build)

    def test_do_build_for_builder_class_instead_of_instance(self):

        called = []

        class DummyBuilder(object):
            def build(self, build):
                called.append(build)

        build = mock.Mock()
        do_build(build, DummyBuilder)

        self.assertEqual(called, [build])



class TestDoBuildProject(SimpleTestCase):

    def test_do_build_project(self):
        builder = mock.Mock()
        project = mock.Mock()
        project.get_builder.return_value = builder
        do_build_project(project)

        builder.build_project.assert_called_once_with(project, branch=None)

