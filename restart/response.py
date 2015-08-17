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

    def render(self, negotiator, renderer_classes, format_suffix):
        """Return a response object with the data rendered.

        :param negotiator: the negotiator object used to select
                           the proper renderer, which will be used
                           to render the response payload.
        :param renderer_classes: the renderer classes to select from.
                               See :ref:`renderer-objects` for
                               information about renderers.
        :param format_suffix: the format suffix of the request uri.
        """
        renderer_class = negotiator.select_renderer(
            renderer_classes, format_suffix
        )
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
