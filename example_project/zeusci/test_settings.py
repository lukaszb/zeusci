
def update_settings_for_tests(settings):
    settings['PASSWORD_HASHERS'] = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
    )
    settings['DATABASES'] = {
        'default': {
            'NAME': ':memory:',
            'ENGINE': 'django.db.backends.sqlite3',
        },
    }
    settings['USE_TZ'] = False

    settings['CELERY_ALWAYS_EAGER'] = True

