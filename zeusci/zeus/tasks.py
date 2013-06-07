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
    return project

