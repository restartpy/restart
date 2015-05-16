from __future__ import absolute_import

import json

from werkzeug.wrappers import Request as WerkzeugRequest


class Request(WerkzeugRequest):

    def get_data(self, *args, **kwargs):
        """Override to handle JSON request."""
        data = super(Request, self).get_data(*args, **kwargs)

        content_type = self.environ.get('CONTENT_TYPE')
        if content_type == 'application/json':
            data = json.loads(data)

        return data
