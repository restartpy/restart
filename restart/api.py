from __future__ import absolute_import

from .config import config
from .request import WerkzeugRequest
from .response import WerkzeugResponse


class RESTArt(object):
    """The class that represents the RESTArt API and acts as the
    central object.
    """

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
        """A dictionary of all registered rules, which is a mapping from
        URI endpoints to URI rules. See :class:`~restart.api.Rule` for
        more information about URI rules.
        """
        return self._rules

    def add_rule(self, resource_class, uri, endpoint,
                 methods=None, actions=None):
        """Register a resource for a given URI rule.

        :param resource_class: the resource class.
        :param uri: the URI registered.
        :param endpoint: the endpoint for the URI.
        :param methods: a sequence of allowed HTTP methods. If not
                        specified, all methods are allowed.
        :param actions: a dictionary with the specific action mapping pairs
                        used to update the default `ACTION_MAP`. If not
                        specified, use the default `ACTION_MAP`. See
                        :ref:`` for more information.
        """
        if endpoint in self._rules:
            raise AssertionError(
                'Endpoint name `%s` already exists' % endpoint
            )
        methods = methods or config.ACTION_MAP.keys()
        handler = self._get_handler(resource_class, actions)
        self._rules[endpoint] = Rule(uri, methods, handler)

    def route(self, cls=None, uri=None, endpoint=None,
              methods=None, actions=None):
        """A decorator that is used to register a resource for a given
        URI rule. See :ref:`routing` for more information.

        :param cls: the class that will be decorated.
        :param uri: the URI registered.
        :param endpoint: the endpoint for the URI.
        :param methods: a sequence of allowed HTTP methods. If not
                        specified, all methods are allowed.
        :param actions: a dictionary with the specific action mapping pairs
                        used to update the default `ACTION_MAP`. If not
                        specified, use the default `ACTION_MAP`. See
                        :ref:`` for more information.
        """
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
        """A special decorator that is used to register a plural resource.
        See :ref:`routing` for more information.

        :param cls: the class that will be decorated.
        :param prefix: the URI prefix for the resource. If not specified,
                       the resource name will be used.
        :param pk: the primary key name to identify a specific resource.
        :param list_actions: the action mapping for the list-part URI
                             (without the primary key). See
                             :ref:`plural-resources` for more information.
        :param item_actions: the action mapping for the item-part URI
                             (with the primary key). See
                             :ref:`plural-resources` for more information.
        """
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
    """A simple class that holds a URI rule.

    :param uri: the URI.
    :param methods: the allowed HTTP methods for the URI.
    :param handler: the handler for the URI.
    """

    def __init__(self, uri, methods, handler):
        self.uri = uri
        self.methods = methods
        self.handler = handler

    def __str__(self):
        return '<Rule [uri({!r})]>'.format(self.uri)

    __repr__ = __str__
