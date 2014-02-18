from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()


class HomeView(RedirectView):
    permanent = False
    pattern_name = 'zeus_project_list'


home = HomeView.as_view()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^api/', include('zeusci.zeus.api.urls')),
    url(r'^', include('zeusci.zeus.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

