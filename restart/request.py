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
        if not raw:
            return {}
        parsed = self.parser.parse(raw)
        return parsed

    @locked_cached_property
    def method(self):
        return self.get_method()

    @locked_cached_property
    def uri(self):
        return self.get_uri()

    @locked_cached_property
    def path(self):
        return self.get_path()

    @locked_cached_property
    def args(self):
        return self.get_args()

    @locked_cached_property
    def auth(self):
        return self.get_auth()

    @locked_cached_property
    def scheme(self):
        return self.get_scheme()

    @locked_cached_property
    def environ(self):
        return self.get_environ()

    def get_data(self):
        raise NotImplementedError()

    def get_method(self):
        raise NotImplementedError()

    def get_uri(self):
        raise NotImplementedError()

    def get_path(self):
        raise NotImplementedError()

    def get_args(self):
        raise NotImplementedError()

    def get_auth(self):
        raise NotImplementedError()

    def get_scheme(self):
        raise NotImplementedError()

    def get_environ(self):
        raise NotImplementedError()


class WerkzeugRequest(Request):
    """The Werkzeug-specific request class."""

    def get_data(self):
        return self.initial_request.data

    def get_method(self):
        return self.initial_request.method

    def get_uri(self):
        return self.initial_request.url

    def get_path(self):
        return self.initial_request.path

    def get_args(self):
        args = {
            k: v if len(v) > 1 else v[0]
            for k, v in self.initial_request.args.iterlists()
        }
        return args

    def get_auth(self):
        return self.initial_request.authorization

    def get_scheme(self):
        return self.initial_request.scheme

    def get_environ(self):
        return self.initial_request.environ
