from django.contrib import admin
from .models import Build
from .models import Project


class BuildAdmin(admin.ModelAdmin):
    list_display = ['project', 'number']

admin.site.register(Build, BuildAdmin)


admin.site.register(Project)

