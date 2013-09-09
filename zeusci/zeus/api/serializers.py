from rest_framework import serializers
from .fields import HyperlinkedIdentityField
from zeus.models import Build
from zeus.models import Command


base_build_fields = [
    'uri',
    'url',
    'number',
    'created_at',
    'finished_at',
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


class CommandSerializer(serializers.ModelSerializer):
    output = serializers.CharField()
    status = serializers.CharField()
    cmd = serializers.CharField(source='get_cmd_string')

    class Meta:
        model = Command
        fields = ['number', 'title', 'cmd', 'output', 'started_at',
                  'finished_at', 'status', 'returncode']


class BuildDetailSerializer(BuildSerializer):
    commands = CommandSerializer(source='commands')

    class Meta:
        model = Build
        fields = base_build_fields + ['commands', 'status']


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
    url = serializers.CharField(source='get_absolute_url')
    buildsets_uri = serializers.HyperlinkedIdentityField(
        view_name='zeus_api_buildset_list',
        pk_url_kwarg='name',
        lookup_field='name',
    )


class ProjectDetailSerializer(ProjectSerializer):
    buildsets_total_count = serializers.IntegerField(source='get_buildsets_total_count')
    buildsets_recent = BuildsetSerializer(source='get_recent_buildsets')

