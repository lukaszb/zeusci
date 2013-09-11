import os

abspath = lambda *p: os.path.abspath(os.path.join(*p))

PROJECT_ROOT = abspath(os.path.dirname(__file__), '..')
VAR_DIR = abspath(PROJECT_ROOT, '..', 'var')
print " => PROJECT_ROOT: %r" % PROJECT_ROOT
print " => VAR_DIR: %r" % VAR_DIR


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Lukasz', 'lukaszbalcerzak@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': abspath(PROJECT_ROOT, '.database.sqlite'),
        #'USER': '',
        #'PASSWORD': '',
        #'HOST': '',
        #'PORT': '',
    }
}

ALLOWED_HOSTS = ['*'] # XXX: for development

TIME_ZONE = 'Europe/Warsaw'
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
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = '6s-*u$$jlc7(g-3wh74s0rx6c1^-*(u%r=%v)rak33&eah3#-)'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    abspath(PROJECT_ROOT, 'templates')
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zeusci.urls'
WSGI_APPLICATION = 'zeusci.wsgi.application'

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
    'compressor',
    'djcelery',
    'gunicorn',
    'django_nose',
    'rest_framework',

    # Internals
    'zeusci',
    'zeus',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'socketio': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
    }
}


# =============================================================================
# Cache
# =============================================================================
CACHES = {
    'default': {
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'LOCATION': 'some-unique-flake',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'zeus-ci',
    }
}


# =============================================================================
# Celery
# =============================================================================
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

import djcelery
djcelery.setup_loader()


# =============================================================================
# Compressor
# =============================================================================
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
)
COMPRESS_OUTPUT_DIR = '.compressor-cache'
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/x-sass', 'sass {infile} {outfile} -C'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

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
}


# django-nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


TESTING = os.environ.get('TESTING', False)
if TESTING:
    from test_settings import update_settings_for_tests
    update_settings_for_tests(locals())

