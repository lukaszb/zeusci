from django.conf import settings
from django.core.management import call_command
from django.core.management.base import NoArgsCommand
import os
import shutil


def rm_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


class Command(NoArgsCommand):

    def handle(self, **options):
        rm_if_exists(settings.VAR_DIR)
        rm_if_exists(settings.DATABASES['default']['NAME'])
        call_command('data')

