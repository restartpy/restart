from __future__ import absolute_import

from werkzeug.wrappers import Response as WerkzeugSpecificResponse


class Response(object):
    """The base response class used in RESTArt.

    :param data: the reponse body.
    :param status: an integer that represents an HTTP status code.
    :param headers: a dictionary with HTTP header values.
    """

    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def finalize(self, renderer_class):
        """Make the rendered and final response.

        :param renderer_class: the renderer class used to render the
                               response data. See :ref:`renderer-objects`
                               for information about renderers.
        """
        renderer = renderer_class()
        self.data = renderer.render(self.data)
        self.headers.update({'Content-Type': renderer.content_type})
        return self.get_specific_response()

    def get_specific_response(self):
        """Get the framework-specific response."""
        raise NotImplementedError()


class WerkzeugResponse(Response):
    """The Werkzeug-specific response class."""

    def get_specific_response(self):
        """Get the Werkzeug-specific response."""
        return WerkzeugSpecificResponse(self.data, self.status, self.headers)
