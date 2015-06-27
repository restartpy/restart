from __future__ import absolute_import

import json


class Parser(object):
    """The base parser class."""

    #: The content type bound to this parser.
    content_type = None

    def parse(self, data):
        """Parse `data`.

        :param data: the data to be parsed.
        """
        raise NotImplementedError()


class JSONParser(Parser):
    """The JSON parser class."""

    #: The content type bound to this parser.
    content_type = 'application/json'

    def parse(self, data):
        """Parse `data` as JSON.

        :param data: the data to be parsed.
        """
        return json.loads(data)
