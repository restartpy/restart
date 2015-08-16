from __future__ import absolute_import

from werkzeug.http import parse_options_header

from .exceptions import BadRequest


class Negotiator(object):
    """The class used to select the proper parser or renderer."""

    def select_parser(self, content_type, parser_classes):
        """Select the proper parser class.

        :param content_type: the target content type.
        :param parser_classes: the parser classes to select from.
        """
        content_type, _ = parse_options_header(content_type)
        for parser_class in parser_classes:
            if parser_class.content_type == content_type:
                return parser_class
        raise BadRequest('The content type of the request data '
                         'is not recognized')
