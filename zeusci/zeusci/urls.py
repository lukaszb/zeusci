#from django.conf.urls import patterns, include, url
from coffin.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zeusci.views.home', name='home'),
    # url(r'^zeusci/', include('zeusci.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

from django.views.generic import TemplateView

view = TemplateView.as_view(template_name='base.jinja')

urlpatterns += patterns('',
    url(r'^$', view, name='home'),
)
