from __future__ import unicode_literals
from celery import task
import inspect


@task
def do_build_project(project, branch=None):
    builder = project.get_builder()
    builder.build_project(project, branch=branch)


@task
def do_buildset(buildset):
    builder = buildset.project.get_builder()
    builder.run_buildset(buildset)


@task
def do_build(build, builder):
    if inspect.isclass(builder):
        builder = builder()
    builder.build(build)
