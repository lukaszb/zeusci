from django.test import TestCase
from ..models import Buildset
from ..models import Status


class TestBuildset(TestCase):

    def test_get_status_for_buildset_with_errors(self):
        buildset = Buildset(errors=[{
            'reason': 'Foo bar',
        }])
        self.assertEqual(buildset.get_status(), Status.FAILED)

