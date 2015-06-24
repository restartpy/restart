from __future__ import absolute_import

from werkzeug.wrappers import Response as WerkzeugSpecificResponse


class Response(object):
    """The base response class."""

    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def finalize(self, renderer_class):
        """Make the rendered final response."""
        renderer = renderer_class()
        self.data = renderer.render(self.data)
        return self.get_specific_response()

    def get_specific_response(self):
        """Get the framework-specific response."""
        raise NotImplementedError()


class WerkzeugResponse(Response):
    """The Werkzeug-specific response class."""

    def get_specific_response(self):
        """Get the Werkzeug-specific response."""
        return WerkzeugSpecificResponse(self.data, self.status, self.headers)
