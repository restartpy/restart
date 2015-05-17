from __future__ import absolute_import

import sys

import click
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple

from restart import router
from restart.request import Request
from restart.utils import load_resources


class API(object):
    def __init__(self, rules):
        self.raw_rules = rules
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
            self.debug = bool(debug)
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)

        run_simple(host, port, self, **options)


@click.command()
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=5000)
@click.option('--debug', '-d', default=False)
@click.argument('entrypoints', nargs=-1, required=True)
def main(entrypoints, host, port, debug):
    if '.' not in sys.path:
        sys.path.insert(0, '.')
    load_resources(entrypoints)

    api = API(router.rules)
    api.run(host, port, debug)
