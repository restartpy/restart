from __future__ import absolute_import

import pytest

from restart.parsers import JSONParser, MultiPartParser, URLEncodedParser
from restart.renderers import JSONRenderer
from restart.negotiator import Negotiator
from restart.exceptions import UnsupportedMediaType, NotFound, NotAcceptable


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

    def test_select_parser_by_unsupported_content_type(self):
        with pytest.raises(UnsupportedMediaType):
            self.assert_selected_parser_class(
                'text/html',
                None
            )

    def test_select_parser_with_empty_parser_classes(self):
        with pytest.raises(UnsupportedMediaType):
            self.negotiator.select_parser(
                (), 'application/json'
            )

    def test_select_renderer_with_format_suffix(self):
        selected_renderer_calss = self.negotiator.select_renderer(
            self.renderer_classes, 'json'
        )
        assert selected_renderer_calss is JSONRenderer

    def test_select_renderer_with_unsupported_format_suffix(self):
        with pytest.raises(NotFound):
            self.negotiator.select_renderer(
                self.renderer_classes, 'csv'
            )

    def test_select_renderer_with_format_suffix_but_no_renderer_classes(self):
        with pytest.raises(NotFound):
            self.negotiator.select_renderer(
                (), 'json'
            )

    def test_select_renderer_without_format_suffix(self):
        selected_renderer_calss = self.negotiator.select_renderer(
            self.renderer_classes, None
        )
        assert selected_renderer_calss is JSONRenderer

    def test_select_renderer_with_no_format_suffix_nor_renderer_classes(self):
        with pytest.raises(NotAcceptable):
            self.negotiator.select_renderer(
                (), None
            )
