from __future__ import absolute_import

import pytest

from restart.art import RESTArt
from restart.resource import Resource
from restart.config import config


class TestArt(object):

    def assert_rule(self, result, expected):
        uri, methods, resource_class = expected
        assert result.uri == uri
        assert result.methods == methods
        assert result.handler.resource_class == resource_class

    def test_add_rule(self):
        class Dummy(Resource):
            name = 'dummy'

        art = RESTArt()
        art.add_rule(Dummy, '/dummy', 'dummy')
        assert 'dummy' in art.rules

        rule = art.rules['dummy']
        self.assert_rule(rule, ('/dummy', config.ACTION_MAP.keys(), Dummy))

    def test_add_rule_with_exsiting_endpoint(self):
        class Dummy(Resource):
            name = 'dummy'

        art = RESTArt()
        art.add_rule(Dummy, '/dummy', 'dummy')

        with pytest.raises(AssertionError):
            art.add_rule(Dummy, '/dummy', 'dummy')

    def test_route(self):
        art = RESTArt()

        @art.route(methods=['GET'])
        class Item(Resource):
            name = 'item'

        assert 'item' in art.rules

        rule = art.rules['item']
        self.assert_rule(rule, ('/item', ['GET'], Item))

    def test_register(self):
        art = RESTArt()

        @art.register
        class User(Resource):
            name = 'users'

        assert 'users_list' in art.rules
        assert 'users_item' in art.rules

        list_rule = art.rules['users_list']
        self.assert_rule(
            list_rule,
            ('/users', ['GET', 'POST'], User)
        )

        item_rule = art.rules['users_item']
        self.assert_rule(
            item_rule,
            ('/users/<pk>', ['GET', 'PUT', 'PATCH', 'DELETE'], User)
        )
