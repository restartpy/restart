from __future__ import absolute_import

import sys

import click
from werkzeug.utils import import_string

from .api import RESTArt
from .adapter import Adapter
from .serving import Service


@click.command()
@click.argument('entrypoint', required=True)
@click.option('--adapter', '-a', default='restart.adapter.WerkzeugAdapter',
              help='The adapter class used to adapt RESTArt to a '
                   'specific framework. Defaults to '
                   '`restart.adapter.WerkzeugAdapter`.')
@click.option('--host', '-h', default='127.0.0.1',
              help='The hostname to listen on. Set this to `0.0.0.0` to '
                   'have the server available externally as well. Defaults '
                   'to `127.0.0.1`.')
@click.option('--port', '-p', default=5000,
              help='The port of the webserver. Defaults to `5000`.')
@click.option('--debug', '-d', default=False,
              help='Enable or disable debug mode. Defaults to `False`.')
@click.option('--level', '-l', default='INFO',
              help='The logging level. Defaults to `INFO`.')
def main(entrypoint, adapter, host, port, debug, level):
    if '.' not in sys.path:
        sys.path.insert(0, '.')

    # Get the API object
    api = import_string(entrypoint)
    if not isinstance(api, RESTArt):
        raise RuntimeError(
            'The object specified by entrypoint %r is not an '
            'instance of `restart.api.RESTArt`' % str(entrypoint)
        )

    # Get the adapter class
    adapter_class = import_string(adapter)
    if not issubclass(adapter_class, Adapter):
        raise RuntimeError(
            'The class specified by adapter %r is not a subclass '
            'of `restart.adapter.Adapter`' % str(adapter)
        )

    # Change the level of the global logger
    from .logging import global_logger
    global_logger.setLevel(level)

    # Run the API as a service
    service = Service(api, adapter_class)
    service.run(host, port, debug)
