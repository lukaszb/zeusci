from rest_framework import generics
from ..models import Project
from .serializers import ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


project_list = ProjectList.as_view()


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    model = Project
    lookup_field = 'name'

project_detail = ProjectDetail.as_view()

