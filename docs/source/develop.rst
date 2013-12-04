.. _develop:

Development
===========

Here we will cover a process of ``zeus-ci`` development.


Testing
-------

We use tox_ for running tests against supported Python versions. ``tox.ini``
file defines exactly *what* and *how* is tested.

Running tests
-------------

We need to make sure we have tox installed::

    pip install tox

Now we can run full tox suite::

    tox

In order to list all test environments::

    tox -l

It is also possible to run single test environment::

    tox -e TEST_ENV

.. seealso:: http://tox.readthedocs.org/


Running tests omitting tox
--------------------------

For convenience we can also run test suite without tox's overhead. Simply run::

    $ py.test

at the root of ``zeus-ci`` repository. We are not covering here how to prepare
environment, i.e. how dependencies should be installed, as this could change in
future and ``tox.ini`` file at the root of the repository should explain that.
The most important thing, however, is to remember that ``zeus-ci`` is Python 3
**only** project and it does not support Python 2. This means that ``py.test``
script must refer to Python 3 installation.

.. _tox: http://pypi.python.org/pypi/tox

