from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse_lazy
from .conf import settings
import datetime
import jsonfield


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

    def get_absolute_url(self):
        return reverse_lazy('zeus_project_detail', kwargs={'name': self.name})

    def setup(self, data):
        self.repo_url = data.get('repo_url')
        self.url = data.get('url')


class Build(models.Model):
    project = models.ForeignKey(Project)
    number = models.PositiveIntegerField()
    build_dir = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    finished_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('project', 'number')
        ordering = ['-created_at']

    def __str__(self):
        return '%s | %s' % (self.project, self.number)

    def save(self, *args, **kwargs):
        if not self.number:
            try:
                newest = Build.objects.filter(project=self.project
                    ).order_by('-number')[0]
                self.number = newest.number + 1
            except IndexError:
                self.number = 1
        super(Build, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {'name': self.project.name, 'build_no': self.number}
        return reverse_lazy('zeus_project_build_detail', kwargs=kwargs)

    @property
    def duration(self):
        if self.created_at and self.finished_at:
            return self.finished_at - self.created_at


class BuildStep(models.Model):
    build = models.ForeignKey(Build)
    number = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    finished_at = models.DateTimeField(null=True)
    options = jsonfield.JSONField()

    class Meta:
        unique_together = ('build', 'number')
        ordering = ['-number']

    def __str__(self):
        return '%s.%s' % (self.build, self.number)

    def get_absolute_url(self):
        kwargs = {
            'name': self.build.project.name,
            'build_no': self.build.number,
            'step_no': self.number,
        }
        return reverse_lazy('zeus_project_build_step_detail', kwargs=kwargs)

    @property
    def duration(self):
        if self.created_at and self.finished_at:
            return self.finished_at - self.created_at

