from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from ..conf import settings as zeus_settings
from ..models import Buildset
from ..models import Build
from ..models import Command
from ..models import Project
from ..tasks import do_build
from .exceptions import ConflictError
from .serializers import BuildsetSerializer
from .serializers import BuildDetailSerializer
from .serializers import ProjectDetailSerializer
from .serializers import ProjectSerializer
from ..tasks import do_build_project
import datetime
import time


class BaseApiMixin(object):
    pagination_serializer_class = zeus_settings.API_PAGINATION_SERIALIZER_CLASS
    paginate_by = zeus_settings.API_PAGINATE_BY

    def dispatch(self, *args, **kwargs):
        if settings.DEBUG and zeus_settings.API_DELAY:
            # TODO: note user (log) that API calls are artificially delayed
            time.sleep(zeus_settings.API_DELAY)
        return super(BaseApiMixin, self).dispatch(*args, **kwargs)


class BaseViewSet(BaseApiMixin, ModelViewSet):
    pass


# ==============================================================================
# Project
# ==============================================================================

class ProjectViewSet(BaseViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


project_list = ProjectViewSet.as_view({'get': 'list', 'post': 'create'})


class ProjectDetail(BaseApiMixin, generics.RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    model = Project
    lookup_field = 'name'


project_detail = ProjectDetail.as_view()

# ==============================================================================
# Buildset
# ==============================================================================

class BuildsetViewSet(BaseViewSet):
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

    def new(self, request, *args, **kwargs):
        project = Project.objects.get(name=self.kwargs['name'])
        do_build_project.delay(project, branch=request.DATA.get('branch'))
        # TODO: At this point we should have our new buildset already created -
        # otherwise we respond with 201 but no object was created yet and if
        # celery task fails then user was prematurely informed about success of
        # this action; Also, we should return ID of created object
        return Response({}, status=HTTP_201_CREATED)


buildset_list = BuildsetViewSet.as_view({
    'get': 'list',
    'post': 'new',
})

buildset_detail = BuildsetViewSet.as_view({
    'get': 'retrieve',
})


# ==============================================================================
# Build
# ==============================================================================

class BuildViewSet(BaseViewSet):
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
        if not hasattr(self, '_build'):
            queryset = self.get_queryset()
            filters = self.get_object_filters()
            self._build = get_object_or_404(queryset, **filters)
        return self._build

    def update(self, request, *args, **kwargs):
        """
        Actually **restarts** a build *in place* - it doesn't create new build
        and the information for current build is lost.
        """
        build = self.get_object()
        build.clear_output()
        if not build.is_finished():
            raise ConflictError('Build is still running and cannot be restarted')
        Command.objects.filter(build=build).delete()
        build.created_at = datetime.datetime.now()
        build.finished_at = None
        build.save(force_update=True)

        from ..builders import PythonBuilder
        do_build.delay(build, PythonBuilder)
        return super(BuildViewSet, self).retrieve(request, *args, **kwargs)


build_detail = BuildViewSet.as_view({'get': 'retrieve', 'put': 'update'})

