from django.test import TestCase
from django.core.urlresolvers import reverse
from zeus.models import Project


def make_url(view_name, **kwargs):
    return 'http://testserver' + reverse(view_name, kwargs=kwargs)


class TestProjectApi(TestCase):
    maxDiff = None

    def setUp(self):
        Project.objects.create(
            name='zeus',
            url='https://github.com/lukaszb/zeus',
            repo_url='git://github.com/lukaszb/zeus.git',
        )
        Project.objects.create(
            name='frogress',
            url='https://github.com/lukaszb/frogress',
            repo_url='git://github.com/lukaszb/frogress.git',
        )

    def test_project_list(self):
        url = reverse('zeus_api_project_list')
        response = self.client.get(url)
        self.assertItemsEqual(response.data, [
            {
                'uri': make_url('zeus_api_project_detail', name='zeus'),
                'name': 'zeus',
                'project_url': 'https://github.com/lukaszb/zeus',
                'repo_url': 'git://github.com/lukaszb/zeus.git'
            },
            {
                'uri': make_url('zeus_api_project_detail', name='frogress'),
                'name': 'frogress',
                'project_url': 'https://github.com/lukaszb/frogress',
                'repo_url': 'git://github.com/lukaszb/frogress.git'
            },
        ])

