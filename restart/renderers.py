from __future__ import absolute_import

import json


class Renderer(object):
    """The base renderer class."""

    #: The content type bound to this renderer.
    content_type = None

    #: The format suffix bound to this renderer.
    format_suffix = None

    def render(self, data):
        """Render `data`.

        :param data: the data to be rendered.
        """
        raise NotImplementedError()


class JSONRenderer(Renderer):
    """The JSON renderer class."""

    #: The content type bound to this renderer.
    content_type = 'application/json'

    #: The format suffix bound to this renderer.
    format_suffix = 'json'

    def render(self, data):
        """Render `data` into JSON.

        :param data: the data to be rendered.
        """
        return json.dumps(data)
