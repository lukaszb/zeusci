from django.conf import settings


DEFAULTS = {
    'PROJECTS': {},
    'FOO': 'default-foobar',
}

USER_SETTINGS = getattr(settings, 'ZEUS_SETTINGS', None)


class ZeusSettings(object):

    def __init__(self, defaults=None, user_settings=None):
        self.defaults = defaults or {}
        self.user_settings = user_settings or {}
        self.settings = dict(self.defaults, **self.user_settings)

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid Zeus setting: %r' % attr)
        return self.settings[attr]


settings = ZeusSettings(DEFAULTS, USER_SETTINGS)

