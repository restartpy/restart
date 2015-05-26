.. _quickstart:

Quickstart
==========


A Minimal Application
---------------------

A RESTArt resource is just a class:

.. code-block:: python

    # helloworld.py

    from restart.art import RESTArt
    from restart.resource import Resource

    art = RESTArt()

    @art.route(methods=['GET'])
    class Greeting(Resource):
        name = 'greeting'

        def read(self, request):
            return {'hello': 'world'}

Run the `Greeting` resource as an API via command `restart`:

.. code-block:: shell

    $ restart helloworld:art

Consume the API now:

.. code-block:: shell

    $ curl http://127.0.0.1:5000/greeting
    {"hello": "world"}
