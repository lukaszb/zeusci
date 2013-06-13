from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('zeus_api_project_list', request=request),
    })



urlpatterns = patterns('zeus.api.views',
    url(r'^$', api_root, name='zeus_api_root'),
    url(r'projects$',
        view='project_list',
        name='zeus_api_project_list'),
    url(r'projects/(?P<name>\w+)$',
        view='project_detail',
        name='zeus_api_project_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

