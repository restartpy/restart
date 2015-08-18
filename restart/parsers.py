from __future__ import absolute_import

import json

from werkzeug.formparser import MultiPartParser as WerkzeugMultiPartParser
from werkzeug.formparser import default_stream_factory
from werkzeug.http import parse_options_header
from werkzeug.urls import url_decode_stream

from .exceptions import BadRequest


class Parser(object):
    """The base parser class."""

    #: The content type bound to this parser.
    content_type = None

    def parse(self, stream, content_type, content_length):
        """Parse the `stream`.

        :param stream: the stream to be parsed.
        """
        raise NotImplementedError()


class JSONParser(Parser):
    """The parser class for JSON data."""

    #: The content type bound to this parser.
    content_type = 'application/json'

    def parse(self, stream, content_type, content_length):
        """Parse the `stream` as JSON.

        :param stream: the stream to be parsed.
        """
        data = stream.read().decode('utf-8')
        try:
            return json.loads(data)
        except ValueError:
            raise BadRequest('JSON data is invalid')


class MultiPartParser(Parser):
    """The parser class for multipart form data, which may
    include file data."""

    #: The content type bound to this parser.
    content_type = 'multipart/form-data'

    def parse(self, stream, content_type, content_length):
        """Parse the `stream` as a multipart encoded form.

        :param stream: the stream to be parsed.
        """
        if content_length is None:
            raise BadRequest('MultiPartParser.parse() requires '
                             '`content_length` argument')

        _, options = parse_options_header(content_type)
        boundary = options.get('boundary')
        if boundary is None:
            raise BadRequest('Multipart data missing boundary '
                             'in Content-Type header')
        boundary = boundary.encode('ascii')

        parser = WerkzeugMultiPartParser(default_stream_factory)
        try:
            form, files = parser.parse(stream, boundary, content_length)
            return form.to_dict(), files.to_dict()
        except ValueError:
            raise BadRequest('Multipart data is invalid')


class URLEncodedParser(Parser):
    """The parser class for form data."""

    #: The content type bound to this parser.
    content_type = 'application/x-www-form-urlencoded'

    def parse(self, stream, content_type, content_length):
        """Parse the `stream` as a URL encoded form.

        :param stream: the stream to be parsed.
        """
        data = url_decode_stream(stream)
        return data.to_dict()
