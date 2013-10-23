.. _zci:

zci - command line interface tool
=================================

``zci`` is a command line tool allowing initialization and management of
``zeus-ci`` project.

.. program:: zci

.. cmdoption:: init <PROJECT_PATH>

   Initializes ``zeus-ci`` project at given <PROJECT_PATH>. If no argument is
   given, current directory is used.

   .. note::
      Following subcommands need to be run within project directory. It doesn't
      matter if it's run at the root of the project or at some subdirectory.

