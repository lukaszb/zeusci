from django.test import TestCase
from django.core.urlresolvers import reverse


class BaseApiTestCase(TestCase):
    
    def make_url(self, view_name, **kwargs):
        return 'http://testserver' + reverse(view_name, kwargs=kwargs)

    def make_build_detail_url(self, name, number):
        return self.make_url('zeus_api_build_detail', name=name, build_no=number)

