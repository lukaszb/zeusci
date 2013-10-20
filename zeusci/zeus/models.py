from __future__ import unicode_literals
from .project import get_project_model
from .utils.choices import Choices
from .utils.general import abspath
from django.db import models
from django.core.urlresolvers import reverse
from django.core.cache import cache
import datetime
import jsonfield


Project = get_project_model()


Status = Choices(
    PENDING='pending',
    RUNNING='running',
    PASSED='passed',
    FAILED='failed',
)


class Buildset(models.Model):
    project = models.ForeignKey(Project, related_name='buildsets')
    number = models.PositiveIntegerField()
    build_dir = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    finished_at = models.DateTimeField(null=True)
    info = jsonfield.JSONField()
    errors = jsonfield.JSONField(default=list)
    branch = models.SlugField(max_length=64, null=True)

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
        if self.errors:
            return Status.FAILED
        builds = self.builds.all()
        if not builds:
            # no builds yet, most propably not yet created
            return Status.PENDING
        for build in builds:
            if build.status == Status.FAILED:
                return Status.FAILED
            elif build.status == Status.PENDING:
                return Status.PENDING
        return Status.PASSED


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
        status = Status.PENDING
        if not statuses or statuses == set([Status.PENDING]):
            status = Status.PENDING
        elif Status.FAILED in statuses:
            status = Status.FAILED
        elif Status.RUNNING in statuses:
            status = Status.RUNNING
        elif statuses == set([Status.PASSED]):
            status = Status.PASSED
        return status

    def is_finished(self):
        # if is pending it's probably not started yet
        return self.status in set([Status.FAILED, Status.PASSED])

    def get_commands(self):
        return self.commands.all()

    def clear_output(self):
        command_ids = self.get_commands().values_list('id', flat=True)
        Output.objects.filter(command__id__in=command_ids).update(output='')
        for command_id in command_ids:
            Command.clear_output_cache_for(command_id)


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
    status = models.CharField(max_length=64, choices=Status.as_dict().items(),
        default=Status.PENDING)

    @classmethod
    def get_cache_key_output(cls, pk):
        return 'zeus-build-command-output-%s' % pk

    @property
    def cache_key_output(self):
        return self.__class__.get_cache_key_output(self.pk)

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

    @classmethod
    def clear_output_cache_for(cls, pk):
        key = cls.get_cache_key_output(pk)
        cache.delete(key)

    def clear_output_cache(self):
        self.__class__.clear_output_cache_for(self.pk)

    def get_cmd_string(self):
        return ' '.join(self.cmd)


class Output(models.Model):
    output = models.TextField()

    def __repr__(self):
        return "<Output: %r>" % self.command

