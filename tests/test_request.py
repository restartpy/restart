from __future__ import absolute_import

import pytest

from restart.request import Request, WerkzeugRequest
from restart.parser import JSONParser
from restart.testing import RequestFactory


factory = RequestFactory(keep_initial_request=True)


def assert_environ(environ):
    keys = (
        'CONTENT_LENGTH',
        'CONTENT_TYPE',
        'HTTP_HOST',
        'PATH_INFO',
        'QUERY_STRING',
        'REQUEST_METHOD',
        'SCRIPT_NAME',
        'SERVER_NAME',
        'SERVER_PORT',
        'SERVER_PROTOCOL',
    )
    for key in keys:
        assert key in environ


class TestRequest(object):

    def test_normal_request(self):
        initial_request = factory.post('/', data='{"hello": "world"}')
        with pytest.raises(NotImplementedError):
            Request(initial_request)


class TestWerkzeugRequest(object):

    def test_normal_request(self):
        initial_request = factory.post('/sample?x=1&y=2',
                                       data='{"hello": "world"}',
                                       content_type='application/json')
        request = WerkzeugRequest(initial_request)
        assert (str(request) ==
                "<WerkzeugRequest [POST 'http://localhost/sample?x=1&y=2']>")
        assert request.data == '{"hello": "world"}'
        assert request.method == 'POST'
        assert request.uri == 'http://localhost/sample?x=1&y=2'
        assert request.path == '/sample'
        assert request.args == {'x': '1', 'y': '2'}
        assert request.auth is None
        assert request.scheme == 'http'
        assert request.headers['Host'] == 'localhost'
        assert request.headers['Content-Type'] == 'application/json'
        assert_environ(request.environ)

    def test_parsed_request(self):
        initial_request = factory.post('/sample?x=1&y=2',
                                       data='{"hello": "world"}')
        request = WerkzeugRequest(initial_request)
        parsed_request = request.parse(JSONParser)
        assert parsed_request.data == {'hello': 'world'}

    def test_normal_request_with_empty_data(self):
        initial_request = factory.get('/')
        request = WerkzeugRequest(initial_request)
        assert request.data == ''
        assert request.method == 'GET'
        assert request.uri == 'http://localhost/'
        assert request.path == '/'
        assert request.args == {}
        assert request.auth is None
        assert request.scheme == 'http'
        assert request.headers['Host'] == 'localhost'
        assert_environ(request.environ)

    def test_parsed_request_with_empty_data(self):
        initial_request = factory.get('/')
        request = WerkzeugRequest(initial_request)
        parsed_request = request.parse(JSONParser)
        assert parsed_request.data == {}
