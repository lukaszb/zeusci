from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from .models import Buildset
from .models import Build
from .models import Command
from .models import Project
from .tasks import do_build_project
from .tasks import do_build
from .api.serializers import ProjectDetailSerializer
from .api.serializers import BuildsetSerializer
from .api.serializers import BuildDetailSerializer
import datetime


class ProjectNoContextView(TemplateView):
    template_name = 'zeus/project.html'


project_list_view = ProjectNoContextView.as_view()
project_create_view = ProjectNoContextView.as_view()


class ProjectView(TemplateView):
    template_name = 'zeus/project.html'

    def get_project(self, name):
        return Project.objects.get(name=name)

    def get_context_data(self, **kwargs):
        data = super(ProjectView, self).get_context_data(**kwargs)
        project = self.get_project(kwargs['name'])
        data['project'] = ProjectDetailSerializer(project).data
        return data


project_view = ProjectView.as_view()


class ProjectBuildsetDetailView(TemplateView):
    template_name = 'zeus/project_buildset.html'

    def get_context_data(self, **kwargs):
        name = kwargs['name']
        buildset_no = kwargs['buildset_no']
        buildset = get_object_or_404(Buildset, project__name=name, number=buildset_no)
        data = super(ProjectBuildsetDetailView, self).get_context_data(**kwargs)
        data['project'] = ProjectDetailSerializer(buildset.project).data
        data['buildset'] = BuildsetSerializer(buildset).data
        return data

project_buildset_detail_view = ProjectBuildsetDetailView.as_view()


class ProjectBuildDetailView(TemplateView):
    template_name = 'zeus/project_build.html'

    def get_context_data(self, **kwargs):
        print(" ----> build detail")
        name = kwargs['name']
        buildset_no = kwargs['buildset_no']
        build_no = kwargs['build_no']
        build = get_object_or_404(Build,
            buildset__project__name=name,
            buildset__number=buildset_no,
            number=build_no,
        )
        data = super(ProjectBuildDetailView, self).get_context_data(**kwargs)
        data['project'] = ProjectDetailSerializer(build.buildset.project).data
        data['buildset'] = BuildsetSerializer(build.buildset).data
        data['build'] = BuildDetailSerializer(build).data
        from zeusci.zeus.templatetags.zeus import jsonify
        data['build_init_json'] = jsonify('init(' + jsonify(data['build']) + ')')
        data['force_build_url'] = build.get_force_build_url()
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
        self.build.created_at = datetime.datetime.now()
        self.build.save(force_update=True, update_fields=['created_at'])
        Command.objects.filter(build=self.build).delete()

        self.build.finished_at = None
        self.build.save()

        from .builders import PythonBuilder
        do_build.delay(self.build, PythonBuilder)
        self.build.clear_output()
        return super(ProjectBuildsetBuildView, self).get(request, name)

project_build_view = ProjectBuildsetBuildView.as_view()

