from __future__ import absolute_import

import json


class Renderer(object):
    """The base renderer class."""

    #: The content type bound to this renderer.
    content_type = None

    #: The format suffix bound to this renderer.
    format_suffix = None

    def render(self, data, context=None):
        """Render `data`.

        :param data: the data to be rendered.
        :param context: a dictionary containing extra context data
                        that can be useful for rendering.
        """
        raise NotImplementedError()


class JSONRenderer(Renderer):
    """The JSON renderer class."""

    #: The content type bound to this renderer.
    content_type = 'application/json'

    #: The format suffix bound to this renderer.
    format_suffix = 'json'

    def render(self, data, context=None):
        """Render `data` into JSON.

        :param data: the data to be rendered.
        :param context: a dictionary containing extra context data
                        that can be useful for rendering.
        """
        return json.dumps(data)
