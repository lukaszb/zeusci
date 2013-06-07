from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView


home = TemplateView.as_view(template_name='base.html')


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^', include('zeus.urls')),
)

