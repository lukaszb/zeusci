from __future__ import unicode_literals
from django.conf.urls import patterns, url
from smarturls import surl


urlpatterns = patterns('zeusci.zeus.views',
    # TODO: make helper 'build forcers' proper API endpoints
    surl('/p/<slug:name>/buildset/$',
        view='project_buildset_view',
        name='zeus_force_project_buildset'),
    surl('/p/force/<slug:name>/builds/<int:buildset_no>\.<int:build_no>/$',
        view='project_build_view',
        name='zeus_force_project_build'),

    # the same view handles those paths as frontend client is responsible for
    # further routing.
    url('^p/(?P<name>[-\w]+)/*',
        view='project_view',
        name='zeus_project_detail'),
    # we need following as we want for:
    # - pass serialized data for buildset/build (faster loading)
    # - reversing urls at backend
    url('^p/(?P<name>[-\w]+)/buildsets/(?P<buildset_no>\d+)/$',
        view='project_view',
        name='zeus_project_buildset_detail'),
    url('^p/(?P<name>[-\w]+)/buildsets/(?P<buildset_no>\d+)\.(?P<build_no>\d+)/$',
        view='project_view',
        name='zeus_project_build_detail'),
)

