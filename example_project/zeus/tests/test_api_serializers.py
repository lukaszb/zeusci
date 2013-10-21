from django.test import SimpleTestCase
from zeus.api.serializers import BuildDetailSerializer
from zeus.models import Build
from zeus.models import Buildset
from zeus.models import Command
from zeus.models import Project
import mock


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

        cmd1 = Command.objects.create(build=build, number=1)

