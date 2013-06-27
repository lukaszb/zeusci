from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns('zeus.views',
    url('^p/(?P<name>\w+)/$', 'project_view', name='zeus_project_detail'),
    url('^p/(?P<name>\w+)/build/(?P<build_no>\d+)/$',
        view='project_build_detail_view',
        name='zeus_project_build_detail'),
    url('^p/(?P<name>\w+)/build/(?P<build_no>\d+)\.(?P<step_no>\d+)/$',
        view='project_build_step_detail_view',
        name='zeus_project_build_step_detail'),

    url('^p/(?P<name>\w+)/build/$',
        view='project_build_view',
        name='zeus_project_build'),
    url('^p/force/(?P<name>\w+)/build/(?P<build_no>\d+)\.(?P<step_no>\d+)/$',
        view='project_build_step_view',
        name='zeus_force_project_build_step'),
)

