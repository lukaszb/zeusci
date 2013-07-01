from django.db import models
from django.core.urlresolvers import reverse_lazy
from .utils.imports import import_class
from .conf import settings


class Project(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField()
    repo_url = models.CharField(max_length=512)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('zeus_project_detail', kwargs={'name': self.name})

    def setup(self, data):
        self.repo_url = data.get('repo_url')
        self.url = data.get('url')

    def get_buildsets(self):
        buildsets = self.buildsets.all().order_by('-number')
        if settings.PROJECT_BUILDSETS_COUNT:
            buildsets = buildsets[:settings.PROJECT_BUILDSETS_COUNT]
        return buildsets


def get_project_model():
    return import_class(settings.PROJECT_MODEL)

