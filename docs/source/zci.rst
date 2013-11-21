.. _zci:

zci - command line interface tool
=================================

``zci`` is a command line tool allowing initialization and management of
``zeus-ci`` project.

zci init
--------

.. program:: zci init

.. cmdoption:: [PROJECT_PATH]

   Initializes ``zeus-ci`` project at given <PROJECT_PATH>. If no argument is
   given, current directory is used.

.. cmdoption:: --no-bootstrap

   Specifies not to bootstrap the project. Refer to `zci_bootstrap`_.


..
   .. note::
      Following subcommands need to be run within project directory. It doesn't
      matter if it's run at the root of the project or at some subdirectory.

.. _zci_bootstrap:

zci bootstrap
-------------

.. program:: zci bootstrap [PROJECT_PATH]

Following actions would be performed:

- create Python virtual environment directory
- prepare default database

