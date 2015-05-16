from __future__ import absolute_import

import json

from werkzeug.wrappers import Response as WerkzeugResponse


class Response(WerkzeugResponse):

    def __init__(self, payload=None, status=None, headers=None, **kwargs):
        """Override to handle JSON response."""
        headers = headers or {}
        if 'Content-Type' not in headers:
            payload = json.dumps(payload)
            headers['Content-Type'] = 'application/json'
        super(Response, self).__init__(payload, status, headers, **kwargs)
