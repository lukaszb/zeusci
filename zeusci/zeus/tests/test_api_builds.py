from .test_api_base import BaseApiTestCase
from django.core.urlresolvers import reverse
from zeus.models import Build
from zeus.models import Buildset
from zeus.models import Output
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
        self.buildset = Buildset.objects.create(
            project=zeus,
            number=1,
        )
        self.build1 = Build(
            buildset=self.buildset,
            number=1,
        )
        output = Output.objects.create(output='Just started')
        self.build1.build_output = output
        self.build1.save()


        dt = datetime.datetime(2013, 7, 2, 22, 8)
        self.build2 = Build(
            buildset=self.buildset,
            number=2,
            created_at=dt,
            finished_at=(dt + datetime.timedelta(seconds=3)),
            returncode=0,
        )
        output = Output.objects.create(output='Finished')
        self.build2.build_output = output
        self.build2.save()

    def test_build_detail(self):
        url_params = {'name': 'zeus', 'buildset_no': 1, 'build_no': 1}
        url = reverse('zeus_api_build_detail', kwargs=url_params)
        response = self.client.get(url)
        self.assertDictEqual(response.data, {
            'uri': self.make_api_build_detail_url('zeus', 1, 1),
            'url': self.build1.get_absolute_url(),
            'number': 1,
            'created_at': self.build1.created_at,
            'finished_at': self.build1.finished_at,
            'returncode': None,
            'output': 'Just started',
            'status': 'pending',
        })


        url_params = {'name': 'zeus', 'buildset_no': 1, 'build_no': 2}
        url = reverse('zeus_api_build_detail', kwargs=url_params)
        response = self.client.get(url)
        self.assertDictEqual(response.data, {
            'uri': self.make_api_build_detail_url('zeus', 1, 2),
            'url': self.build2.get_absolute_url(),
            'number': 2,
            'created_at': self.build2.created_at,
            'finished_at': self.build2.finished_at,
            'returncode': 0,
            'output': 'Finished',
            'status': 'passed',
        })

