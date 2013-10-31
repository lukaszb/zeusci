import os


abspath = lambda *p: os.path.abspath(os.path.join(*p))

PROJECT_ROOT = abspath(os.path.dirname(__file__), '..')
VAR_DIR = abspath(PROJECT_ROOT, '..', 'var')

print(" => PROJECT_ROOT: %r" % PROJECT_ROOT)
print(" => VAR_DIR: %r" % VAR_DIR)



DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': abspath(PROJECT_ROOT, '.database.sqlite'),
    }
}

ALLOWED_HOSTS = ['127.0.0.1']

TIME_ZONE = 'Europe/Warsaw' # zeus-ci is build in Warsaw, Poland

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = False

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    abspath(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '=(30104+(w5^ge&&(+rdfk*!8)li)5k&@(74pws6a(3d_s=8rh'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zeusapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'zeusapp.wsgi.application'

TEMPLATE_DIRS = (
    abspath(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Externals
    'django_extensions',
    'djcelery',
    'gunicorn',
    'rest_framework',
    'compressor',

    # Internals
    'zeusci.zeus',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


# =============================================================================
# Celery
# =============================================================================
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

import djcelery
djcelery.setup_loader()


# =============================================================================
# REST
# =============================================================================
REST_FRAMEWORK = {
    'PAGINATE_BY': 20,
}

# =============================================================================
# Zeus
# =============================================================================

ZEUS_SETTINGS= {
    #'PROJECTS': {
        #'frogress': {
            #'repo_url': 'git://github.com/lukaszb/frogress.git',
            #'url': 'https://github.com/lukaszb/frogress',
        #},
    #},
    'BUILDS_ROOT': abspath(VAR_DIR, 'builds'),
    'REMOVE_BUILD_DIRS': False,
    'PROJECT_BUILDSETS_COUNT': 10,
    'API_DELAY': 0.0,
}


# django-nose
#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
#TEST_RUNNER = 'django_pytest.test_runner.TestRunner'
TEST_RUNNER = 'discover_runner.DiscoverRunner'


TESTING = os.environ.get('TESTING', False)
if TESTING:
    from test_settings import update_settings_for_tests
    update_settings_for_tests(locals())


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

