from __future__ import unicode_literals
from .project import get_project_model
from .utils.general import abspath
from django.db import models
from django.core.urlresolvers import reverse
from django.core.cache import cache
import datetime
import jsonfield


PENDING = 'pending'
RUNNING = 'running'
PASSED = 'passed'
FAILED = 'failed'

Project = get_project_model()


class Buildset(models.Model):
    project = models.ForeignKey(Project, related_name='buildsets')
    number = models.PositiveIntegerField()
    build_dir = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    finished_at = models.DateTimeField(null=True)
    info = jsonfield.JSONField()

    class Meta:
        unique_together = ('project', 'number')
        ordering = ['-number']

    def __str__(self):
        return '%s | %s' % (self.project, self.number)

    def save(self, *args, **kwargs):
        if not self.number:
            try:
                newest = Buildset.objects.filter(project=self.project
                    ).order_by('-number')[0]
                self.number = newest.number + 1
            except IndexError:
                self.number = 1
        super(Buildset, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {'name': self.project.name, 'buildset_no': self.number}
        return reverse('zeus_project_buildset_detail', kwargs=kwargs)

    @property
    def duration(self):
        if self.created_at and self.finished_at:
            return self.finished_at - self.created_at

    @property
    def builds_dir(self):
        return abspath(self.build_dir, 'builds')

    @property
    def build_repo_dir(self):
        return abspath(self.build_dir, 'repo')

    def get_status(self):
        builds = self.builds.all()
        if not builds:
            # no builds yet, most propably not yet created
            return PENDING
        for build in builds:
            if build.status == FAILED:
                return FAILED
            elif build.status == PENDING:
                return PENDING
        return PASSED


class Build(models.Model):
    buildset = models.ForeignKey(Buildset, related_name='builds')
    number = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    finished_at = models.DateTimeField(null=True)
    options = jsonfield.JSONField()
    build_output = models.OneToOneField('Output', null=True, blank=True,
        related_name='build')

    class Meta:
        unique_together = ('buildset', 'number')
        ordering = ['number']

    def __str__(self):
        return '%s.%s' % (self.buildset, self.number)

    def _get_url_kwargs(self):
        return {
            'name': self.buildset.project.name,
            'buildset_no': self.buildset.number,
            'build_no': self.number,
        }

    def get_absolute_url(self):
        kwargs = self._get_url_kwargs()
        return reverse('zeus_project_build_detail', kwargs=kwargs)

    def get_force_build_url(self):
        kwargs = self._get_url_kwargs()
        return reverse('zeus_force_project_build', kwargs=kwargs)

    @property
    def duration(self):
        if self.created_at and self.finished_at:
            return self.finished_at - self.created_at

    @property
    def build_dir(self):
        return abspath(self.buildset.builds_dir, str(self.number))

    @property
    def build_repo_dir(self):
        return abspath(self.build_dir, 'repo')

    @property
    def status(self):
        commands = self.get_commands()
        statuses = set(command.status for command in commands)
        if not statuses or statuses == set([PENDING]):
            return PENDING
        if FAILED in statuses:
            return FAILED
        if RUNNING in statuses:
            return RUNNING
        if statuses == set([PASSED]):
            return PASSED

    def is_finished(self):
        return self.status in set([FAILED, PASSED])

    def get_commands(self):
        if not hasattr(self, '_commands_cache'):
            self._commands_cache = self.commands.all()
        return self._commands_cache

    @property
    def cache_key_output(self):
        return 'zeus-build-output-%s' % self.pk

    @property
    def output(self):
        output = cache.get(self.cache_key_output)
        if output is None:
            if self.build_output is not None:
                output = self.build_output.output
            else:
                output = ''
            cache.set(self.cache_key_output, output)
        return output

    def clear_output(self):
        Output.objects.filter(build=self).update(output='')
        self.clear_output_cache()

    def clear_output_cache(self):
        cache.delete(self.cache_key_output)


class Command(models.Model):
    build = models.ForeignKey(Build, related_name='commands')
    number = models.PositiveIntegerField()
    command_output = models.OneToOneField('Output', null=True, blank=True,
        related_name='command')
    cmd = jsonfield.JSONField(default=list)
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    returncode = models.IntegerField(null=True)

    @property
    def status(self):
        if self.started_at is None:
            return PENDING
        elif self.returncode is None:
            return RUNNING
        elif self.returncode == 0:
            return PASSED
        else:
            return FAILED

    @property
    def cache_key_output(self):
        return 'zeus-build-command-output-%s' % self.pk

    @property
    def output(self):
        output = cache.get(self.cache_key_output)
        if output is None:
            if self.command_output is not None:
                output = self.command_output.output
            else:
                output = ''
            cache.set(self.cache_key_output, output)
        return output

    def clear_output(self):
        Output.objects.filter(command=self).update(output='')
        self.clear_output_cache()

    def clear_output_cache(self):
        cache.delete(self.cache_key_output)

    def get_cmd_string(self):
        return ' '.join(self.cmd)


class Output(models.Model):
    output = models.TextField()

    def __repr__(self):
        return "<Output: %r>" % self.build

