.. _quick-start:

Quick start
===========

Here we describe steps needed to quickly setup ``zeus-ci`` instance, in example
at your laptop.


Prerequisites
-------------

Make sure you have following components and servers installed and running:

- Python_ (min version: 3.3)
- supervisor_
- memcached_
- rabbitmq_


Installation
------------

Install ``zeusci`` package::

    $ pip3 install zeusci


Start server at default location
--------------------------------

In order to start server and it's components (like background jobs worker)

::

    $ zci start

Yeah, it's that easy.


.. _python: https://www.python.org/
.. _supervisor: http://supervisord.org/
.. _memcached: http://memcached.org/
.. _rabbitmq: http://www.rabbitmq.com/
