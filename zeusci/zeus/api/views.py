from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import Build
from ..models import Project
from .serializers import BuildSerializer
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

    def get_object(self):
        queryset = self.get_queryset()
        filters = {'number': self.kwargs['build_no']}
        return get_object_or_404(queryset, **filters)



class BuildList(BuildApiMixin, generics.ListCreateAPIView):
    pass

build_list = BuildList.as_view()


class BuildDetail(BuildApiMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

build_detail = BuildDetail.as_view()

