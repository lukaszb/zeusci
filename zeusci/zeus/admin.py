from django.contrib import admin
from .models import Buildset
from .models import Build
from .models import Project


class BuildsetAdmin(admin.ModelAdmin):
    list_display = ['project', 'number']

admin.site.register(Buildset, BuildsetAdmin)


class BuildAdmin(admin.ModelAdmin):
    list_display = ['buildset', 'number']

admin.site.register(Build, BuildAdmin)


admin.site.register(Project)

