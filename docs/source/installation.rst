.. _installation:

Installation
============

This application requires Django_ 1.5 or higher.

.. warning::
   Currently zeus-ci must not be used inside virtualenv. It still prepares
   virtualenv for CI server (i.e. when running ``zci init``), however it would
   fail if is run inside another virtualenv. This issue would be fixed after
   MVP is ready.

In order to install ``zeus-ci`` simply use ``pip``::

   pip install zeus-ci

Now you can follow up instructions on :ref:`how to initialize a project
<setup>`.

.. _django: http://www.djangoproject.com/


