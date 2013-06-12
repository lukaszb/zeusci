from __future__ import unicode_literals
from .builders import build
from .models import BuildStep
from celery import task
import time


@task()
def add(x, y):
    return x + y

@task()
def mul(x, y):
    time.sleep(3)
    return x * y

@task
def build_project(project):
    return build(project)

@task
def build_step(builder, build, step_no, env):
    step = BuildStep.objects.create(build=build, number=step_no)
    builder.build_step(step, env)

@task
def some_task():
    print('foobar')



