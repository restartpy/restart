from __future__ import absolute_import

from .config import config


rules = {}


class Rule(object):
    def __init__(self, uri, methods, resource_cls, actions):
        self.uri = uri
        self.methods = methods or config.ACTION_MAP.keys()
        self.handler = self._get_handler(resource_cls, actions)

    def _get_handler(self, resource_cls, actions):
        action_map = config.ACTION_MAP.copy()
        if actions:
            # Override `ACTION_MAP` by `actions`
            action_map.update(actions)

        def handler(request, *args, **kwargs):
            resource = handler.resource_cls()
            return resource.dispatch_request(action_map, request, *args, **kwargs)

        handler.resource_cls = resource_cls
        return handler

    def __str__(self):
        return '<Rule [uri({!r})]>'.format(self.uri)

    __repr__ = __str__


def add_rule(resource_cls, uri, endpoint, methods=None, actions=None):
    if endpoint in rules:
        raise AssertionError('Endpoint name `%s` already exists' % endpoint)

    rules[endpoint] = Rule(uri, methods, resource_cls, actions)


def route(cls=None, uri=None, endpoint=None, methods=None, actions=None):
    def decorator(cls):
        real_uri = uri or '/%s' % cls.name
        real_endpoint = endpoint or cls.name
        add_rule(cls, real_uri, real_endpoint, methods, actions)
        return cls
    if cls:
        return decorator(cls)
    return decorator


def register(cls=None, prefix=None, pk='<pk>',
             list_actions=None, item_actions=None):
    def decorator(cls):
        real_prefix = prefix or '/%s' % cls.name
        real_list_actions = {'GET': 'read_list', 'DELETE': 'delete_list'}
        if list_actions:
            real_list_actions.update(list_actions)

        add_rule(cls, real_prefix,
                 endpoint='%s_list' % cls.name,
                 methods=['POST', 'GET', 'DELETE'],
                 actions=real_list_actions)
        add_rule(cls, '%s/%s' % (real_prefix, pk),
                 endpoint='%s_item' % cls.name,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'],
                 actions=item_actions)
        return cls
    if cls:
        return decorator(cls)
    return decorator
