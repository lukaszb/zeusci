from django.core.urlresolvers import reverse
from zeus.models import Buildset
from zeus.models import Project
from .test_api_base import BaseApiTestCase
import datetime


class TestProjectApi(BaseApiTestCase):
    maxDiff = None

    def setUp(self):
        zeus = Project.objects.create(
            name='zeus',
            url='https://github.com/lukaszb/zeus',
            repo_url='git://github.com/lukaszb/zeus.git',
        )
        Project.objects.create(
            name='frogress',
            url='https://github.com/lukaszb/frogress',
            repo_url='git://github.com/lukaszb/frogress.git',
        )
        Buildset.objects.create(project=zeus, number=1)
        Buildset.objects.create(project=zeus, number=2, build_dir='/tmp/zeus/2')
        dt = datetime.datetime(2013, 6, 13, 23, 12)
        Buildset.objects.create(project=zeus, number=3, finished_at=dt)


    def test_project_list(self):
        url = reverse('zeus_api_project_list')
        response = self.client.get(url)
        self.assertItemsEqual(response.data, [
            {
                'uri': self.make_url('zeus_api_project_detail', name='zeus'),
                'name': 'zeus',
                'project_url': 'https://github.com/lukaszb/zeus',
                'repo_url': 'git://github.com/lukaszb/zeus.git'
            },
            {
                'uri': self.make_url('zeus_api_project_detail', name='frogress'),
                'name': 'frogress',
                'project_url': 'https://github.com/lukaszb/frogress',
                'repo_url': 'git://github.com/lukaszb/frogress.git'
            },
        ])

    def test_project_detail(self):
        url = reverse('zeus_api_project_detail', kwargs={'name': 'zeus'})
        response = self.client.get(url)
        self.assertDictEqual(response.data, {
            'uri': self.make_url('zeus_api_project_detail', name='zeus'),
            'name': 'zeus',
            'project_url': 'https://github.com/lukaszb/zeus',
            'repo_url': 'git://github.com/lukaszb/zeus.git',
            'buildsets': [
                {
                    'uri': self.make_buildset_detail_url('zeus', 1),
                    'builds': [],
                },
                {
                    'uri': self.make_buildset_detail_url('zeus', 2),
                    'builds': [],
                },
                {
                    'uri': self.make_buildset_detail_url('zeus', 3),
                    'builds': [],
                },
            ],
        })

