from __future__ import unicode_literals
from .project import get_project_model
from .conf import settings
from .utils.general import abspath
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.core.cache import cache
import datetime
import jsonfield


Project = get_project_model()


class Build(models.Model):
    project = models.ForeignKey(Project)
    number = models.PositiveIntegerField()
    build_dir = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    finished_at = models.DateTimeField(null=True)
    info = jsonfield.JSONField()

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

    @property
    def build_steps_dir(self):
        return abspath(self.build_dir, 'steps')

    @property
    def build_repo_dir(self):
        return abspath(self.build_dir, 'repo')


class BuildStep(models.Model):
    build = models.ForeignKey(Build)
    number = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    finished_at = models.DateTimeField(null=True)
    options = jsonfield.JSONField()
    returncode = models.IntegerField(null=True)
    output_path = models.FilePathField(settings.BUILDS_OUTPUT_DIR, recursive=True)

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

    def get_force_build_url(self):
        kwargs = {
            'name': self.build.project.name,
            'build_no': self.build.number,
            'step_no': self.number,
        }
        return reverse_lazy('zeus_project_force_build_step', kwargs=kwargs)

    @property
    def duration(self):
        if self.created_at and self.finished_at:
            return self.finished_at - self.created_at

    @property
    def output(self):
        return open(self.output_path).read()

    @property
    def build_step_dir(self):
        return abspath(self.build.build_steps_dir, str(self.number))

    @property
    def build_step_repo_dir(self):
        return abspath(self.build_step_dir, 'repo')

    SUCCESS = 'success'
    PENDING = 'pending'
    FAIL = 'fail'

    @property
    def status(self):
        if self.finished_at and self.returncode == 0:
            return self.SUCCESS
        elif self.returncode is None:
            return self.PENDING
        else:
            return self.FAIL

    @classmethod
    def get_task_is_running_cache_key(pk):
        return 'zeus-ci-build-step-task-running-%s' % pk

    @property
    def task_is_running_cache_key(self):
        if not self.pk:
            raise ValueError("Only steps already stored at database can have "
                "task cache key")
        return BuildStep.get_task_cache_key(self.pk)

    def start_task(self, save=False):
        timeout = settings.BUILD_STEP_TIMEOUT
        cache.set(self.task_is_running_cache_key, 'yes', timeout=timeout)
        self.finished_at = None
        if save:
            self.save()

    def finish_task(self, save=False):
        cache.delete(self.task_is_running_cache_key)
        self.finished_at = datetime.datetime.now()
        if save:
            self.save()

    def is_task_running(self):
        return cache.get(self.task_is_running_cache_key) is not None

