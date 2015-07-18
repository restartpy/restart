from __future__ import absolute_import

import pytest
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request as WerkzeugSpecificRequest

from restart.request import Request, WerkzeugRequest
from restart.parser import JSONParser


def fake_werkzeug_request(method='GET', url='/', data='',
                          content_type='application/json'):
    if '?' in url:
        path, query_string = url.split('?')
    else:
        path, query_string = url, None
    builder = EnvironBuilder(path=path, query_string=query_string,
                             method=method, data=data,
                             content_type=content_type)
    environ = builder.get_environ()
    request = WerkzeugSpecificRequest(environ)
    return request


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
        initial_request = fake_werkzeug_request(
            method='POST',
            data='{"hello": "world"}'
        )

        with pytest.raises(NotImplementedError):
            Request(initial_request)


class TestWerkzeugRequest(object):

    def test_normal_request(self):
        initial_request = fake_werkzeug_request(
            method='POST',
            url='/sample?x=1&y=2',
            data='{"hello": "world"}'
        )
        request = WerkzeugRequest(initial_request)
        assert str(request) == \
                "<WerkzeugRequest [POST 'http://localhost/sample?x=1&y=2']>"
        assert request.data == '{"hello": "world"}'
        assert request.method == 'POST'
        assert request.uri == 'http://localhost/sample?x=1&y=2'
        assert request.path == '/sample'
        assert request.args == {'x': '1', 'y': '2'}
        assert request.auth is None
        assert request.scheme == 'http'
        assert_environ(request.environ)

    def test_parsed_request(self):
        initial_request = fake_werkzeug_request(
            method='POST',
            url='/sample?x=1&y=2',
            data='{"hello": "world"}'
        )
        request = WerkzeugRequest(initial_request)
        parsed_request = request.parse(JSONParser)
        assert parsed_request.data == {'hello': 'world'}

    def test_normal_request_with_empty_data(self):
        initial_request = fake_werkzeug_request()
        request = WerkzeugRequest(initial_request)
        assert request.data == ''
        assert request.method == 'GET'
        assert request.uri == 'http://localhost/'
        assert request.path == '/'
        assert request.args == {}
        assert request.auth is None
        assert request.scheme == 'http'
        assert_environ(request.environ)

    def test_parsed_request_with_empty_data(self):
        initial_request = fake_werkzeug_request()
        request = WerkzeugRequest(initial_request)
        parsed_request = request.parse(JSONParser)
        assert parsed_request.data == {}
