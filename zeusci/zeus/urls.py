from __future__ import unicode_literals
from django.conf.urls import patterns
from smarturls import surl


urlpatterns = patterns('zeus.views',
    surl('/p/<slug:name>/$', 'project_view', name='zeus_project_detail'),
    surl('/p/<slug:name>/build/<int:build_no>/$',
        view='project_build_detail_view',
        name='zeus_project_build_detail'),
    surl('/p/<slug:name>/build/<int:build_no>\.<int:step_no>/$',
        view='project_build_step_detail_view',
        name='zeus_project_build_step_detail'),

    surl('/p/<slug:name>/build/$',
        view='project_build_view',
        name='zeus_project_build'),
    surl('/p/force/<slug:name>/build/<int:build_no>\.<int:step_no>/$',
        view='project_build_step_view',
        name='zeus_force_project_build_step'),
)

