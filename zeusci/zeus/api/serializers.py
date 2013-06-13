from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    uri = serializers.HyperlinkedIdentityField(
        view_name='zeus_api_project_detail',
        pk_url_kwarg='name',
        lookup_field='name',
    )
    name = serializers.CharField('name')
    project_url = serializers.CharField(source='url')
    repo_url = serializers.CharField('repo_url')

