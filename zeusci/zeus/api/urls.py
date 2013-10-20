from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns
from smarturls import surl


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('zeus_api_project_list', request=request),
    })



urlpatterns = patterns('zeus.api.views',
    url(r'^$', api_root, name='zeus_api_root'),
    surl('projects$',
        view='project_list',
        name='zeus_api_project_list'),
    surl('/projects/<slug:name>$',
        view='project_detail',
        name='zeus_api_project_detail'),
    surl('/projects/<slug:name>/buildsets$',
        view='buildset_list',
        name='zeus_api_buildset_list'),
    #surl('/projects/<slug:name>/buildsets/new$',
        #view='buildset_new',
        #name='zeus_api_buildset_new'),
    surl('/projects/<slug:name>/buildsets/<int:buildset_no>$',
        view='buildset_detail',
        name='zeus_api_buildset_detail'),
    surl('/projects/<slug:name>/builds/<int:buildset_no>\.<int:build_no>$',
        view='build_detail',
        name='zeus_api_build_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

