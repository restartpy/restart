from __future__ import absolute_import

from .utils import locked_cached_property


class ProxyRequest(object):

    def __init__(self, raw_request, parser_class):
        self.raw_request = raw_request
        self.parser = parser_class()

    @locked_cached_property
    def data(self):
        raw = self.get_data()
        parsed = self.parser.parse(raw)
        return parsed

    @locked_cached_property
    def method(self):
        return self.get_method()

    @locked_cached_property
    def uri(self):
        return self.get_uri()

    def get_data(self):
        raise NotImplementedError()

    def get_method(self):
        raise NotImplementedError()

    def get_uri(self):
        raise NotImplementedError()


class WerkzeugProxyRequest(ProxyRequest):

    def get_data(self):
        return self.raw_request.data

    def get_method(self):
        return self.raw_request.method

    def get_uri(self):
        return self.raw_request.url
