from __future__ import absolute_import

import pytest
from werkzeug.routing import Map

from restart.api import RESTArt
from restart.resource import Resource
from restart.adapter import Adapter, WerkzeugAdapter


api = RESTArt()


@api.route(methods=['GET'])
class Demo(Resource):
    name = 'demo'

    def read(self, request):
        return "I'm a demo"


class TestAdapter(object):

    def test_adapt(self):
        adapter = Adapter(api)
        adapted_rules = adapter.adapted_rules

        assert len(adapted_rules) == 1
        endpoint = list(adapted_rules.keys())[0]
        assert endpoint == 'demo'

        rule = adapted_rules[endpoint]
        assert rule.uri == '/demo'
        assert rule.methods == ['GET']
        assert rule.handler.resource_class == Demo

    def test_final_rules(self):
        adapter = Adapter(api)
        with pytest.raises(NotImplementedError):
            adapter.final_rules


class TestWerkzeugAdapter(object):

    def test_final_rules(self):
        adapter = WerkzeugAdapter(api)
        final_rules = adapter.final_rules

        assert isinstance(final_rules, Map)
        assert len(final_rules._rules) == 1
