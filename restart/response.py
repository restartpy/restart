from __future__ import absolute_import

from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.wrappers import Response as WerkzeugSpecificResponse


class Response(object):
    """The base response class used in RESTArt.

    :param data: the response body.
    :param status: an integer that represents an HTTP status code.
    :param headers: a dictionary with HTTP header values.
    """

    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status_code = status
        self.headers = headers or {}

    @property
    def status(self):
        code = self.status_code
        try:
            _status = '%d %s' % (code, HTTP_STATUS_CODES[code].upper())
        except KeyError:
            _status = '%d UNKNOWN' % code
        return _status

    def render(self, renderer_class):
        """Return a response object with the data rendered.

        :param renderer_class: the renderer class used to render the
                               response data. See :ref:`renderer-objects`
                               for information about renderers.
        """
        renderer = renderer_class()
        self.data = renderer.render(self.data)
        self.headers.update({'Content-Type': renderer.content_type})
        return self

    def __str__(self):
        return '<{} [{}]>'.format(self.__class__.__name__, self.status)

    __repr__ = __str__

    def get_specific_response(self):
        """Get the framework-specific response."""
        raise NotImplementedError()


class WerkzeugResponse(Response):
    """The Werkzeug-specific response class."""

    def get_specific_response(self):
        """Get the Werkzeug-specific response."""
        return WerkzeugSpecificResponse(self.data, self.status_code,
                                        self.headers)
