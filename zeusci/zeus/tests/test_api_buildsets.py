from .test_api_base import BaseApiTestCase
from django.core.urlresolvers import reverse
from zeus.models import Buildset
from zeus.models import Project
import datetime


class TestBuildsetApi(BaseApiTestCase):
    maxDiff = None

    def setUp(self):
        zeus = Project.objects.create(
            name='zeus',
            url='https://github.com/lukaszb/zeus',
            repo_url='git://github.com/lukaszb/zeus.git',
        )
        frogress = Project.objects.create(
            name='frogress',
            url='https://github.com/lukaszb/frogress',
            repo_url='git://github.com/lukaszb/frogress.git',
        )
        Buildset.objects.create(project=zeus, number=1)
        Buildset.objects.create(project=zeus, number=2, build_dir='/tmp/zeus/2')
        dt = datetime.datetime(2013, 6, 13, 23, 12)
        Buildset.objects.create(project=zeus, number=3, finished_at=dt)
        Buildset.objects.create(project=frogress, number=1)

    def test_buildset_list(self):
        url = reverse('zeus_api_buildset_list', kwargs={'name': 'zeus'})
        response = self.client.get(url)
        results = [
            {
                'uri': self.make_buildset_detail_url('zeus', 3),
                'builds': [],
            },
            {
                'uri': self.make_buildset_detail_url('zeus', 2),
                'builds': [],
            },
            {
                'uri': self.make_buildset_detail_url('zeus', 1),
                'builds': [],
            },
        ]
        self.assertEqual(response.data['results'], results)

