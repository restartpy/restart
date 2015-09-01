.. _api:

API
===

This section covers all the interfaces of RESTArt.


RESTArt Object
--------------

.. module:: restart.api

.. autoclass:: RESTArt
   :members:

.. autoclass:: Rule
   :members:


Resource Object
---------------

.. module:: restart.resource

.. autoclass:: Resource
   :members:


Request Objects
---------------

.. module:: restart.request

.. autoclass:: Request
   :members:

.. autoclass:: WerkzeugRequest
   :members:


Response Objects
----------------

.. module:: restart.response

.. autoclass:: Response
   :members:

.. autoclass:: WerkzeugResponse
   :members:


Negotiator Object
-----------------

.. module:: restart.negotiator

.. autoclass:: Negotiator
   :members:


.. _parser-objects:

Parser Objects
--------------

.. module:: restart.parsers

.. autoclass:: Parser
   :members:

.. autoclass:: JSONParser
   :members:

.. autoclass:: MultiPartParser
   :members:

.. autoclass:: URLEncodedParser
   :members:


.. _renderer-objects:

Renderer  Objects
-----------------

.. module:: restart.renderers

.. autoclass:: Renderer
   :members:

.. autoclass:: JSONRenderer
   :members:


Middleware Objects
------------------

.. module:: restart.middlewares

.. autoclass:: CORSMiddleware
   :members:


Adapter Objects
---------------

.. module:: restart.adapter

.. autoclass:: Adapter
   :members:

.. autoclass:: WerkzeugAdapter
   :members:


Service Object
--------------

.. module:: restart.serving

.. autoclass:: Service
   :members:
   :special-members: __call__
