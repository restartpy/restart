from __future__ import absolute_import

from .config import config


class RESTArt(object):
    """The class that represents the RESTArt API and acts as the
    central object.
    """

    def __init__(self):
        self._rules = {}

    def _get_handler(self, resource_class, actions):
        action_map = config.ACTION_MAP.copy()
        if actions:
            # Override `ACTION_MAP` by `actions`
            action_map.update(actions)

        def handler(request, *args, **kwargs):
            resource = handler.resource_class(handler.action_map)
            return resource.dispatch_request(request, *args, **kwargs)

        # Attach related data to the handler
        handler.resource_class = resource_class
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
        """Register a resource for the given URI rule.

        :param resource_class: the resource class.
        :param uri: the URI registered. Werkzeug-style converters are
                    supported here. See `Rule Format <http://werkzeug
                    .pocoo.org/docs/0.10/routing/#rule-format>`_ for
                    more information.
        :param endpoint: the endpoint for the URI.
        :param methods: a sequence of allowed HTTP methods. If not
                        specified, all methods are allowed.
        :param actions: a dictionary with the specific action mapping pairs
                        used to update the default `ACTION_MAP`. If not
                        specified, the default `ACTION_MAP` will be used.
                        See :ref:`configuration` for more information.
        """
        if endpoint in self._rules:
            raise AssertionError(
                'Endpoint name `%s` already exists' % endpoint
            )
        methods = methods or config.ACTION_MAP.keys()
        handler = self._get_handler(resource_class, actions)
        self._rules[endpoint] = Rule(uri, methods, handler)

    def add_rule_with_format_suffix(self, resource_class, uri, endpoint,
                                    methods=None, actions=None,
                                    format_suffix='disabled'):
        """Register a resource for the given URI rule with a possible
        format suffix.

        :param format_suffix: a string indicating whether or how to support
                              content negotiation via format suffixes on
                              URIs. If specified, its value must be
                              `'disabled'` (not supported),
                              `'optional'` (supported and optional) or
                              `'mandatory'` (supported and mandatory).
                              If not specified, defaults to `'disabled'`.

        See :meth:`add_rule` for the meanings of other parameters.
        """
        FORMAT_SUFFIX_VALUES = ('disabled', 'optional', 'mandatory')
        assert format_suffix in FORMAT_SUFFIX_VALUES, \
            '`format_suffix` must be one of %s' % str(FORMAT_SUFFIX_VALUES)

        if format_suffix in ('disabled', 'optional'):
            self.add_rule(resource_class, uri, endpoint, methods, actions)

        if format_suffix in ('mandatory', 'optional'):
            self.add_rule(resource_class, uri + '.<format>',
                          endpoint + '_format',
                          methods, actions)

    def route(self, cls=None, uri=None, endpoint=None,
              methods=None, actions=None, format_suffix='disabled'):
        """A decorator that is used to register a resource for a given
        URI rule. See :ref:`routing` for more information.

        :param cls: the class that will be decorated.
        :param uri: the URI registered. Werkzeug-style converters are
                    supported here. See `Rule Format`_ for more
                    information. If not specified, the resource
                    :attr:`~restart.resource.Resource.name` with a leading
                    slash will be used. For example, the `uri` will be
                    `'/todos'` if the resource name is `'todos'`.
        :param endpoint: the endpoint for the URI. If not specified, the
                         resource :attr:`~restart.resource.Resource.name`
                         will be used.
        :param methods: a sequence of allowed HTTP methods. If not
                        specified, all methods are allowed.
        :param actions: a dictionary with the specific action mapping pairs
                        used to update the default `ACTION_MAP`. If not
                        specified, the default `ACTION_MAP` will be used.
                        See :ref:`configuration` for more information.
        :param format_suffix: see :meth:`add_rule_with_format_suffix`.
        """
        def decorator(cls):
            actual_uri = uri or '/%s' % cls.name
            actual_endpoint = endpoint or cls.name
            self.add_rule_with_format_suffix(cls, actual_uri, actual_endpoint,
                                             methods, actions, format_suffix)
            return cls
        if cls:
            return decorator(cls)
        return decorator

    def register(self, cls=None, prefix=None, pk='<pk>',
                 list_actions=None, item_actions=None,
                 format_suffix='disabled'):
        """A special decorator that is used to register a plural resource.
        See :ref:`routing` for more information.

        Important note:

            Unlike the :meth:`route` and :meth:`add_rule` methods,
            `'OPTIONS'` is always allowed implicitly in :meth:`register`
            to handle potential CORS. In order to achieve the same purpose,
            you must add `'OPTIONS'` into the `methods` parameter explicitly
            when using the :meth:`route` and :meth:`add_rule` methods.


        :param cls: the class that will be decorated.
        :param prefix: the URI prefix for the resource. If not specified,
                       the resource :attr:`~restart.resource.Resource.name`
                       with a leading slash will be used. For example, the
                       `prefix` will be `'/todos'` if the resource name
                       is `'todos'`.
        :param pk: the primary key name used to identify a specific
                   resource. Werkzeug-style converters are supported here.
                   See `Rule Format`_ for more information.
        :param list_actions: the action mapping pairs for the list-part
                             URI (the URI without the primary key, see
                             :ref:`plural-resources` for more information).
                             If not specified, the default `ACTION_MAP`
                             will be used. See :ref:`configuration` for
                             more information.
        :param item_actions: the action mapping pairs for the item-part
                             URI (the URI with the primary key, see
                             :ref:`plural-resources` for more information).
                             If not specified, the default `ACTION_MAP`
                             will be used. See :ref:`configuration` for
                             more information.
        :param format_suffix: see :meth:`add_rule_with_format_suffix`.
        """
        def decorator(cls):
            actual_prefix = prefix or '/%s' % cls.name
            actual_list_actions = {'GET': 'index'}
            if list_actions:
                actual_list_actions.update(list_actions)
            self.add_rule_with_format_suffix(
                cls, actual_prefix,
                endpoint='%s_list' % cls.name,
                methods=['OPTIONS', 'GET', 'POST'],
                actions=actual_list_actions,
                format_suffix=format_suffix
            )
            self.add_rule_with_format_suffix(
                cls, '%s/%s' % (actual_prefix, pk),
                endpoint='%s_item' % cls.name,
                methods=['OPTIONS', 'GET', 'PUT', 'PATCH', 'DELETE'],
                actions=item_actions,
                format_suffix=format_suffix
            )
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
