from django.test import TestCase
from ..models import Buildset
from ..models import Project
from ..models import Status


class TestBuildset(TestCase):

    def test_get_status_for_buildset_with_errors(self):
        buildset = Buildset(errors=[{
            'reason': 'Foo bar',
        }])
        self.assertEqual(buildset.get_status(), Status.FAILED)

    def test_save_error_with_bytes(self):
        zeus = Project.objects.create(
            name='zeus',
            url='https://github.com/lukaszb/zeus',
            repo_url='git://github.com/lukaszb/zeus.git',
        )
        self.buildset = Buildset.objects.create(
            project=zeus,
            number=1,
            errors=[{'stderr': b'error output'}],
        )
        self.assertEqual(self.buildset.errors[0]['stderr'], 'error output')

