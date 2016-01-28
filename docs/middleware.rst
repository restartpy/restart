.. _middleware:

Middleware
==========

Middleware is a framework of hooks into RESTArt's request/response processing. It's a light, low-level "plugin" system for globally altering RESTArt's input or output.

In RESTArt, any Python class that has a :meth:`process_request` method or a :meth:`process_response` method can be used as a middleware. See :attr:`~restart.resource.Resource.perform_action` for more information about middleware behaviors.


Write a middleware class
------------------------

Suppose you already have an API, and now you want to only allow the authenticated users to access it. To add this limit, you can write a simple middleware class (based on `HTTP Basic authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`_) like this::

    # my_middlewares.py

    from restart.exceptions import Unauthorized

    class AuthMiddleware(object):
        """The middleware used for authentication."""

        def process_request(self, request):
            """Authenticate the request.

            :param request: the request object.
            """
            username = request.auth.get('username')
            password = request.auth.get('password')
            if not (username == 'YOUR_USERNAME' and password == 'YOUR_PASSWORD'):
                raise Unauthorized()

For a real-world middleware implementation, see `RESTArt-CrossDomain <https://github.com/RussellLuo/restart-crossdomain>`_ for an example.


Use a middleware class
----------------------

RESTArt supports middlewares in two styles:

- Global middlewares
- Resource-level middlewares

The processing order of the two styles of middlewares is as follows:

- During request phase, the :meth:`process_request` methods of global middlewares are called before those of resource-level middlewares.
- During response phase, the :meth:`process_response` methods of resource-level middlewares are called before those of global middlewares.


Global middlewares
^^^^^^^^^^^^^^^^^^

To use a middleware class as a global middleware, just add it to the :ref:`MIDDLEWARE_CLASSES <option-middleware-class>` tuple in your RESTArt configuration module.

In the :ref:`MIDDLEWARE_CLASSES <option-middleware-class>` tuple, each middleware is represented by a string: the full Python path to the middleware's class name. For example, here's how to enable the above ``AuthMiddleware`` middleware class::

    MIDDLEWARE_CLASSES = (
        'my_middlewares.AuthMiddleware',
    )


Resource-level middlewares
^^^^^^^^^^^^^^^^^^^^^^^^^^

To use a middleware class as a resource-level middleware, just add it to the ``middleware_classes`` tuple as the class attribute of your resource class.

In the ``middleware_classess`` tuple, each middleware is represented by a class. For example, here's how to enable the above ``AuthMiddleware`` middleware class::

    from restart.api import RESTArt
    from restart.resource import Resource

    from my_middlewares import AuthMiddleware

    api = RESTArt()

    @api.route(methods=['GET'])
    class Demo(Resource):
        name = 'demo'

        middleware_classes = (AuthMiddleware,)

        def read(self, request):
            return 'this is a demo'
