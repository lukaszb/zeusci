from __future__ import unicode_literals
from django.conf.urls import patterns
from smarturls import surl


urlpatterns = patterns('zeus.views',
    surl('/p/<slug:name>/$', 'project_view', name='zeus_project_detail'),
    surl('/p/<slug:name>/buildset/<int:buildset_no>/$',
        view='project_buildset_detail_view',
        name='zeus_project_buildset_detail'),
    surl('/p/<slug:name>/builds/<int:buildset_no>\.<int:build_no>/$',
        view='project_build_detail_view',
        name='zeus_project_build_detail'),

    surl('/p/<slug:name>/buildset/$',
        view='project_buildset_view',
        name='zeus_force_project_buildset'),
    surl('/p/force/<slug:name>/builds/<int:buildset_no>\.<int:build_no>/$',
        view='project_build_view',
        name='zeus_force_project_build'),
)

