from django.contrib import admin
from .models import Build
from .models import Step
from .models import Project


class BuildAdmin(admin.ModelAdmin):
    list_display = ['project', 'number']

admin.site.register(Build, BuildAdmin)


class StepAdmin(admin.ModelAdmin):
    list_display = ['build', 'number']

admin.site.register(Step, StepAdmin)


admin.site.register(Project)

