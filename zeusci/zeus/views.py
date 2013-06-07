from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from .conf import settings
from .models import Project
from .tasks import build_project



class ProjectView(TemplateView):
    template_name = 'zeus/project.html'

    def get_project(self, name):
        return Project.objects.for_name(name)

    def get_context_data(self, **kwargs):
        data = super(ProjectView, self).get_context_data(**kwargs)
        data['project'] = self.get_project(kwargs['name'])
        data['settings'] = settings
        return data


project_view = ProjectView.as_view()


class ProjectBuildView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('zeus_project', kwargs={'name': self.project_name})

    def get(self, request, name):
        self.project_name = name
        build_project.delay(Project.objects.for_name(name))
        return super(ProjectBuildView, self).get(request, name)

project_build_view = ProjectBuildView.as_view()

