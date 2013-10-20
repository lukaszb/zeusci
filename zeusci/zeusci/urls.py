from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView
#import socketio.sdjango


admin.autodiscover()

class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        from zeus.models import Project
        data = super(HomeView, self).get_context_data(**kwargs)
        data['projects'] = Project.objects.all()
        return data

home = HomeView.as_view()


urlpatterns = patterns('',
    #url("^socket\.io", include(socketio.sdjango.urls)),
    url(r'^$', home, name='home'),
    url(r'^api/', include('zeus.api.urls')),
    url(r'^', include('zeus.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

