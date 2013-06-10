from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

home = TemplateView.as_view(template_name='base.html')


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^', include('zeus.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

