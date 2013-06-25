from rest_framework import serializers
from .fields import HyperlinkedIdentityField
from zeus.models import BuildStep


base_build_step_fields = ['uri', 'number', 'created_at', 'finished_at', 'returncode']
class BuildStepSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_build_step_detail',
        lookup_field={
            'step_no': 'number',
            'build_no': 'build__number',
            'name': 'build__project__name',
        },
    )
    class Meta:
        model = BuildStep
        fields = base_build_step_fields


class DetailBuildStepSerializer(BuildStepSerializer):
    output = serializers.CharField()
    class Meta:
        model = BuildStep
        fields = base_build_step_fields + ['output']


class BuildSerializer(serializers.Serializer):
    uri = HyperlinkedIdentityField(
        view_name='zeus_api_build_detail',
        lookup_field={
            'build_no': 'number',
            'name': 'project__name',
        },
    )
    steps = BuildStepSerializer(source='steps')


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

