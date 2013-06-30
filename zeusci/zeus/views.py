from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from .conf import settings
from .models import Buildset
from .models import Build
from .models import Project
from .tasks import do_build_project
from .tasks import do_build



class ProjectView(TemplateView):
    template_name = 'zeus/project.html'

    def get_project(self, name):
        return Project.objects.get(name=name)

    def get_context_data(self, **kwargs):
        data = super(ProjectView, self).get_context_data(**kwargs)
        data['project'] = self.get_project(kwargs['name'])
        data['settings'] = settings
        return data


project_view = ProjectView.as_view()


class ProjectBuildsetDetailView(TemplateView):
    template_name = 'zeus/project_buildset.html'

    def get_context_data(self, **kwargs):
        name = kwargs['name']
        buildset_no = kwargs['buildset_no']
        buildset = get_object_or_404(Buildset, project__name=name, number=buildset_no)
        data = super(ProjectBuildsetDetailView, self).get_context_data(**kwargs)
        data['project'] = buildset.project
        data['buildset'] = buildset
        return data

project_buildset_detail_view = ProjectBuildsetDetailView.as_view()


class ProjectBuildDetailView(TemplateView):
    template_name = 'zeus/project_build.html'

    def get_context_data(self, **kwargs):
        print " ----> build detail"
        name = kwargs['name']
        buildset_no = kwargs['buildset_no']
        build_no = kwargs['build_no']
        build = get_object_or_404(Build,
            buildset__project__name=name,
            buildset__number=buildset_no,
            number=build_no,
        )
        data = super(ProjectBuildDetailView, self).get_context_data(**kwargs)
        data['project'] = build.buildset.project
        data['buildset'] = build.buildset
        data['build'] = build
        return data

project_build_detail_view = ProjectBuildDetailView.as_view()


class ProjectBuildsetView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('zeus_project_detail', kwargs={'name': self.project.name})

    def get(self, request, name):
        self.project = get_object_or_404(Project, name=name)
        do_build_project.delay(self.project)
        return super(ProjectBuildsetView, self).get(request, name)

project_buildset_view = ProjectBuildsetView.as_view()


class ProjectBuildsetBuildView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('zeus_project_build_detail', kwargs={
            'name': self.build.buildset.project.name,
            'buildset_no': self.build.buildset.number,
            'build_no': self.build.number,
        })

    def get(self, request, name, buildset_no, build_no):
        self.build = get_object_or_404(
            Build,
            buildset__project__name=name,
            buildset__number=buildset_no,
            number=build_no,
        )
        from .builders import PythonBuildseter
        do_build.delay(self.build, PythonBuildseter)
        self.build.clear_output()
        return super(ProjectBuildsetBuildView, self).get(request, name)

project_build_view = ProjectBuildsetBuildView.as_view()

