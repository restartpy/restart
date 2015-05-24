from __future__ import absolute_import

from werkzeug.utils import import_string

from .config import config
from .response import Response


class Resource(object):

    name = None

    parser_class = import_string(config.PARSER_CLASS)
    renderer_class = import_string(config.RENDERER_CLASS)

    def __init__(self, proxy_request_class, proxy_response_class, action_map):
        self.proxy_request_class = proxy_request_class
        self.proxy_response_class = proxy_response_class
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

        proxy_req = self.proxy_request_class(request, self.parser_class)
        rv = action(proxy_req, *args, **kwargs)
        response = self.make_response(rv)
        proxy_resp = self.proxy_response_class(response, self.renderer_class)
        return proxy_resp.make_response()

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
        elif not isinstance(rv, Response):
            rv = Response(rv, status=status, headers=headers)

        return rv
