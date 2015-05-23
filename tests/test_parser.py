from __future__ import absolute_import

import pytest

from restart.parser import Parser, JSONParser


class TestParser(object):

    def test_parser(self):
        parser = Parser()

        with pytest.raises(NotImplementedError):
            parser.parse('{"hello": "world"}')

    def test_json_parser(self):
        parser = JSONParser()
        parsed = parser.parse('{"hello": "world"}')

        assert parsed == {'hello': 'world'}
