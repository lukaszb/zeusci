from rest_framework import serializers
from .fields import HyperlinkedIdentityField


class BuildSerializer(serializers.Serializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_build_detail',
        lookup_field={
            'build_no': 'number',
            'name': 'project__name',
        },
    )


class ProjectSerializer(serializers.Serializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='zeus_api_project_detail',
        pk_url_kwarg='name',
        lookup_field='name',
    )
    name = serializers.CharField('name')
    project_url = serializers.CharField(source='url')
    repo_url = serializers.CharField('repo_url')


class ProjectDetailSerializer(ProjectSerializer):
    builds = BuildSerializer(source='get_builds')

