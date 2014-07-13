.. _setup:

Setup a Zeus-CI project
=======================

Once ``zeus-ci`` is installed command line tool ``zci`` is available.

Initialization
--------------

In order to initialize a project we need to run::

    $ zci init [PROJECT_PATH]

By invoking this command we create a ``zeus-ci`` project. It would create a
following structure of files and directories::

    PROJECT_ROOT/
    ├── app/
    │   ├── zeusapp/
    │   │   ├──  __init__.py
    │   │   ├──  settings.py
    │   │   ├──  urls.py
    │   │   └──  wsgi.py
    │   └── manage.py
    ├── config/
    │   ├──  ez_setup.py
    │   ├──  requirements.txt
    │   └──  supervisord.conf
    ├── log/
    ├── var/
    │   └── builds/
    └── venv/
        └── ... (content of Python virtualenv sandbox)


Let's describe briefly what those are:

- ``app/`` directory contains skeleton for ``zeus-ci``, Django_-based project.
  Read more on :ref:`how to integrate with existing Django project
  <integration>`.

- ``config/`` - here lies installation and deployment related configuration
  files.

- ``log/`` is a directory where all logs would be stored.

- ``venv/`` directory contains sandboxed Python_ environment. Our project would
  use only Python packages and linked binary from this environment. Read more
  on virtualenv_.

- ``var/`` here all *various* files would be stored. By default, ``zeus-ci``
  would store here all builds-related files. If sqlite database is used, it's
  file would be put here by default.


Configuration
~~~~~~~~~~~~~

We need to :ref:`configure <configuration>` our project first. By default, our
project would use sqlite_ database and RabbitMQ_ server as message broker
(needed for communication between web server and build workers).

.. note::
   Make sure to :ref:`configure <configuration>` project for your needs before
   using it in production.


After configuration
~~~~~~~~~~~~~~~~~~~

For running commands we will use ``manage.py`` script. For example run::

    $ app/manage.py

to list all available commands.

Prepare database
~~~~~~~~~~~~~~~~

::

    $ app/manage.py syncdb

This will prepare our database. It will also ask to create administrator user
which we should do now.


Running web server
------------------

Development server is invoked by running::

    $ app/manage.py runserver


Running worker
--------------

In another terminal run::

    $ app/manage.py celery worker


Add project
-----------

We need to go to http://127.0.0.1:8000/ and log in with credentials provided at
the database preparation step. As admin user we can follow instructions on main
page in order to create a project.


.. _python: http://www.python.org
.. _virtualenv: http://www.virtualenv.org
.. _django: http://www.djangoproject.com
.. _sqlite: http://www.sqlite.org
.. _rabbitmq: http://www.rabbitmq.com

