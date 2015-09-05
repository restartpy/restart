from __future__ import absolute_import

import functools

from six import iteritems
from werkzeug.routing import Map as WerkzeugMap, Rule as WerkzeugRule

from .api import Rule
from .request import Request, WerkzeugRequest
from .response import Response, WerkzeugResponse


class Adapter(object):
    """The class used to adapt the RESTArt API to a specific framework.

    :param api: the RESTArt API to adapt.
    """

    #: The class that is used to adapt request objects.  See
    #: :class:`~restart.request.Request` for more information.
    request_class = Request

    #: The class that is used to adapt response objects.  See
    #: :class:`~restart.response.Response` for more information.
    response_class = Response

    def __init__(self, api):
        self.api = api
        self.adapted_rules = self.adapt(api.rules)

    def adapt(self, rules):
        """Adapt the rules to be framework-specific."""
        def decorator(handler):
            @functools.wraps(handler)
            def adapted_handler(request, *args, **kwargs):
                """Adapt the request object and the response object for
                each `handler` in `rules`.
                """
                adapted_request = self.request_class(request)
                response = handler(adapted_request, *args, **kwargs)
                adapted_response = self.response_class(
                    response.data, response.status_code, response.headers
                )
                return adapted_response.get_specific_response()
            return adapted_handler

        adapted_rules = {
            endpoint: Rule(rule.uri, rule.methods, decorator(rule.handler))
            for endpoint, rule in iteritems(rules)
        }
        return adapted_rules

    @property
    def final_rules(self):
        raise NotImplementedError()


class WerkzeugAdapter(Adapter):

    #: The class that is used to adapt request objects.  See
    #: :class:`~restart.request.WerkzeugRequest` for more information.
    request_class = WerkzeugRequest

    #: The class that is used to adapt response objects.  See
    #: :class:`~restart.response.WerkzeugResponse` for more information.
    response_class = WerkzeugResponse

    @property
    def final_rules(self):
        rule_map = WerkzeugMap([
            WerkzeugRule(rule.uri, endpoint=endpoint, methods=rule.methods)
            for endpoint, rule in iteritems(self.adapted_rules)
        ])
        return rule_map
