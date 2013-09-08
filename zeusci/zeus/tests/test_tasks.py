from __future__ import unicode_literals
from django.test import SimpleTestCase
from zeus.tasks import do_build
import mock


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

