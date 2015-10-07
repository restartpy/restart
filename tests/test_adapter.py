from __future__ import absolute_import

import pytest
from werkzeug.wrappers import Response as WerkzeugSpecificResponse

from restart.api import RESTArt
from restart.resource import Resource
from restart.response import Response
from restart.adapter import Adapter, WerkzeugAdapter
from restart.testing import RequestFactory

factory = RequestFactory()

api = RESTArt()


@api.route(methods=['GET'])
class Demo(Resource):
    name = 'demo'

    def read(self, request):
        return "I'm a demo"


def dummy_handler(*args, **kwargs):
    return Response('dummy')


class TestAdapter(object):

    def test_adapt_rules(self):
        adapter = Adapter(api)
        adapted_rules = adapter.adapted_rules

        assert len(adapted_rules) == 1
        endpoint = list(adapted_rules.keys())[0]
        assert endpoint == 'demo'

        rule = adapted_rules[endpoint]
        assert rule.uri == '/demo'
        assert rule.methods == ['GET']
        assert rule.handler.resource_class == Demo

    def test_adapt_handler(self):
        adapter = Adapter(api)
        with pytest.raises(NotImplementedError):
            adapter.adapt_handler(dummy_handler)

    def test_wsgi_app(self):
        adapter = Adapter(api)
        with pytest.raises(NotImplementedError):
            adapter.wsgi_app(None, None)

    def test_get_embedded_rules(self):
        adapter = Adapter(api)
        with pytest.raises(NotImplementedError):
            adapter.get_embedded_rules()


class TestWerkzeugAdapter(object):

    def test_adapt_handler(self):
        adapter = WerkzeugAdapter(api)
        request = factory.get('/demo')
        response = adapter.adapt_handler(dummy_handler, request)
        assert isinstance(response, WerkzeugSpecificResponse)
