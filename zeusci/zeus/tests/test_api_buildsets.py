from .test_api_base import BaseApiTestCase
from django.core.urlresolvers import reverse
from rest_framework.status import HTTP_201_CREATED
from unittest import mock
from zeusci.zeus.models import Buildset
from zeusci.zeus.models import Project
import datetime


class TestBuildsetApi(BaseApiTestCase):
    maxDiff = None

    def setUp(self):
        zeus = Project.objects.create(
            name='zeus',
            website_url='https://github.com/lukaszb/zeus',
            repo_url='git://github.com/lukaszb/zeus.git',
        )
        self.frogress = Project.objects.create(
            name='frogress',
            website_url='https://github.com/lukaszb/frogress',
            repo_url='git://github.com/lukaszb/frogress.git',
        )
        dt = datetime.datetime(2013, 6, 13, 23, 12)
        self.bs1 = Buildset.objects.create(
            project=zeus,
            number=1,
            created_at=dt,
        )
        self.bs2 = Buildset.objects.create(
            project=zeus,
            number=2,
            created_at=dt,
            build_dir='/tmp/zeus/2',
        )
        self.bs3 = Buildset.objects.create(
            project=zeus,
            number=3,
            created_at=dt,
            finished_at=dt,
        )
        self.bs4 = Buildset.objects.create(
            project=self.frogress,
            number=1,
            created_at=dt
        )

    def test_buildset_list(self):
        url = reverse('zeus_api_buildset_list', kwargs={'name': 'zeus'})
        response = self.client.get(url)
        results = [
            {
                'uri': self.make_api_buildset_detail_url('zeus', 3),
                'url': self.bs3.get_absolute_url(),
                'number': 3,
                'created_at': self.bs3.created_at,
                'finished_at': self.bs3.created_at,
                'status': 'pending',
                'builds': [],
                'errors': [],
                'branch': None,
            },
            {
                'uri': self.make_api_buildset_detail_url('zeus', 2),
                'url': self.bs2.get_absolute_url(),
                'number': 2,
                'created_at': self.bs2.created_at,
                'finished_at': self.bs2.finished_at,
                'status': 'pending',
                'builds': [],
                'errors': [],
                'branch': None,
            },
            {
                'uri': self.make_api_buildset_detail_url('zeus', 1),
                'url': self.bs1.get_absolute_url(),
                'number': 1,
                'created_at': self.bs1.created_at,
                'finished_at': self.bs1.finished_at,
                'status': 'pending',
                'builds': [],
                'errors': [],
                'branch': None,
            },
        ]
        self.assertEqual(response.data['results'], results)

    @mock.patch('zeusci.zeus.api.views.do_buildset')
    def test_buildset_new(self, do_buildset):
        url = reverse('zeus_api_buildset_list', kwargs={'name': 'frogress'})
        response = self.client.post(url, data={'branch': 'foo'})
        assert response.status_code == HTTP_201_CREATED

        # Make sure new buildset was created (there was one at setup already)
        buildset = self.frogress.buildsets.get(number=2)
        assert response.data['number'] == 2
        assert response.data['url'] == buildset.get_absolute_url()

        do_buildset.delay.assert_called_once_with(buildset)
