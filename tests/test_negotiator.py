from __future__ import absolute_import

import pytest

from restart.parsers import JSONParser, MultiPartParser, URLEncodedParser
from restart.renderers import JSONRenderer
from restart.negotiator import Negotiator
from restart.exceptions import BadRequest


class TestNegotiator(object):

    negotiator = Negotiator()
    parser_classes = (JSONParser, MultiPartParser, URLEncodedParser)
    renderer_classes = (JSONRenderer,)

    def assert_selected_parser_class(self, content_type, parser_class):
        selected_parser_class = self.negotiator.select_parser(
            self.parser_classes, content_type
        )
        assert selected_parser_class is parser_class

    def test_select_parser_by_application_json(self):
        self.assert_selected_parser_class(
            'application/json',
            JSONParser
        )

    def test_select_parser_by_multipart_form_data(self):
        self.assert_selected_parser_class(
            'multipart/form-data',
            MultiPartParser
        )

    def test_select_parser_by_application_x_www_form_urlencoded(self):
        self.assert_selected_parser_class(
            'application/x-www-form-urlencoded',
            URLEncodedParser
        )

    def test_select_parser_by_non_supported_content_type(self):
        with pytest.raises(BadRequest):
            self.assert_selected_parser_class(
                'text/html',
                None
            )

    def test_select_renderer_with_format_suffix(self):
        selected_renderer_calss = self.negotiator.select_renderer(
            self.renderer_classes, 'json'
        )
        assert selected_renderer_calss is JSONRenderer

    def test_select_renderer_without_format_suffix(self):
        selected_renderer_calss = self.negotiator.select_renderer(
            self.renderer_classes, None
        )
        assert selected_renderer_calss is JSONRenderer
