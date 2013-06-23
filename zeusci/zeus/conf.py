from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .utils.general import abspath
import os
import tempfile


DEFAULTS = {
    'PROJECTS': {},
    'BUILDS_ROOT': tempfile.gettempdir(),
    'BUILDS_OUTPUT_DIR': None,
    'PROJECT_MODEL': 'zeus.project.Project',
    'REMOVE_BUILD_DIRS': True,
    'FOO': 'default-foobar',
}

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
        return self.settings[attr]

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

