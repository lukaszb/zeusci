from __future__ import unicode_literals
from django.db import models
from .conf import settings


class ProjectManager(models.Manager):

    def for_name(self, name):
        obj = self.model()
        obj.name = name
        attrs = ['url', 'repo_url']
        for attr in attrs:
            setattr(obj, attr, settings.PROJECTS[name].get(attr))
        return obj


class Project(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField()
    repo_url = models.CharField(max_length=512)

    objects = ProjectManager()

    def __str__(self):
        return self.name

    def setup(self, data):
        self.repo_url = data.get('repo_url')
        self.url = data.get('url')

