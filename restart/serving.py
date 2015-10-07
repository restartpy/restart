from __future__ import absolute_import

from werkzeug.serving import run_simple

from .adapter import WerkzeugAdapter


class Service(object):
    """The service class for serving the RESTArt API.

    :param api: the RESTArt API.
    :param adapter_class: the class that is used to adapt the api object.
                          See :class:`~restart.adapter.WerkzeugAdapter`
                          for more information.
    """

    def __init__(self, api, adapter_class=WerkzeugAdapter):
        self.adapter = adapter_class(api)

    @property
    def rules(self):
        """The framework-specific API rules."""
        return self.adapter.adapted_rules

    @property
    def embedded_rules(self):
        """The framework-specific rules used to be embedded into
        an existing or legacy application.
        """
        return self.adapter.get_embedded_rules()

    def wsgi_app(self, environ, start_response):
        """The actual WSGI application.

        :param environ: a WSGI environment.
        :param start_response: a callable accepting a status code, a list
                               of headers and an optional exception context
                               to start the response
        """
        return self.adapter.wsgi_app(environ, start_response)

    def __call__(self, environ, start_response):
        """Make the Service object itself to be a WSGI application.

        :param environ: a WSGI environment.
        :param start_response: a callable accepting a status code, a list
                               of headers and an optional exception context
                               to start the response
        """
        return self.wsgi_app(environ, start_response)

    def run(self, host=None, port=None, debug=None, **options):
        """Runs the API on a local development server.

        :param host: the hostname to listen on. Set this to `'0.0.0.0'` to
                     have the server available externally as well. Defaults
                     to `'127.0.0.1'`.
        :param port: the port of the webserver. Defaults to `5000`.
        :param debug: if given, enable or disable debug mode.
        :param options: the options to be forwarded to the underlying Werkzeug
                        server. See :func:`werkzeug.serving.run_simple`
                        for more information.
        """
        if host is None:
            host = '127.0.0.1'
        if port is None:
            port = 5000
        if debug is not None:
            debug = bool(debug)
        options.setdefault('use_reloader', debug)
        options.setdefault('use_debugger', debug)
        run_simple(host, port, self, **options)
