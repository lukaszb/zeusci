from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from .conf import settings
from .models import Build
from .models import Step
from .models import Project
from .tasks import build_project
from .tasks import build_step



class ProjectView(TemplateView):
    template_name = 'zeus/project.html'

    def get_project(self, name):
        return Project.objects.get(name=name)

    def get_context_data(self, **kwargs):
        data = super(ProjectView, self).get_context_data(**kwargs)
        data['project'] = self.get_project(kwargs['name'])
        data['settings'] = settings
        print data
        return data


project_view = ProjectView.as_view()


class ProjectBuildDetailView(TemplateView):
    template_name = 'zeus/project_build.html'

    def get_context_data(self, **kwargs):
        name = kwargs['name']
        build_no = kwargs['build_no']
        build = get_object_or_404(Build, project__name=name, number=build_no)
        data = super(ProjectBuildDetailView, self).get_context_data(**kwargs)
        data['project'] = build.project
        data['build'] = build
        return data

project_build_detail_view = ProjectBuildDetailView.as_view()


class ProjectStepDetailView(TemplateView):
    template_name = 'zeus/project_build_step.html'

    def get_context_data(self, **kwargs):
        name = kwargs['name']
        build_no = kwargs['build_no']
        step_no = kwargs['step_no']
        step = get_object_or_404(Step,
            build__project__name=name,
            build__number=build_no,
            number=step_no,
        )
        data = super(ProjectStepDetailView, self).get_context_data(**kwargs)
        data['project'] = step.build.project
        data['build'] = step.build
        data['step'] = step
        return data

project_build_step_detail_view = ProjectStepDetailView.as_view()


class ProjectBuildView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('zeus_project_detail', kwargs={'name': self.project.name})

    def get(self, request, name):
        self.project = get_object_or_404(Project, name=name)
        build_project.delay(self.project)
        return super(ProjectBuildView, self).get(request, name)

project_build_view = ProjectBuildView.as_view()


class ProjectBuildStepView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('zeus_project_build_step_detail', kwargs={
            'name': self.step.build.project.name,
            'build_no': self.step.build.number,
            'step_no': self.step.number,
        })

    def get(self, request, name, build_no, step_no):
        self.step = get_object_or_404(
            Step,
            build__project__name=name,
            build__number=build_no,
            number=step_no,
        )
        from .builders import PythonBuilder
        build_step.delay(self.step, PythonBuilder)
        return super(ProjectBuildStepView, self).get(request, name)

project_build_step_view = ProjectBuildStepView.as_view()

