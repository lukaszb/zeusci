from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import Buildset
from ..models import Build
from ..models import Project
from .serializers import BuildsetSerializer
from .serializers import DetailBuildSerializer
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


class BuildsetApiMixin(object):
    serializer_class = BuildsetSerializer
    model = Buildset

    def get_queryset(self):
        return Buildset.objects.filter(project__name=self.kwargs['name'])

    def get_object_filters(self):
        return {'number': self.kwargs['buildset_no']}

    def get_object(self):
        queryset = self.get_queryset()
        filters = self.get_object_filters()
        return get_object_or_404(queryset, **filters)



class BuildsetList(BuildsetApiMixin, generics.ListCreateAPIView):
    pass

buildset_list = BuildsetList.as_view()


class BuildsetDetail(BuildsetApiMixin, generics.RetrieveAPIView):
    pass

buildset_detail = BuildsetDetail.as_view()


class BuildDetail(generics.RetrieveAPIView):
    serializer_class = DetailBuildSerializer
    model = Build

    def get_queryset(self):
        return Build.objects.filter(buildset__project__name=self.kwargs['name'])

    def get_object_filters(self):
        return {
            'buildset__number': self.kwargs['buildset_no'],
            'number': self.kwargs['build_no'],
        }

    def get_object(self):
        queryset = self.get_queryset()
        filters = self.get_object_filters()
        return get_object_or_404(queryset, **filters)


build_detail = BuildDetail.as_view()

