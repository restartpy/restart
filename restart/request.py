from __future__ import absolute_import

from .utils import locked_cached_property


class Request(object):
    """The base request class."""

    def __init__(self, initial_request, parser_class):
        self.initial_request = initial_request
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


class WerkzeugRequest(Request):
    """The Werkzeug-specific request class."""

    def get_data(self):
        return self.initial_request.data

    def get_method(self):
        return self.initial_request.method

    def get_uri(self):
        return self.initial_request.url
