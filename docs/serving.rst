.. _serving:

Serving
=======

This section shows you how to run your APIs in RESTArt.

As a concrete example, consider the following ``Greeting`` API::

    # helloworld.py

    from restart.api import RESTArt
    from restart.resource import Resource

    api = RESTArt()

    @api.route(methods=['GET'])
    class Greeting(Resource):
        name = 'greeting'

        def read(self, request):
            return {'hello': 'world'}


The Pythonic Way
----------------

As a Pythonista, chances are you like to run the API just as a normal Python script. That's good!

The Pythonic way you want is supported by RESTArt, at the cost of a little wrapper code with the help of the :class:`~restart.serving.Service` class::

    # runserver.py

    from restart.serving import Service
    from helloworld import api

    service = Service(api)

    if __name__ == '__main__':
        service.run()

Now, you can run the API like this::

    $ python runserver.py


The Command Line Utility
------------------------

To make the serving step as simple as possible, RESTArt also provides a command line utility called ``restart``. You may have seen it in :ref:`quickstart`. Yes! It's born for serving, and you will not be disappointed to use it::

    $ restart helloworld:api

That's all. Isn't it amazing?

``restart`` has only one argument:

===============  ==============  ========================================
Argument         Example         Description
===============  ==============  ========================================
entrypoint       helloworld:api  A string in the form ``module_path:api``
                                 where `api` is the central RESTArt API
                                 object and `module_path` is the path to
                                 the module where `api` is defined.
===============  ==============  ========================================

For the options supported by ``reatart``, see the help messages::

    $ restart --help
