from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()


class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        from zeusci.zeus.models import Project
        data = super(HomeView, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        return data

home = HomeView.as_view()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^api/', include('zeusci.zeus.api.urls')),
    url(r'^api-docs/', include('rest_framework_swagger.urls')),
    url(r'^', include('zeusci.zeus.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

