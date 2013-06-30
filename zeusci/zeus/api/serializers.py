from rest_framework import serializers
from .fields import HyperlinkedIdentityField
from zeus.models import Build


base_build_fields = ['uri', 'number', 'created_at', 'finished_at', 'returncode']

class BuildSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_build_detail',
        lookup_field={
            'build_no': 'number',
            'buildset_no': 'buildset__number',
            'name': 'buildset__project__name',
        },
    )
    class Meta:
        model = Build
        fields = base_build_fields


class DetailBuildSerializer(BuildSerializer):
    output = serializers.CharField()
    class Meta:
        model = Build
        fields = base_build_fields + ['output']


class BuildsetSerializer(serializers.Serializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_buildset_detail',
        lookup_field={
            'buildset_no': 'number',
            'name': 'project__name',
        },
    )
    builds = BuildSerializer(source='builds')


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
    buildsets = BuildsetSerializer(source='get_buildsets')

