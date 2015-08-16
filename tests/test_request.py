from __future__ import absolute_import

import pytest

from restart.request import Request, WerkzeugRequest
from restart.parsers import JSONParser
from restart.negotiator import Negotiator
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
        request = Request(initial_request)
        assert request.data == {}

        with pytest.raises(NotImplementedError):
            request.content_type
        with pytest.raises(NotImplementedError):
            request.content_length
        with pytest.raises(NotImplementedError):
            request.stream
        with pytest.raises(NotImplementedError):
            request.method
        with pytest.raises(NotImplementedError):
            request.uri
        with pytest.raises(NotImplementedError):
            request.path
        with pytest.raises(NotImplementedError):
            request.args
        with pytest.raises(NotImplementedError):
            request.auth
        with pytest.raises(NotImplementedError):
            request.scheme
        with pytest.raises(NotImplementedError):
            request.headers
        with pytest.raises(NotImplementedError):
            request.environ

    def test_modified_request(self):
        MODIFIED = 'It is tricky but sometimes useful'

        initial_request = factory.post('/', data='{"hello": "world"}')
        request = Request(initial_request)

        request._data = MODIFIED
        assert request.data == MODIFIED

        request._method = MODIFIED
        assert request.method == MODIFIED

        request._uri = MODIFIED
        assert request.uri == MODIFIED

        request._path = MODIFIED
        assert request.path == MODIFIED

        request._args = MODIFIED
        assert request.args == MODIFIED

        request._auth = MODIFIED
        assert request.auth == MODIFIED

        request._scheme = MODIFIED
        assert request.scheme == MODIFIED

        request._headers = MODIFIED
        assert request.headers == MODIFIED

        request._environ = MODIFIED
        assert request.environ == MODIFIED


class TestWerkzeugRequest(object):

    def test_normal_request(self):
        initial_request = factory.post('/sample?x=1&y=2',
                                       data='{"hello": "world"}',
                                       content_type='application/json')
        request = WerkzeugRequest(initial_request)
        assert (str(request) ==
                "<WerkzeugRequest [POST 'http://localhost/sample?x=1&y=2']>")
        assert request.data == {}
        assert request.stream.read() == '{"hello": "world"}'
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
        initial_request = factory.post(
            '/sample?x=1&y=2',
            data='{"hello": "world"}',
            content_type='application/json'
        )
        request = WerkzeugRequest(initial_request)
        parsed_request = request.parse(Negotiator, [JSONParser])
        assert parsed_request.data == {'hello': 'world'}
        assert request.stream.read() == ''

    def test_normal_request_with_empty_data(self):
        initial_request = factory.get('/')
        request = WerkzeugRequest(initial_request)
        assert request.data == {}
        assert request.stream.read() == ''
        assert request.method == 'GET'
        assert request.uri == 'http://localhost/'
        assert request.path == '/'
        assert request.args == {}
        assert request.auth is None
        assert request.scheme == 'http'
        assert request.headers['Host'] == 'localhost'
        assert_environ(request.environ)
