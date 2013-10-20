
Zeus-CI
=======

Flexible, yet modern Continous Integration server you'd love to use.


Development
===========

Clone repository, enter it's root directory.

In short
--------

::

    pip install fabric jinja2

    git clone git@github.com:lukaszb/zeusci.git
    cd zeusci
    pip install fabric
    fab setup_env
    fab test_py:zeus
    fab reset_env
    fab server

And in another terminal::

    fab celery

Setup environment
-----------------

System
~~~~~~

You should have Ruby, sass, nodejs, npm and coffee-script already installed.
And of course Python.

.. note:: We are going to simplify this.

You would need fabric::

    $ pip install fabric


From now on, ``fab`` would be single point of management over the whole
project. In order to list all available commands simply run::

    fab -l

Project
~~~~~~~

We need to prepare Python virtual environment::

    $ fab setup_env


Tests
~~~~~

Run all Python tests::

    $ fab test_py

Run single tests::

    $ fab test_py:zeus.tests.test_api_builds:TestBuildApi.test_build_detail

