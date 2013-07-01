from django.test import TestCase
from django.core.urlresolvers import reverse


class BaseApiTestCase(TestCase):

    def make_url(self, view_name, **kwargs):
        return 'http://testserver' + reverse(view_name, kwargs=kwargs)

    def make_buildset_list_url(self, name):
        return self.make_url('zeus_api_buildset_list', name=name)

    def make_buildset_detail_url(self, name, number):
        return self.make_url('zeus_api_buildset_detail', name=name, buildset_no=number)

