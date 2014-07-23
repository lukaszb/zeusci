from rest_framework import serializers
from .fields import HyperlinkedIdentityField
from zeusci.zeus.fields import bytes2str
from zeusci.zeus.models import Build
from zeusci.zeus.models import Buildset
from zeusci.zeus.models import Command
from zeusci.zeus.models import Project


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
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Build
        fields = base_build_fields
        read_only_fields = ['number', 'created_at', 'finished_at']


class CommandSerializer(serializers.ModelSerializer):
    output = serializers.CharField()
    status = serializers.CharField()
    cmd = serializers.CharField(source='get_cmd_string')

    class Meta:
        model = Command
        fields = ['number', 'title', 'cmd', 'output', 'started_at',
                  'finished_at', 'status', 'returncode']


class BuildDetailSerializer(BuildSerializer):
    commands = CommandSerializer(source='commands', read_only=True)

    class Meta:
        model = Build
        fields = base_build_fields + ['commands', 'status']
        read_only_fields = ['number', 'created_at', 'finished_at']


class BuildsetSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_buildset_detail',
        lookup_field={
            'buildset_no': 'number',
            'name': 'project__name',
        },
    )
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    number = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    finished_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(source='get_status', read_only=True)
    builds = BuildSerializer(source='builds', read_only=True)
    errors = serializers.SerializerMethodField('get_errors')
    branch = serializers.SlugField(required=False, default=None)

    def get_errors(self, obj):
        return [bytes2str(error.copy()) for error in obj.errors]

    class Meta:
        model = Buildset
        fields = [
            'uri',
            'url',
            'number',
            'created_at',
            'finished_at',
            'status',
            'builds',
            'errors',
            'branch',
        ]


class ProjectSerializer(serializers.ModelSerializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='zeus_api_project_detail',
        pk_url_kwarg='name',
        lookup_field='name',
    )
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    buildsets_uri = serializers.HyperlinkedIdentityField(
        view_name='zeus_api_buildset_list',
        pk_url_kwarg='name',
        lookup_field='name',
    )

    class Meta:
        model = Project
        fields = ['name', 'repo_url', 'uri', 'url', 'website_url', 'buildsets_uri']


class ProjectDetailSerializer(ProjectSerializer):
    buildsets_total_count = serializers.IntegerField(source='get_buildsets_total_count')
    buildsets_recent = BuildsetSerializer(source='get_recent_buildsets')

    class Meta:
        model = Project
        fields = ProjectSerializer.Meta.fields + [
            'buildsets_total_count',
            'buildsets_recent',
        ]

