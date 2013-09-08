from __future__ import unicode_literals
from celery import task
import inspect


@task
def do_build_project(project):
    builder = project.get_builder()
    builder.build_project(project)


@task
def do_build(build, builder):
    if inspect.isclass(builder):
        builder = builder()
    builder.build(build)

