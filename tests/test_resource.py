from __future__ import absolute_import

import pytest

from restart.config import config
from restart.resource import Resource
from restart.response import Response, WerkzeugResponse
from restart.exceptions import HTTPException
from restart.testing import RequestFactory


factory = RequestFactory()


class RefuseRequestMiddleware(object):

    def process_request(self, request):
        return 'You are refused'


class AlterRequestMiddleware(object):

    def process_request(self, request):
        request.data += ' (altered)'


class AlterResponseMiddleware(object):

    def process_response(self, request, response):
        response.status_code = 201
        return response


class Echo(Resource):

    name = 'echo'

    def read(self, request):
        return request.data

    def create(self, request):
        raise Exception('Error occurs')


class TestResource(object):

    def make_resource(self, action_map=config.ACTION_MAP):
        return Echo(action_map)

    def test_dispatch_request(self):
        data = '"hello"'
        request = factory.get('/', data=data)
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == data
        assert response.status_code == 200

    def test_dispatch_request_with_invalid_action_map(self):
        data = '"hello"'
        request = factory.get('/', data=data)
        resource = self.make_resource(action_map={'POST': 'create'})

        with pytest.raises(KeyError) as exc:
            resource.dispatch_request(request)
        expected_exc_msg = "Config `ACTION_MAP` has no mapping for 'GET'"
        assert str(exc.value) == repr(expected_exc_msg)

    def test_dispatch_request_with_unimplemented_action(self):
        data = '"hello"'
        request = factory.patch('/', data=data)
        resource = self.make_resource()

        with pytest.raises(AttributeError) as exc:
            resource.dispatch_request(request)
        expected_exc_msg = "Unimplemented action 'update'"
        assert str(exc.value) == expected_exc_msg

    def test_dispatch_request_with_action_exception(self):
        data = '"hello"'
        request = factory.post('/', data=data)
        resource = self.make_resource()

        with pytest.raises(Exception) as exc:
            resource.dispatch_request(request)
        expected_exc_msg = 'Error occurs'
        assert str(exc.value) == expected_exc_msg

    def test_handle_exception_with_exception(self):
        resource = self.make_resource()
        resource.request = factory.get('/')
        with pytest.raises(Exception):
            resource.handle_exception(Exception())

    def test_handle_exception_with_httpexception(self):
        resource = self.make_resource()
        resource.request = factory.get('/')
        exc = HTTPException()
        rv = resource.handle_exception(exc)
        assert rv == ({'message': None}, None, {'Content-Type': 'text/html'})

    def test_perform_action_with_request_middlewares(self):
        # Save and change middlewares of Echo class
        initial_middlewares = Echo.middlewares
        Echo._middlewares = (
            RefuseRequestMiddleware(),
            AlterRequestMiddleware()
        )

        data = '"hello"'
        request = factory.get('/', data=data)
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '"You are refused"'
        assert response.status_code == 200

        # Retrieve middlewares of Echo class
        Echo._middlewares = initial_middlewares

    def test_perform_action_with_alter_middlewares(self):
        # Save and change middlewares of Echo class
        initial_middlewares = Echo.middlewares
        Echo._middlewares = (
            AlterRequestMiddleware(),
            AlterResponseMiddleware()
        )

        data = '"hello"'
        request = factory.get('/', data=data)
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '"hello (altered)"'
        assert response.status_code == 201

        # Retrieve middlewares of Echo class
        Echo._middlewares = initial_middlewares

    def test_make_response_with_data(self):
        rv = {'hello': 'world'}
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, Response)
        assert response.data == rv
        assert response.status_code == 200
        assert response.headers == {}

    def test_make_response_with_data_status(self):
        rv = {'hello': 'world'}, 204
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, Response)
        assert response.data == rv[0]
        assert response.status_code == rv[1]
        assert response.headers == {}

    def test_make_response_with_data_status_headers(self):
        rv = {'hello': 'world'}, 204, {'HOST': 'www.test.com'}
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, Response)
        assert response.data == rv[0]
        assert response.status_code == rv[1]
        assert response.headers == rv[2]

    def test_make_response_with_response(self):
        rv = WerkzeugResponse({'hello': 'world'}, 204,
                              {'HOST': 'www.test.com'})
        resource = self.make_resource()
        response = resource.make_response(rv)

        assert isinstance(response, Response)
        assert response.data == rv.data
        assert response.status_code == rv.status_code
        assert response.status == rv.status
        assert response.headers == rv.headers
