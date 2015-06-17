from __future__ import absolute_import

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request
from werkzeug.serving import run_simple


class Service(object):
    def __init__(self, art):
        self.raw_rules = art.rules
        self.rule_map = Map([
            Rule(rule.uri, endpoint=endpoint, methods=rule.methods)
            for endpoint, rule in self.raw_rules.iteritems()
        ])

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        adapter = self.rule_map.bind_to_environ(request.environ)
        endpoint, kwargs = adapter.match()
        response = self.raw_rules[endpoint].handler(request, **kwargs)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def run(self, host=None, port=None, debug=None, **options):
        """Runs the API on a local development server."""
        if host is None:
            host = '127.0.0.1'
        if port is None:
            port = 5000
        if debug is not None:
            debug = bool(debug)
        options.setdefault('use_reloader', debug)
        options.setdefault('use_debugger', debug)
        run_simple(host, port, self, **options)
