from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from unittest import mock
from zeusci.zeus.models import Buildset
from zeusci.zeus.models import Project
from .test_api_base import BaseApiTestCase
import datetime

class TestProjectApi(BaseApiTestCase):
    maxDiff = None
    client_class = APIClient

    def setUp(self):
        self.zeus = Project.objects.create(
            name='zeus',
            website_url='https://github.com/lukaszb/zeus',
            repo_url='git://github.com/lukaszb/zeus.git',
        )
        self.frogress = Project.objects.create(
            name='frogress',
            website_url='https://github.com/lukaszb/frogress',
            repo_url='git://github.com/lukaszb/frogress.git',
        )
        Buildset.objects.create(project=self.zeus, number=1)
        Buildset.objects.create(project=self.zeus, number=2, build_dir='/tmp/zeus/2')
        dt = datetime.datetime(2013, 6, 13, 23, 12)
        Buildset.objects.create(project=self.zeus, number=3, finished_at=dt)

    def test_create(self):
        url = reverse('zeus_api_project_list')
        response = self.client.post(url, {
            'name': 'ack-vim',
            'website_url': 'http://github.com/vim-scripts/ack.vim',
            'repo_url': 'git://github.com/vim-scripts/ack.vim.git',
        })

        self.assertEqual(response.status_code, 201, response.data)

    def test_project_list(self):
        url = reverse('zeus_api_project_list')
        response = self.client.get(url)
        results = [
            {
                'uri': self.make_url('zeus_api_project_detail', name='zeus'),
                'name': 'zeus',
                'website_url': 'https://github.com/lukaszb/zeus',
                'repo_url': 'git://github.com/lukaszb/zeus.git',
                'url': self.zeus.get_absolute_url(),
                'buildsets_uri': self.make_api_buildset_list_url('zeus'),
            },
            {
                'uri': self.make_url('zeus_api_project_detail', name='frogress'),
                'name': 'frogress',
                'website_url': 'https://github.com/lukaszb/frogress',
                'repo_url': 'git://github.com/lukaszb/frogress.git',
                'url': self.frogress.get_absolute_url(),
                'buildsets_uri': self.make_api_buildset_list_url('frogress'),
            },
        ]
        self.assertEqual(response.data['results'], results)

    @mock.patch('zeusci.zeus.models.settings')
    def test_project_detail(self, settings):
        settings.PROJECT_BUILDSETS_COUNT = 10
        url = reverse('zeus_api_project_detail', kwargs={'name': 'zeus'})
        buildset1 = Buildset.objects.get(project__name='zeus', number=1)
        buildset2 = Buildset.objects.get(project__name='zeus', number=2)
        buildset3 = Buildset.objects.get(project__name='zeus', number=3)
        response = self.client.get(url)
        self.assertDictEqual(response.data, {
            'uri': self.make_url('zeus_api_project_detail', name='zeus'),
            'name': 'zeus',
            'website_url': 'https://github.com/lukaszb/zeus',
            'repo_url': 'git://github.com/lukaszb/zeus.git',
            'url': self.zeus.get_absolute_url(),
            'buildsets_uri': self.make_api_buildset_list_url('zeus'),
            'buildsets_total_count': 3,
            'buildsets_recent': [
                {
                    'uri': self.make_api_buildset_detail_url('zeus', 3),
                    'url': buildset3.get_absolute_url(),
                    'number': 3,
                    'created_at': buildset3.created_at,
                    'finished_at': buildset3.finished_at,
                    'status': 'pending',
                    'builds': [],
                    'errors': [],
                },
                {
                    'uri': self.make_api_buildset_detail_url('zeus', 2),
                    'url': buildset2.get_absolute_url(),
                    'number': 2,
                    'created_at': buildset2.created_at,
                    'finished_at': buildset2.finished_at,
                    'status': 'pending',
                    'builds': [],
                    'errors': [],
                },
                {
                    'uri': self.make_api_buildset_detail_url('zeus', 1),
                    'url': buildset1.get_absolute_url(),
                    'number': 1,
                    'created_at': buildset1.created_at,
                    'finished_at': buildset1.finished_at,
                    'status': 'pending',
                    'builds': [],
                    'errors': [],
                },
            ],
        })

    @mock.patch('zeusci.zeus.models.settings')
    def test_project_detail_respects_buildsets_count(self, settings):
        settings.PROJECT_BUILDSETS_COUNT = 2
        url = reverse('zeus_api_project_detail', kwargs={'name': 'zeus'})
        response = self.client.get(url)
        self.assertEqual(response.data['buildsets_total_count'], 3)
        self.assertEqual([bs['uri'] for bs in response.data['buildsets_recent']], [
            self.make_api_buildset_detail_url('zeus', 3),
            self.make_api_buildset_detail_url('zeus', 2),
        ])

