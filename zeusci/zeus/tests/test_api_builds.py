from .test_api_base import BaseApiTestCase
from django.core.urlresolvers import reverse
from zeus.models import Build
from zeus.models import Project
import datetime


class TestBuildApi(BaseApiTestCase):
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
        Build.objects.create(project=zeus, number=1)
        Build.objects.create(project=zeus, number=2, build_dir='/tmp/zeus/2')
        dt = datetime.datetime(2013, 6, 13, 23, 12)
        Build.objects.create(project=zeus, number=3, finished_at=dt)
        Build.objects.create(project=frogress, number=1)

    def test_build_list(self):
        url = reverse('zeus_api_build_list', kwargs={'name': 'zeus'})
        response = self.client.get(url)
        self.assertItemsEqual(response.data, [
            {
                'uri': self.make_build_detail_url('zeus', 1),
            },
            {
                'uri': self.make_build_detail_url('zeus', 2),
            },
            {
                'uri': self.make_build_detail_url('zeus', 3),
            },
        ])

