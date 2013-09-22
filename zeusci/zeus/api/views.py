from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..conf import settings as zeus_settings
from ..models import Buildset
from ..models import Build
from ..models import Project
from .serializers import BuildsetSerializer
from .serializers import BuildDetailSerializer
from .serializers import ProjectDetailSerializer
from .serializers import ProjectSerializer
import time


class BaseApiMixin(object):
    pagination_serializer_class = zeus_settings.API_PAGINATION_SERIALIZER_CLASS
    paginate_by = zeus_settings.API_PAGINATE_BY

    def dispatch(self, *args, **kwargs):
        if settings.DEBUG and zeus_settings.API_DELAY:
            # TODO: note user (log) that API calls are artificially delayed
            time.sleep(zeus_settings.API_DELAY)
        return super(BaseApiMixin, self).dispatch(*args, **kwargs)


class ProjectList(BaseApiMixin, generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


project_list = ProjectList.as_view()


class ProjectDetail(BaseApiMixin, generics.RetrieveUpdateDestroyAPIView):
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



class BuildsetList(BaseApiMixin, BuildsetApiMixin, generics.ListCreateAPIView):
    pass

buildset_list = BuildsetList.as_view()


class BuildsetDetail(BaseApiMixin, BuildsetApiMixin, generics.RetrieveAPIView):
    pass

buildset_detail = BuildsetDetail.as_view()


class BuildDetail(BaseApiMixin, generics.RetrieveAPIView):
    serializer_class = BuildDetailSerializer
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

