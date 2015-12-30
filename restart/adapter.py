from __future__ import absolute_import

import functools

from six import iteritems
from werkzeug.routing import Map as WerkzeugMap, Rule as WerkzeugRule
from werkzeug.wrappers import (
    Request as WerkzeugSpecificRequest,
    Response as WerkzeugSpecificResponse
)
from werkzeug.exceptions import NotFound

from .api import Rule
from .request import WerkzeugRequest
from .response import WerkzeugResponse


class Adapter(object):
    """The class used to adapt the RESTArt API to a specific framework.

    :param api: the RESTArt API to adapt.
    """

    def __init__(self, api):
        self.adapted_rules = self.adapt_rules(api.rules)

    def adapt_rules(self, rules):
        """Adapt the rules to be framework-specific."""
        def decorator(handler):
            @functools.wraps(handler)
            def adapted_handler(*args, **kwargs):
                return self.adapt_handler(handler, *args, **kwargs)
            return adapted_handler

        adapted_rules = {
            endpoint: Rule(rule.uri, rule.methods, decorator(rule.handler))
            for endpoint, rule in iteritems(rules)
        }
        return adapted_rules

    def adapt_handler(self, handler, *args, **kwargs):
        """Adapt the request object and the response object for
        the `handler` function.

        :param handler: the handler function to be adapted.
        :param args: a list of positional arguments that will be passed
                     to the handler.
        :param kwargs: a dictionary of keyword arguments that will be passed
                       to the handler.
        """
        raise NotImplementedError()

    def wsgi_app(self, environ, start_response):
        """The actual framework-specific WSGI application.

        See :meth:`~restart.serving.Service.wsgi_app` for the
        meanings of the parameters.
        """
        raise NotImplementedError()

    def get_embedded_rules(self):
        """Get the framework-specific rules used to be embedded into
        an existing or legacy application.
        """
        raise NotImplementedError()


class WerkzeugAdapter(Adapter):

    def __init__(self, *args, **kwargs):
        super(WerkzeugAdapter, self).__init__(*args, **kwargs)
        self.rule_map = WerkzeugMap(self.get_embedded_rules())

    def adapt_handler(self, handler, request, *args, **kwargs):
        """Adapt the request object and the response object for
        the `handler` function.

        :param handler: the handler function to be adapted.
        :param request: the Werkzeug request object.
        :param args: a list of positional arguments that will be passed
                     to the handler.
        :param kwargs: a dictionary of keyword arguments that will be passed
                       to the handler.
        """
        adapted_request = WerkzeugRequest(request)
        response = handler(adapted_request, *args, **kwargs)
        adapted_response = WerkzeugResponse(
            response.data, response.status_code, response.headers
        )
        return adapted_response.get_specific_response()

    def wsgi_app(self, environ, start_response):
        """The actual Werkzeug-specific WSGI application.

        See :meth:`~restart.serving.Service.wsgi_app` for the
        meanings of the parameters.
        """
        request = WerkzeugSpecificRequest(environ)
        adapter = self.rule_map.bind_to_environ(request.environ)
        try:
            endpoint, kwargs = adapter.match()
        except NotFound:
            response = WerkzeugSpecificResponse(
                'The requested URI was not found.', 404
            )
        else:
            response = self.adapted_rules[endpoint].handler(request, **kwargs)
        return response(environ, start_response)

    def get_embedded_rules(self):
        """Get the Werkzeug-specific rules used to be embedded into
        an existing or legacy application.

        Example::

            # The existing Werkzeug application,
            # whose URL map is `app.url_map`
            app = ...
            ...

            # The RESTArt API
            from restart.api import RESTArt
            api = RESTArt()
            ...

            # Embed RESTArt into Werkzeug
            from restart.serving import Service
            service = Service(api)
            for rule in service.embedded_rules:
                app.url_map.add(rule)
        """
        rules = [
            WerkzeugRule(rule.uri, endpoint=endpoint, methods=rule.methods)
            for endpoint, rule in iteritems(self.adapted_rules)
        ]
        return rules
