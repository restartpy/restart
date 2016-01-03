.. _framework-integration:

Framework Integration
=====================

RESTArt looks like a micro-framework. Like many frameworks, RESTArt handles requests and responses in its own way, and you can build REST APIs based on RESTArt without the help of any other framework.

Actually, RESTArt is designed as a library, which is framework-agnostic. It's the underlying library `Werkzeug`_ that gives RESTArt the ability to serve APIs independently. Strictly speaking, RESTArt consists of the framework-agnostic core library and the framework-specific Werkzeug integration.


Why to integrate with other frameworks?
---------------------------------------

With the built-in Werkzeug integration, RESTArt works well for serving standalone APIs. You may ask why we need to integrate RESTArt with other frameworks? The following are the reasons I can think of:

- You are working with an existing or legacy application, which uses a specific framework
- Your API must be based on a useful library or an awesome extension, but it is framework-specific
- The integration with a specific framework can improve the performance of your API (e.g. `RESTArt-Falcon`_)


How to integrate with other frameworks?
---------------------------------------

In RESTArt, framework integration is made easy by using adapters. For a real-world example, see the `source code`_ of :class:`WerkzeugAdapter <restart.adapter.WerkzeugAdapter>`, which is the adapter for the built-in Werkzeug integration.

.. _flask-adapter:

As another example, We can write an adapter for integrating RESTArt into `Flask`_. Since both RESTArt and `Flask`_ are based on `Werkzeug`_, it's an easy job::

    from six import iteritems
    from restart.adapter import Adapter, WerkzeugAdapter
    from flask import Flask, request


    class FlaskAdapter(Adapter):

        def __init__(self, *args, **kwargs):
            super(FlaskAdapter, self).__init__(*args, **kwargs)
            self.werkzeug_adapter = WerkzeugAdapter(*args, **kwargs)
            self.app = Flask(__name__)
            # Add Flask-specific URI routes
            for rule in self.get_embedded_rules():
                self.app.add_url_rule(**rule)

        def adapt_handler(self, handler, *args, **kwargs):
            """Adapt the request object and the response object for
            the `handler` function.

            :param handler: the handler function to be adapted.
            :param args: a list of positional arguments that will be passed
                         to the handler.
            :param kwargs: a dictionary of keyword arguments that will be passed
                           to the handler.
            """
            return self.werkzeug_adapter.adapt_handler(handler, request,
                                                       *args, **kwargs)

        def wsgi_app(self, environ, start_response):
            """The actual Flask-specific WSGI application.

            See :meth:`~restart.serving.Service.wsgi_app` for the
            meanings of the parameters.
            """
            return self.app(environ, start_response)

        def get_embedded_rules(self):
            """Get the Flask-specific rules used to be embedded into
            an existing or legacy application.

            Usage:

                # The existing Flask application
                from flask import Flask
                app = Flask()
                ...

                # The RESTArt API
                from restart.api import RESTArt
                api = RESTArt()
                ...

                # Embed RESTArt into Flask
                from restart.serving import Service
                from restart.ext.flask.adapter import FlaskAdapter
                service = Service(api, FlaskAdapter)
                for rule in service.embedded_rules:
                    app.add_url_rule(**rule)
            """
            rules = [
                dict(rule=rule.uri, endpoint=endpoint,
                     view_func=rule.handler, methods=rule.methods)
                for endpoint, rule in iteritems(self.adapted_rules)
            ]
            return rules


Framework Adapters
------------------

As a summary, the following list gives the adapters for some frameworks:

===========  ===================================  =================
Framework    Adapter                              Support Type
===========  ===================================  =================
`Werkzeug`_  `WerkzeugAdapter`_                   Built-in class
`Flask`_     :ref:`FlaskAdapter <flask-adapter>`  Extension class
`Falcon`_    `RESTArt-Falcon`_                    Extension library
===========  ===================================  =================

Feel free to contribute adapters for other frameworks.


.. _Werkzeug: http://werkzeug.pocoo.org
.. _RESTArt-Falcon: https://github.com/RussellLuo/restart-falcon
.. _source code: https://github.com/RussellLuo/restart/blob/master/restart/adapter.py#L68
.. _WerkzeugAdapter: https://github.com/RussellLuo/restart/blob/master/restart/adapter.py#L68
.. _Flask: http://flask.pocoo.org
.. _Falcon: https://github.com/falconry/falcon
