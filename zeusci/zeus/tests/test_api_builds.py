from .test_api_base import BaseApiTestCase
from django.core.urlresolvers import reverse
from django.core.cache import cache
from zeusci.zeus.models import Build
from zeusci.zeus.models import Buildset
from zeusci.zeus.models import Command
from zeusci.zeus.models import Output
from zeusci.zeus.models import Project
from zeusci.zeus.models import Status
import datetime


class TestBuildApi(BaseApiTestCase):
    maxDiff = None
    urls = 'zeusci.zeus.tests.urls'

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
        self.build1 = Build.objects.create(
            buildset=self.buildset,
            number=1,
        )
        self.build1_cmd1 = Command.objects.create(
            number=1,
            build=self.build1,
            title='Step 1 -- Configuration',
            cmd=['./configure'],
        )
        output = Output.objects.create(output='Configured')
        self.build1_cmd1.command_output = output
        delta = datetime.timedelta(seconds=2)
        self.build1_cmd1.started_at = self.build1_cmd1.created_at + delta
        self.build1_cmd1.finished_at = self.build1_cmd1.started_at + delta
        self.build1_cmd1.returncode = 0
        self.build1_cmd1.status = Status.PASSED
        self.build1_cmd1.save()

        self.build1_cmd2 = Command.objects.create(
            number=2,
            build=self.build1,
            title='Step 2 -- Build',
            cmd=['make', 'all'],
        )
        output = Output.objects.create(output='Build in progress ...')
        self.build1_cmd2.command_output = output
        self.build1_cmd2.started_at = self.build1_cmd2.created_at
        self.build1_cmd2.status = Status.RUNNING
        self.build1_cmd2.save()


        dt = datetime.datetime(2013, 7, 2, 22, 8)
        self.build2 = Build(
            buildset=self.buildset,
            number=2,
            created_at=dt,
            finished_at=(dt + datetime.timedelta(seconds=3)),
        )
        self.build2.save()
        cache.clear()

    def test_build_detail(self):
        url_params = {'name': 'zeus', 'buildset_no': 1, 'build_no': 1}
        url = reverse('zeus_api_build_detail', kwargs=url_params)
        response = self.client.get(url)
        expected = {
            'uri': self.make_api_build_detail_url('zeus', 1, 1),
            'url': self.build1.get_absolute_url(),
            'number': 1,
            'created_at': self.build1.created_at,
            'finished_at': self.build1.finished_at,
            'status': 'running',
            'commands': [
                {
                    'number': 1,
                    'title': 'Step 1 -- Configuration',
                    'cmd': './configure',
                    'output': 'Configured',
                    'started_at': self.build1_cmd1.started_at,
                    'finished_at': self.build1_cmd1.finished_at,
                    'status': 'passed',
                    'returncode': 0,
                },
                {
                    'number': 2,
                    'title': 'Step 2 -- Build',
                    'cmd': 'make all',
                    'output': 'Build in progress ...',
                    'started_at': self.build1_cmd2.started_at,
                    'finished_at': None,
                    'status': 'running',
                    'returncode': None,
                },
            ],
        }
        self.assertDictEqual(response.data, expected)

        url_params = {'name': 'zeus', 'buildset_no': 1, 'build_no': 2}
        url = reverse('zeus_api_build_detail', kwargs=url_params)
        response = self.client.get(url)
        expected = {
            'uri': self.make_api_build_detail_url('zeus', 1, 2),
            'url': self.build2.get_absolute_url(),
            'number': 2,
            'created_at': self.build2.created_at,
            'finished_at': self.build2.finished_at,
            'status': 'pending',
            'commands': [],
        }
        self.assertDictEqual(response.data, expected)

    def test_build_restart_fails_if_build_is_still_running(self):
        url_params = {'name': 'zeus', 'buildset_no': 1, 'build_no': 1}
        url = reverse('zeus_api_build_detail', kwargs=url_params)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 409)

    def test_build_restart(self):
        url_params = {'name': 'zeus', 'buildset_no': 1, 'build_no': 1}
        url = reverse('zeus_api_build_detail', kwargs=url_params)
        self.build1.commands.update(status=Status.FAILED)

        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['status'], Status.PENDING)
        self.assertIsNone(response.data['finished_at'])
        self.assertEqual(self.build1.commands.count(), 0)

    def test_build_status_is_changing_correctly(self):
        self.assertEqual(self.build1.status, Status.RUNNING)

        self.build1_cmd1.status = Status.FAILED
        self.build1_cmd1.save()
        self.assertEqual(self.build1.status, Status.FAILED)

        self.build1.commands.update(status=Status.PASSED)
        self.assertEqual(self.build1.status, Status.PASSED)

        self.build1.commands.all().delete()
        self.assertEqual(self.build1.status, Status.PENDING)

        # Create a command and make sure status us RUNNING once again
        Command.objects.create(
            number=1,
            build=self.build1,
            title='Step 1 -- Configuration',
            cmd=['./configure'],
            status=Status.RUNNING,
        )
        self.assertEqual(self.build1.status, Status.RUNNING)

