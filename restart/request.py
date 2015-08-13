from __future__ import absolute_import

from .utils import locked_cached_property


class Request(object):
    """The base request class used in RESTArt.

    :param initial_request: the initial request, which is framework-specific.
    """

    def __init__(self, initial_request):
        self.initial_request = initial_request

    def parse(self, parser_class):
        """Return a request object with the data parsed, which is a
        dictionary. If the request data is empty, the parsed data
        will be an empty dictionary.

        :param parser_class: the parser class used to parse the request data.
                             See :ref:`parser-objects` for information about
                             parsers.
        """
        parser = parser_class()
        if not self.data:
            self._data = {}
        else:
            self._data = parser.parse(self.data)
        return self

    def __str__(self):
        return "<{} [{} '{}']>".format(self.__class__.__name__,
                                       self.method, self.uri)

    __repr__ = __str__

    @locked_cached_property(name='_data')
    def data(self):
        """The request payload."""
        return self.get_data()

    @locked_cached_property(name='_method')
    def method(self):
        """The request method. (For example `'GET'` or `'POST'`)."""
        return self.get_method()

    @locked_cached_property(name='_uri')
    def uri(self):
        """The request URI."""
        return self.get_uri()

    @locked_cached_property(name='_path')
    def path(self):
        """The request path as unicode, which will always include a leading
        slash, even if the URI root is accessed.
        """
        return self.get_path()

    @locked_cached_property(name='_args')
    def args(self):
        """A dictionary with the parsed URI parameters."""
        return self.get_args()

    @locked_cached_property(name='_auth')
    def auth(self):
        """The authorization data from the request."""
        return self.get_auth()

    @locked_cached_property(name='_scheme')
    def scheme(self):
        """URI scheme (http or https)."""
        return self.get_scheme()

    @locked_cached_property(name='_headers')
    def headers(self):
        """The request headers."""
        return self.get_headers()

    @locked_cached_property(name='_environ')
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

    def get_headers(self):
        """Get the request headers."""
        raise NotImplementedError()

    def get_environ(self):
        """Get the request WSGI environment."""
        raise NotImplementedError()


class WerkzeugRequest(Request):
    """The Werkzeug-specific request class."""

    def get_data(self):
        """Get the request data from the Werkzeug-specific
        request object.
        """
        return self.initial_request.data

    def get_method(self):
        """Get the request method from the Werkzeug-specific
        request object.
        """
        return self.initial_request.method

    def get_uri(self):
        """Get the request URI from the Werkzeug-specific
        request object.
        """
        return self.initial_request.url

    def get_path(self):
        """Get the request path from the Werkzeug-specific
        request object.
        """
        return self.initial_request.path

    def get_args(self):
        """Get the request URI parameters from the Werkzeug-specific
        request object.
        """
        args = {
            k: v if len(v) > 1 else v[0]
            for k, v in self.initial_request.args.iterlists()
        }
        return args

    def get_auth(self):
        """Get the request authorization data from the Werkzeug-specific
        request object.
        """
        return self.initial_request.authorization

    def get_scheme(self):
        """Get the request scheme from the Werkzeug-specific
        request object.
        """
        return self.initial_request.scheme

    def get_headers(self):
        """Get the request headers from the Werkzeug-specific
        request object.
        """
        return dict(self.initial_request.headers)

    def get_environ(self):
        """Get the WSGI environment from the Werkzeug-specific
        request object.
        """
        return self.initial_request.environ
