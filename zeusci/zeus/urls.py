from django.conf.urls import patterns, url


urlpatterns = patterns('zeus.views',
    url('^p/(?P<project_name>\w+)/$', 'project_view', name='zeus_project'),
)

