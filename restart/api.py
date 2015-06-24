from __future__ import absolute_import

from .config import config
from .request import WerkzeugRequest
from .response import WerkzeugResponse


class RESTArt(object):
    """The RESTArt object that represents the RESTArt API and acts
    as the central object."""

    #: The class that is used for request objects.  See
    #: :class:`~restart.request.Request` for more information.
    request_class = WerkzeugRequest

    #: The class that is used for response objects.  See
    #: :class:`~restart.response.Response` for more information.
    response_class = WerkzeugResponse

    def __init__(self):
        self._rules = {}

    def _get_handler(self, resource_class, actions):
        action_map = config.ACTION_MAP.copy()
        if actions:
            # Override `ACTION_MAP` by `actions`
            action_map.update(actions)

        def handler(request, *args, **kwargs):
            resource = handler.resource_class(
                handler.request_class,
                handler.response_class,
                handler.action_map
            )
            return resource.dispatch_request(request, *args, **kwargs)

        # Attach related data to the handler
        handler.resource_class = resource_class
        handler.request_class = self.request_class
        handler.response_class = self.response_class
        handler.action_map = action_map
        return handler

    @property
    def rules(self):
        return self._rules

    def add_rule(self, resource_class, uri, endpoint,
                 methods=None, actions=None):
        if endpoint in self._rules:
            raise AssertionError(
                'Endpoint name `%s` already exists' % endpoint
            )
        methods = methods or config.ACTION_MAP.keys()
        handler = self._get_handler(resource_class, actions)
        self._rules[endpoint] = Rule(uri, methods, handler)

    def route(self, cls=None, uri=None, endpoint=None,
              methods=None, actions=None):
        def decorator(cls):
            actual_uri = uri or '/%s' % cls.name
            actual_endpoint = endpoint or cls.name
            self.add_rule(cls, actual_uri, actual_endpoint, methods, actions)
            return cls
        if cls:
            return decorator(cls)
        return decorator

    def register(self, cls=None, prefix=None, pk='<pk>',
                 list_actions=None, item_actions=None):
        def decorator(cls):
            actual_prefix = prefix or '/%s' % cls.name
            actual_list_actions = {'GET': 'index'}
            if list_actions:
                actual_list_actions.update(list_actions)

            self.add_rule(cls, actual_prefix,
                          endpoint='%s_list' % cls.name,
                          methods=['GET', 'POST'],
                          actions=actual_list_actions)
            self.add_rule(cls, '%s/%s' % (actual_prefix, pk),
                          endpoint='%s_item' % cls.name,
                          methods=['GET', 'PUT', 'PATCH', 'DELETE'],
                          actions=item_actions)
            return cls
        if cls:
            return decorator(cls)
        return decorator


class Rule(object):
    def __init__(self, uri, methods, handler):
        self.uri = uri
        self.methods = methods
        self.handler = handler

    def __str__(self):
        return '<Rule [uri({!r})]>'.format(self.uri)

    __repr__ = __str__
