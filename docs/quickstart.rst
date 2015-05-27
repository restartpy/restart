.. _quickstart:

Quickstart
==========

Eager to get started? This page gives you a good introduction to RESTArt.

It assumes you already have RESTArt installed. If you do not, head over to the :ref:`installation` section.


A Minimal API
-------------

A minimal RESTArt API looks something like this::

    from restart.art import RESTArt
    from restart.resource import Resource

    art = RESTArt()

    @art.route(methods=['GET'])
    class Greeting(Resource):
        name = 'greeting'

        def read(self, request):
            return {'hello': 'world'}

Just save it as :file:`helloworld.py` and run it with :command:`restart` command::

    $ restart helloworld:art

Then you can consume the API now::

    $ curl http://127.0.0.1:5000/greeting
    {"hello": "world"}

So what does the above code do?

1. First we import two classes :class:`~restart.art.RESTArt` and :class:`~restart.resource.Resource` for later use.
2. Next we create an instance of the :class:`~restart.art.RESTArt` class, which represents the whole RESTArt API.
3. We then use the :meth:`~restart.art.RESTArt.route` decorator to register the `Greeting` class which only cares HTTP verb `GET`.
4. The `Greeting` class is defined as a resource by subclassing the :class:`~restart.resource.Resource` class. It has a :meth:`read` method which is a handler for HTTP verb `GET`.


Resources
---------

In the world of REST APIs, resource is the first-class citizen. That is to say, when you are implementing a REST API, resources are your building blocks.

There are two types of resources: plural resources and singular resources.


Plural Resources
^^^^^^^^^^^^^^^^

Most resources are conceptually equivalent to a collection. These resources are called **Plural Resources**.

As a commonly-accepted practice, you should always use plurals in URIs for pluaral resources. Let's take the classical `Todo` application as an example. If we implement Todo as a resource, there will be two basic URLs for it::

    /todos
    /todos/123

And the frequently-used HTTP verbs (or methods) are::

    GET /todos
    POST /todos
    GET /todos/123
    PUT /todos/123
    PATCH /todos/123
    DELETE /todos/123


Singular Resources
^^^^^^^^^^^^^^^^^^

Sometimes, there are resources that have no collection concept, then we can treat them as **Singular Resources**.

The `Greeting` resource is just an example of singular resources. There are only one URI for it::

    /greeting

Although we only care HTTP verb `GET` then, the possible and frequently-used HTTP verbs are as follows::

    GET /greeting
    PUT /greeting
    PATCH /greeting
    DELETE /greeting

Note the lack of a greeting ID and usage of POST verb.


Routing
-------

With the above concepts and conventions in mind, RESTArt provide three methods to route a resource: :meth:`~restart.art.RESTArt.register`, :meth:`~restart.art.RESTArt.route` and :meth:`~restart.art.RESTArt.add_rule`.


register()
^^^^^^^^^^

The :meth:`~restart.art.RESTArt.register` decorator is provided as a convenient helper specially for plural resources.

Take the `Todo` resource as an example, we may define and register it with the :meth:`~restart.art.RESTArt.register` decorator like this::

    @art.register
    class Todo(Resource):
        name = 'todos'

        # define methods here

See `here <https://github.com/RussellLuo/restart/tree/master/examples/todo/todo.py>`_ for the full code of the `Todo` resource.

Now six different routes are created:

==========  ===========  ===============  ===========================
HTTP Verb   Path         Resource:Action  Used for
==========  ===========  ===============  ===========================
GET         /todos       Todo:index()     display a list of all todos
POST        /todos       Todo:create()    create a new todo
GET         /todos/<pk>  Todo:read()      display a specific todo
PUT         /todos/<pk>  Todo:replace()   replace a specific todo
PATCH       /todos/<pk>  Todo:update()    update a specific todo
DELETE      /todos/<pk>  Todo:delete()    delete a specific todo
==========  ===========  ===============  ===========================

.. note:: You can also register a plural resource by using :meth:`~restart.art.RESTArt.route` instead of :meth:`~restart.art.RESTArt.register`, although it is more complicated.

   For example, the following registration is equivalent to the above one::

    @art.route(uri='/todos', endpoint='todos_list',
               methods=['GET', 'POST'], actions={'GET': 'index'})
    @art.route(uri='/todos/<pk>', endpoint='todos_item',
               methods=['GET', 'PUT', 'PATCH', 'DELETE'])
    class Todo(Resource):
        name = 'todos'

        # define methods here


route()
^^^^^^^

The :meth:`~restart.art.RESTArt.route` decorator is provided mainly for singular resources, but you can also use it for plural resources to customize more details.

For example, if we want to provide a global and single configuration object, we can create it as a singular resource like this::

    @art.route(methods=['GET', 'PUT', 'PATCH', 'DELETE'])
    class Configuration(Resource):
        name = 'configuration'

        # define methods here

Now four different routes are created:

==========  ==============  =======================  =========================
HTTP Verb   Path            Resource:Action          Used for
==========  ==============  =======================  =========================
GET         /configuration  Configuration:read()     display the configuration 
PUT         /configuration  Configuration:replace()  replace the configuration
PATCH       /configuration  Configuration:update()   update the configuration
DELETE      /configuration  Configuration:delete()   delete the configuration
==========  ==============  =======================  =========================


add_rule()
^^^^^^^^^^

The :meth:`~restart.art.RESTArt.add_rule` method is the fundamental method both for :meth:`~restart.art.RESTArt.register` and :meth:`~restart.art.RESTArt.route`. If you do not like the decorator style, and you want to customize more behaviors, you should use it.
