from __future__ import absolute_import

from restart.config import config
from restart.resource import Resource
from restart.response import Response
from restart.middlewares import CORSMiddleware
from restart.testing import RequestFactory


factory = RequestFactory()


class Echo(Resource):
    name = 'echo'

    def read(self, request):
        return request.data


class TestCORSMiddleware(object):

    def make_resource(self, action_map=config.ACTION_MAP):
        return Echo(action_map)

    def setup_class(cls):
        # Save and change `Echo.middlewares`
        cls.initial_middlewares = Echo.middlewares
        Echo.middlewares = (CORSMiddleware(),)

    def teardown_class(cls):
        # Retrieve `Echo.middlewares`
        Echo.middlewares = cls.initial_middlewares

    def test_preflight_request_without_request_headers(self):
        request = factory.options(
            '/',
            headers=[('Origin', 'http://localhost'),
                     ('Access-Control-Request-Method', 'GET')]
        )
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '""'
        assert response.status_code == 200
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert (response.headers['Access-Control-Allow-Methods'] ==
                'GET, POST, PUT, PATCH, DELETE')
        assert response.headers['Access-Control-Max-Age'] == '864000'
        assert 'Access-Control-Allow-Headers' not in response.headers
        assert 'Access-Control-Allow-Credentials' not in response.headers
        assert 'Vary' not in response.headers

    def test_preflight_request_with_request_headers(self):
        request = factory.options(
            '/',
            headers=[('Origin', 'http://localhost'),
                     ('Access-Control-Request-Method', 'GET'),
                     ('Access-Control-Request-Headers', 'X-CORS')]
        )
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '""'
        assert response.status_code == 200
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert (response.headers['Access-Control-Allow-Methods'] ==
                'GET, POST, PUT, PATCH, DELETE')
        assert response.headers['Access-Control-Max-Age'] == '864000'
        assert response.headers['Access-Control-Allow-Headers'] == 'X-CORS'
        assert 'Access-Control-Allow-Credentials' not in response.headers
        assert 'Vary' not in response.headers

    def test_preflight_request_with_credentials(self):
        # Save and change CORS config
        initial_cors_allow_origin = config.CORS_ALLOW_ORIGIN
        initial_cors_allow_credentials = config.CORS_ALLOW_CREDENTIALS
        config.CORS_ALLOW_ORIGIN = 'http://localhost'
        config.CORS_ALLOW_CREDENTIALS = True

        request = factory.options(
            '/',
            headers=[('Origin', 'http://localhost'),
                     ('Access-Control-Request-Method', 'GET')]
        )
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '""'
        assert response.status_code == 200
        assert (response.headers['Access-Control-Allow-Origin'] ==
                'http://localhost')
        assert (response.headers['Access-Control-Allow-Methods'] ==
                'GET, POST, PUT, PATCH, DELETE')
        assert response.headers['Access-Control-Max-Age'] == '864000'
        assert response.headers['Access-Control-Allow-Credentials'] == 'true'
        assert response.headers['Vary'] == 'Origin'

        # Retrive CORS config
        config.CORS_ALLOW_ORIGIN = initial_cors_allow_origin
        config.CORS_ALLOW_CREDENTIALS = initial_cors_allow_credentials

    def test_actual_request(self):
        data = {'hello': 'world'}
        request = factory.get('/', data=data)
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '{"hello": "world"}'
        assert response.status_code == 200
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert 'Access-Control-Allow-Credentials' not in response.headers
        assert 'Vary' not in response.headers

    def test_actual_request_with_credentials(self):
        # Save and change CORS config
        initial_cors_allow_origin = config.CORS_ALLOW_ORIGIN
        initial_cors_allow_credentials = config.CORS_ALLOW_CREDENTIALS
        config.CORS_ALLOW_ORIGIN = 'http://localhost'
        config.CORS_ALLOW_CREDENTIALS = True

        data = {'hello': 'world'}
        request = factory.get('/', data=data)
        resource = self.make_resource()
        response = resource.dispatch_request(request)

        assert isinstance(response, Response)
        assert response.data == '{"hello": "world"}'
        assert response.status_code == 200
        assert (response.headers['Access-Control-Allow-Origin'] ==
                'http://localhost')
        assert response.headers['Access-Control-Allow-Credentials'] == 'true'
        assert response.headers['Vary'] == 'Origin'

        # Retrive CORS config
        config.CORS_ALLOW_ORIGIN = initial_cors_allow_origin
        config.CORS_ALLOW_CREDENTIALS = initial_cors_allow_credentials
