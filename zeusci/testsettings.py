import os
import random
import string

DEBUG = False

INSTALLED_APPS = (
    'zeusci.zeus',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
    },
}

SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'tests', 'templates'),
)

# this is for tests only so we don't care if it's regenerated
SECRET_KEY = ''.join([random.choice(string.ascii_letters) for x in range(40)])

ROOT_URLCONF = 'zeusci.zeus.tests.urls'

