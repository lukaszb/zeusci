from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import Build
from ..models import BuildStep
from ..models import Project
from .serializers import BuildSerializer
from .serializers import DetailBuildStepSerializer
from .serializers import ProjectDetailSerializer
from .serializers import ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


project_list = ProjectList.as_view()


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDetailSerializer
    model = Project
    lookup_field = 'name'

project_detail = ProjectDetail.as_view()


class BuildApiMixin(object):
    serializer_class = BuildSerializer
    model = Build

    def get_queryset(self):
        return Build.objects.filter(project__name=self.kwargs['name'])

    def get_object_filters(self):
        return {'number': self.kwargs['build_no']}

    def get_object(self):
        queryset = self.get_queryset()
        filters = self.get_object_filters()
        return get_object_or_404(queryset, **filters)



class BuildList(BuildApiMixin, generics.ListCreateAPIView):
    pass

build_list = BuildList.as_view()


class BuildDetail(BuildApiMixin, generics.RetrieveAPIView):
    pass

build_detail = BuildDetail.as_view()


class BuildStepDetail(generics.RetrieveAPIView):
    serializer_class = DetailBuildStepSerializer
    model = BuildStep

    def get_queryset(self):
        return BuildStep.objects.filter(build__project__name=self.kwargs['name'])

    def get_object_filters(self):
        return {
            'build__number': self.kwargs['build_no'],
            'number': self.kwargs['step_no'],
        }

    def get_object(self):
        queryset = self.get_queryset()
        filters = self.get_object_filters()
        return get_object_or_404(queryset, **filters)


build_step_detail = BuildStepDetail.as_view()

