.. _testing:

Testing
=======

RESTArt provides a small set of tools that come in handy when writing tests.


.. module:: restart.testing


The test client
---------------

The test client is a Python class that acts as a dummy Web client, allowing you to test your resources and interact with your RESTArt-powered APIs programmatically.

.. autoclass:: Client
   :members:


The request factory
-------------------

The :class:`~restart.testing.RequestFactory` provides a way to generate a request instance that can be used as the first argument to any resource. This means you can test a resource very easy.

.. autoclass:: RequestFactory
   :members:
