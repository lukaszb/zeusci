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


.. _tox: http://pypi.python.org/pypi/tox

