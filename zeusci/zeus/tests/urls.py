from django.conf.urls import patterns, url
from zeusci.zeus.api.urls import urlpatterns as api_urlpatterns


urlpatterns = patterns('zeusci.zeus.views',
    # the same view handles those paths as frontend client is responsible for
    # further routing.
    url('^p/(?P<name>[-\w]+)/*',
        view='project_view',
        name='zeus_project_detail'),
    # we need buildset/build routes here so the urls can be bookmarked (or page
    # refreshed)
    url('^p/(?P<name>[-\w]+)/buildsets/(?P<buildset_no>\d+)/$',
        view='project_view',
        name='zeus_project_buildset_detail'),
    url('^p/(?P<name>[-\w]+)/buildsets/(?P<buildset_no>\d+)\.(?P<build_no>\d+)/$',
        view='project_view',
        name='zeus_project_build_detail'),
) + api_urlpatterns

