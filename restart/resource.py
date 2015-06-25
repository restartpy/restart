from __future__ import absolute_import

from werkzeug.utils import import_string

from .config import config
from .exceptions import HTTPException


class Resource(object):

    name = None

    parser_class = import_string(config.PARSER_CLASS)
    renderer_class = import_string(config.RENDERER_CLASS)

    def __init__(self, request_class, response_class, action_map):
        self.request_class = request_class
        self.response_class = response_class
        self.action_map = action_map

    def dispatch_request(self, request, *args, **kwargs):
        try:
            action_name = self.action_map[request.method]
        except KeyError as exc:
            exc.args = (
                'Config `ACTION_MAP` has no mapping for %r' % request.method,
            )
            raise

        try:
            action = getattr(self, action_name)
        except AttributeError as exc:
            exc.args = ('Unimplemented action %r' % action_name,)
            raise

        request = self.request_class(request, self.parser_class)
        try:
            rv = action(request, *args, **kwargs)
        except Exception as exc:
            rv = self.handle_exception(request, exc)
        response = self.make_response(rv)
        return response.finalize(self.renderer_class)

    def handle_exception(self, request, exc):
        """Handle any exception that occurs, by returning an
        appropriate response, or re-raising the error.
        """
        if isinstance(exc, HTTPException):
            headers = dict(exc.get_headers(request.environ))
            rv = ({'message': exc.description}, exc.code, headers)
            return rv
        else:
            raise exc

    def make_response(self, rv):
        status = 200
        headers = None

        if isinstance(rv, tuple):
            rv_len = len(rv)
            if rv_len == 2:
                rv, status = rv
            elif rv_len == 3:
                rv, status, headers = rv
            else:
                raise ValueError('Resource action return a wrong response')

        if rv is None:
            raise ValueError('Resource action did not return a response')
        elif not isinstance(rv, self.response_class):
            rv = self.response_class(rv, status=status, headers=headers)

        return rv
