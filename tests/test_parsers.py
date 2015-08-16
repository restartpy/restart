from __future__ import absolute_import

import pytest
from cStringIO import StringIO

from werkzeug.datastructures import FileStorage
from restart.parsers import (
    Parser, JSONParser,
    MultiPartParser, URLEncodedParser
)
from restart.testing import RequestFactory


class TestParsers(object):

    factory = RequestFactory(keep_initial_request=True)

    def parse(self, parser, data, content_type=None):
        request = self.factory.get('/', data=data,
                                   content_type=content_type)
        return parser.parse(request.stream,
                            request.content_type,
                            request.content_length)

    def test_parser(self):
        parser = Parser()

        with pytest.raises(NotImplementedError):
            data = {'hello': 'world'}
            self.parse(parser, data)

    def test_json_parser(self):
        parser = JSONParser()
        data = '{"hello": "world"}'
        parsed = self.parse(parser, data, 'application/json')

        assert parsed == {'hello': 'world'}

    def test_multi_part_parser(self):
        parser = MultiPartParser()
        data = {
            'text': 'this is some text',
            'file': (StringIO('this is the file'), 'test.txt')
        }
        parsed_data, parsed_files = self.parse(parser, data)

        assert parsed_data['text'] == 'this is some text'
        assert isinstance(parsed_files['file'], FileStorage)
        assert parsed_files['file'].filename == 'test.txt'
        assert parsed_files['file'].stream.read() == 'this is the file'

    def test_urlencoded_parser(self):
        parser = URLEncodedParser()
        data = {'hello': 'world'}
        parsed = self.parse(parser, data)

        assert parsed == {'hello': 'world'}
