from django.conf.urls import patterns, url


urlpatterns = patterns('zeus.views',
    url('^p/(?P<name>\w+)/$', 'project_view', name='zeus_project'),
    url('^p/(?P<name>\w+)/build/$', 'project_build_view', name='zeus_project_build'),
)

