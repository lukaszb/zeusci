from django.contrib import admin
from .models import Build
from .models import BuildStep
from .models import Project


class BuildAdmin(admin.ModelAdmin):
    list_display = ['project', 'number']

admin.site.register(Build, BuildAdmin)


class BuildStepAdmin(admin.ModelAdmin):
    list_display = ['build', 'number']

admin.site.register(BuildStep, BuildStepAdmin)


admin.site.register(Project)

