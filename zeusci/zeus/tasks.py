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
def do_build_project(project):
    return build(project)

@task
def do_build(build, builder_cls):
    builder = builder_cls()
    print " -> Running build(%r, %r)" % (build, builder_cls)
    builder.build(build)

