from __future__ import absolute_import

from werkzeug.wrappers import Response as WerkzeugResponse


class Response(object):

    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}


class ProxyResponse(object):

    def __init__(self, raw_response, renderer_class):
        renderer = renderer_class()
        self.data = renderer.render(raw_response.data)
        self.status = raw_response.status
        self.headers = raw_response.headers

    def make_response(self):
        raise NotImplementedError()


class WerkzeugProxyResponse(ProxyResponse):

    def make_response(self):
        return WerkzeugResponse(self.data, self.status, self.headers)
