from rest_framework import serializers
from .fields import HyperlinkedIdentityField
from zeus.models import Build


base_build_fields = [
    'uri',
    'url',
    'number',
    'created_at',
    'finished_at',
    'returncode',
    'status',
]

class BuildSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_build_detail',
        lookup_field={
            'build_no': 'number',
            'buildset_no': 'buildset__number',
            'name': 'buildset__project__name',
        },
    )
    url = serializers.CharField(source='get_absolute_url')
    status = serializers.CharField()
    class Meta:
        model = Build
        fields = base_build_fields


class BuildDetailSerializer(BuildSerializer):
    output = serializers.CharField()
    class Meta:
        model = Build
        fields = base_build_fields + ['output', 'status']


class BuildsetSerializer(serializers.Serializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_buildset_detail',
        lookup_field={
            'buildset_no': 'number',
            'name': 'project__name',
        },
    )
    url = serializers.CharField(source='get_absolute_url')
    number = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    finished_at = serializers.DateTimeField()
    status = serializers.CharField(source='get_status')
    builds = BuildSerializer(source='builds')


class ProjectSerializer(serializers.Serializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='zeus_api_project_detail',
        pk_url_kwarg='name',
        lookup_field='name',
    )
    name = serializers.CharField('name')
    website_url = serializers.CharField(source='url')
    repo_url = serializers.CharField('repo_url')
    project_url = serializers.CharField(source='get_absolute_url')
    buildsets_uri = serializers.HyperlinkedIdentityField(
        view_name='zeus_api_buildset_list',
        pk_url_kwarg='name',
        lookup_field='name',
    )


class ProjectDetailSerializer(ProjectSerializer):
    buildsets_total_count = serializers.IntegerField(source='get_buildsets_total_count')
    buildsets_recent = BuildsetSerializer(source='get_recent_buildsets')

