from __future__ import absolute_import

import pytest
from werkzeug.wrappers import Response as WerkzeugSpecificResponse

from restart.config import config
from restart.resource import Resource
from restart.request import WerkzeugRequest
from restart.response import WerkzeugResponse


class FakeWerkzeugRequest(object):
    def __init__(self, data=None, method='GET', url='/'):
        self.data = data or ''
        self.method = method
        self.url = url


class EchoResource(Resource):
    name = 'echo'

    def read(self, request):
        return request.data


class TestResource(object):

    def make_resource(self, request_class=WerkzeugRequest,
                      response_class=WerkzeugResponse,
                      action_map=config.ACTION_MAP):
        return EchoResource(request_class, response_class, action_map)

    def test_dispatch_request(self):
        data = '"hello"'
        request = FakeWerkzeugRequest(data)
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, WerkzeugSpecificResponse)
        assert response.data == data
        assert response.status_code == 200

    def test_dispatch_request_with_invalid_action_map(self):
        data = '"hello"'
        request = FakeWerkzeugRequest(data)
        resource = self.make_resource(action_map={'POST': 'create'})

        with pytest.raises(KeyError) as exc:
            resource.dispatch_request(request)
        expected_exc_msg = "Config `ACTION_MAP` has no mapping for 'GET'"
        assert str(exc.value) == repr(expected_exc_msg)

    def test_dispatch_request_with_unimplemented_action(self):
        data = '"hello"'
        request = FakeWerkzeugRequest(data, method='POST')
        resource = self.make_resource()

        with pytest.raises(AttributeError) as exc:
            resource.dispatch_request(request)
        expected_exc_msg = "Unimplemented action 'create'"
        assert str(exc.value) == expected_exc_msg

    def test_make_response_with_data(self):
        rv = {'hello': 'world'}
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, resource.response_class)
        assert response.data == rv
        assert response.status == 200
        assert response.headers == {}

    def test_make_response_with_data_status(self):
        rv = {'hello': 'world'}, 204
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, resource.response_class)
        assert response.data == rv[0]
        assert response.status == rv[1]
        assert response.headers == {}

    def test_make_response_with_data_status_headers(self):
        rv = {'hello': 'world'}, 204, {'HOST': 'www.test.com'}
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, resource.response_class)
        assert response.data == rv[0]
        assert response.status == rv[1]
        assert response.headers == rv[2]

    def test_make_response_with_response(self):
        rv = WerkzeugResponse({'hello': 'world'}, 204,
                              {'HOST': 'www.test.com'})
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, WerkzeugResponse)
        assert response.data == rv.data
        assert response.status == rv.status
        assert response.headers == rv.headers
