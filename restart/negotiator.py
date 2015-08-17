from __future__ import absolute_import

from werkzeug.http import parse_options_header

from .exceptions import BadRequest


class Negotiator(object):
    """The class used to select the proper parser and renderer."""

    def select_parser(self, parser_classes, content_type):
        """Select the proper parser class.

        :param parser_classes: the parser classes to select from.
        :param content_type: the target content type.
        """
        assert parser_classes, 'No parser class available'
        content_type, _ = parse_options_header(content_type)
        for parser_class in parser_classes:
            if parser_class.content_type == content_type:
                return parser_class
        raise BadRequest('The content type of the request data '
                         'is not recognized')

    def select_renderer(self, renderer_classes, format_suffix):
        """Select the proper renderer class.

        Note:
            For simplicity, the content-negotiation here is only based
            on the format suffix specified in the request uri. The more
            standard (and also complex) Accept header is ignored.

        :param renderer_classes: the renderer classes to select from.
        :param format_suffix: the format suffix of the request uri.
        """
        assert renderer_classes, 'No renderer class available'
        if format_suffix:
            for renderer_class in renderer_classes:
                if renderer_class.format_suffix == format_suffix:
                    return renderer_class
        # Use the first renderer class if no format suffix is specified
        return renderer_classes[0]
