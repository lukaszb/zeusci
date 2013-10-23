.. _integration:

Integration with existing Django project
========================================

This document describes how to include ``zeus-ci`` into existing Django
project. It assumes user knows how to manage Django project and is familiar
with it's basic concepts.


.. note::
   Make sure you have ``zeus-ci`` Python package already installed::

      $ pip install zeusci


Add zeus to INSTALLED_APPS
--------------------------

Include ``zeusci.zeus`` in ``INSTALLED_APPS`` at ``settings.py`` file::

    INSTALLED_APPS = (
        # other apps
        'zeusci.zeus',
    )


Configure celery
----------------

``zeus-ci`` uses Celery_. Refer to it's documentation on how to configure
message broker and `integrate Celery with Django project
<http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#configuring-your-django-project-to-use-celery>`_.


Add url routes
--------------

We need to hook ``zeusci`` endpoints (including API) at our ``urls.py``. This
can be done as follows::

    from django.conf.urls import patterns, url, include
    from zeusci import zeus


    urlpatterns = patterns('',
        # other url patterns
        url(r'^api/', include(zeus.site.api_urls)),
        url(r'^', include(zeus.site.urls)),
    )


.. _celery: http://www.celeryproject.org/

