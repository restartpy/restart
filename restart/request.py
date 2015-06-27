from __future__ import absolute_import

from .utils import locked_cached_property


class Request(object):
    """The base request class used in RESTArt.

    :param initial_request: the initial request, which is framework-specific.
    :param parser_class: the parser class used to parse the request data.
                         See :ref:`parser-objects` for information about
                         parsers.
    """

    def __init__(self, initial_request, parser_class):
        self.initial_request = initial_request
        self.parser = parser_class()

    @locked_cached_property
    def data(self):
        """A dictionary with the parsed request payload. If the request
        payload is empty, an empty dictionary will be returned."""
        raw = self.get_data()
        if not raw:
            return {}
        parsed = self.parser.parse(raw)
        return parsed

    @locked_cached_property
    def method(self):
        """The request method. (For example `'GET'` or `'POST'`)."""
        return self.get_method()

    @locked_cached_property
    def uri(self):
        """The request URI."""
        return self.get_uri()

    @locked_cached_property
    def path(self):
        """The request path as unicode, which will always include a leading
        slash, even if the URI root is accessed."""
        return self.get_path()

    @locked_cached_property
    def args(self):
        """A dictionary with the parsed URI parameters."""
        return self.get_args()

    @locked_cached_property
    def auth(self):
        """The authorization data from the request."""
        return self.get_auth()

    @locked_cached_property
    def scheme(self):
        """URI scheme (http or https)."""
        return self.get_scheme()

    @locked_cached_property
    def environ(self):
        """The WSGI environment used for the request data retrival."""
        return self.get_environ()

    def get_data(self):
        """Get the request data."""
        raise NotImplementedError()

    def get_method(self):
        """Get the request method."""
        raise NotImplementedError()

    def get_uri(self):
        """Get the request URI."""
        raise NotImplementedError()

    def get_path(self):
        """Get the request path."""
        raise NotImplementedError()

    def get_args(self):
        """Get the request URI parameters."""
        raise NotImplementedError()

    def get_auth(self):
        """Get the request authorization data."""
        raise NotImplementedError()

    def get_scheme(self):
        """Get the request scheme."""
        raise NotImplementedError()

    def get_environ(self):
        """Get the request WSGI environment."""
        raise NotImplementedError()


class WerkzeugRequest(Request):
    """The Werkzeug-specific request class."""

    def get_data(self):
        """Get the request data from the Werkzeug-specific
        request object."""
        return self.initial_request.data

    def get_method(self):
        """Get the request method from the Werkzeug-specific
        request object."""
        return self.initial_request.method

    def get_uri(self):
        """Get the request URI from the Werkzeug-specific
        request object."""
        return self.initial_request.url

    def get_path(self):
        """Get the request path from the Werkzeug-specific
        request object."""
        return self.initial_request.path

    def get_args(self):
        """Get the request URI parameters from the Werkzeug-specific
        request object."""
        args = {
            k: v if len(v) > 1 else v[0]
            for k, v in self.initial_request.args.iterlists()
        }
        return args

    def get_auth(self):
        """Get the request authorization data from the Werkzeug-specific
        request object."""
        return self.initial_request.authorization

    def get_scheme(self):
        """Get the request scheme from the Werkzeug-specific
        request object."""
        return self.initial_request.scheme

    def get_environ(self):
        """Get the WSGI environment from the Werkzeug-specific
        request object."""
        return self.initial_request.environ
