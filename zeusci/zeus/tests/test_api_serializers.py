from django.test import SimpleTestCase
from unittest import mock
from zeusci.zeus.api.serializers import BuildDetailSerializer
from zeusci.zeus.models import Build
from zeusci.zeus.models import Buildset
from zeusci.zeus.models import Project


def serialize(build):
    request = mock.Mock()
    # pass request as we use HyperlinkedIdentityField and without it
    # deprecation warning would be issued
    return BuildDetailSerializer(build, context={'request': request}).data


class TestBuildDetailSerializer(SimpleTestCase):


    def test_status(self):
        project = Project(name='zeus')

        buildset = Buildset(project=project, number=2)

        # set pk so it fakes db-saved instance
        build = Build(number=103, buildset=buildset, pk=1)

        # status without commands
        self.assertEqual(serialize(build)['status'], 'pending')


