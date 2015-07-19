.. _middleware:

Middleware
==========

Middleware is a framework of hooks into RESTArt's request/response processing. It's a light, low-level "plugin" system for globally altering RESTArt's input or output.

In RESTArt, any Python class that has a :meth:`process_request` method or a :meth:`process_response` method can be used as a middleware. For how to implement a middleware, see :class:`~restart.middlewares.CORSMiddleware` for an example.

See :attr:`~restart.resource.Resource.perform_action` for more information about middleware behaviors.


Activate middleware
-------------------

To activate a middleware, add it to the ``MIDDLEWARE_CLASSES`` tuple in your RESTArt config.

In ``MIDDLEWARE_CLASSES``, each middleware is represented by a string: the full Python path to the middleware's class name. For example, here's how to enable the :class:`~restart.middlewares.CORSMiddleware` middleware::

    MIDDLEWARE_CLASSES = (
        'restart.middlewares.CORSMiddleware',
    )
