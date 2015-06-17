from __future__ import absolute_import

import sys

import click
from werkzeug.utils import import_string

from .api import RESTArt
from .serving import Service


@click.command()
@click.argument('entrypoint', required=True)
@click.option('--host', '-h', default='127.0.0.1')
@click.option('--port', '-p', default=5000)
@click.option('--debug', '-d', default=False)
def main(entrypoint, host, port, debug):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

    api = import_string(entrypoint)
    if not isinstance(api, RESTArt):
        raise RuntimeError(
            'No instance of `RESTArt` found with entrypoint %r' % entrypoint
        )

    service = Service(api)
    service.run(host, port, debug)
