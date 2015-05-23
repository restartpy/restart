from __future__ import absolute_import

import json


class Parser(object):

    content_type = None

    def parse(self, data):
        """Parse `data`."""
        raise NotImplementedError()


class JSONParser(Parser):

    content_type = 'application/json'

    def parse(self, data):
        """Parse `data` as JSON."""
        return json.loads(data)
