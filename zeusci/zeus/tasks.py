from __future__ import unicode_literals
from .builders import build
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
def build_step(builder, step):
    step.start_task()
    builder.build_step(step)
    step.finish_task(save=True)

