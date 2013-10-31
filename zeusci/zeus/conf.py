from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .utils.general import abspath
from .utils.imports import import_class
import os
import tempfile


DEFAULTS = {
    'PROJECTS': {},
    'BUILDS_ROOT': tempfile.gettempdir(),
    'BUILDS_OUTPUT_DIR': None,
    'PROJECT_MODEL': 'zeus.project.Project',
    'REMOVE_BUILD_DIRS': True,
    'FOO': 'default-foobar',
    'PROJECT_BUILDSETS_COUNT': 10,
    'API_PAGINATION_SERIALIZER_CLASS': 'rest_framework.pagination.PaginationSerializer',
    'API_PAGINATE_BY': 20,
    'API_DELAY': None, # delay in seconds to all api calls
    'COMMAND_EXECUTION_BACKEND': 'zeusci.procme.Command',
    'COMMAND_TIMEOUT': 60 * 60,
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    'API_PAGINATION_SERIALIZER_CLASS',
    'COMMAND_EXECUTION_BACKEND',
]

USER_SETTINGS = getattr(settings, 'ZEUS_SETTINGS', None)


class ZeusSettings(object):

    def __init__(self, defaults=None, user_settings=None):
        self.defaults = defaults or {}
        self.user_settings = user_settings or {}
        self.settings = dict(self.defaults, **self.user_settings)
        self.verify()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid Zeus setting: %r' % attr)
        value = self.settings[attr]
        if attr in IMPORT_STRINGS:
            return import_class(value)
        return value

    def verify(self):
        if 'BUILDS_ROOT' not in self.settings:
            raise ImproperlyConfigured('Zeus requires BUILDS_ROOT setting')
        try:
            os.makedirs(self.BUILDS_ROOT)
        except OSError as error:
            if error.errno != 17: # 17 is: directory exist
                raise
        if self.settings['BUILDS_OUTPUT_DIR'] is None:
            self.settings['BUILDS_OUTPUT_DIR'] = abspath(
                self.settings['BUILDS_ROOT'], 'outputs')


settings = ZeusSettings(DEFAULTS, USER_SETTINGS)

