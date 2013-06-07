from django.views.generic import TemplateView
from .conf import settings
from .models import Project



class ProjectView(TemplateView):
    template_name = 'zeus/project.html'

    def get_project(self, project_name):
        return Project.objects.for_name(project_name)

    def get_context_data(self, **kwargs):
        data = super(ProjectView, self).get_context_data(**kwargs)
        data['project'] = self.get_project(kwargs['project_name'])
        data['settings'] = settings
        return data


project_view = ProjectView.as_view()

