from __future__ import absolute_import

import json


class Renderer(object):

    content_type = None

    def render(self, data):
        """Render `data`."""
        raise NotImplementedError()


class JSONRenderer(Renderer):

    content_type = 'application/json'

    def render(self, data):
        """Render `data` into JSON."""
        return json.dumps(data)
