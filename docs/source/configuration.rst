.. _configuration:

Configuration
=============


Our ``zeus-ci`` project needs a few components prepared. In this document we
describe each of those components and how to configure it. Here is a quick
list:

- :ref:`database <configuration_database>`
- :ref:`broker <configuration_broker>`
- :ref:`cache server <configuration_cache>`


.. _configuration_database:

Configure database connection
-----------------------------

Database is used to store all information on users, projects, builds etc. 

.. TODO: Describe how to configure database connection.


.. _configuration_broker:

Configure message broker connection
-----------------------------------

Message broker is required for communication between web server and workers.

.. TODO: Describe how to configure message broker (celery)


.. _configuration_cache:

Configure caching server
------------------------

.. TODO: Describe how to configure caching backend

