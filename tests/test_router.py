from __future__ import absolute_import

import pytest

from restart import router
from restart.resource import Resource
from restart.config import config


class TestRouter(object):

    def teardown_method(self, method):
        router.rules.clear()

    def assert_rule(self, result, expected):
        uri, methods, resource_class = expected
        assert result.uri == uri
        assert result.methods == methods
        assert result.handler.resource_class == resource_class

    def test_add_rule(self):
        class Dummy(Resource):
            name = 'dummy'

        router.add_rule(Dummy, '/dummy', 'dummy')
        assert 'dummy' in router.rules

        rule = router.rules['dummy']
        self.assert_rule(rule, ('/dummy', config.ACTION_MAP.keys(), Dummy))

    def test_add_rule_with_exsiting_endpoint(self):
        class Dummy(Resource):
            name = 'dummy'

        router.add_rule(Dummy, '/dummy', 'dummy')

        with pytest.raises(AssertionError):
            router.add_rule(Dummy, '/dummy', 'dummy')

    def test_route(self):
        @router.route(methods=['GET'])
        class Item(Resource):
            name = 'item'

        assert 'item' in router.rules

        rule = router.rules['item']
        self.assert_rule(rule, ('/item', ['GET'], Item))

    def test_register(self):
        @router.register
        class User(Resource):
            name = 'users'

        assert 'users_list' in router.rules
        assert 'users_item' in router.rules

        list_rule = router.rules['users_list']
        self.assert_rule(
            list_rule,
            ('/users', ['GET', 'POST'], User)
        )

        item_rule = router.rules['users_item']
        self.assert_rule(
            item_rule,
            ('/users/<pk>', ['GET', 'PUT', 'PATCH', 'DELETE'], User)
        )
