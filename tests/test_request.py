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


class TestRequest(object):

    def assert_environ(self, environ):
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

    def test_request(self):
        initial_request = fake_werkzeug_request(
            method='POST',
            data='{"hello": "world"}'
        )
        request = Request(initial_request, JSONParser)

        with pytest.raises(NotImplementedError):
            request.data
        with pytest.raises(NotImplementedError):
            request.method
        with pytest.raises(NotImplementedError):
            request.uri
        with pytest.raises(NotImplementedError):
            request.args
        with pytest.raises(NotImplementedError):
            request.auth
        with pytest.raises(NotImplementedError):
            request.scheme
        with pytest.raises(NotImplementedError):
            request.environ

    def test_werkzeug_request(self):
        initial_request = fake_werkzeug_request(
            method='POST',
            url='/sample?x=1&y=2',
            data='{"hello": "world"}'
        )
        werkzeug_request = WerkzeugRequest(initial_request, JSONParser)

        assert werkzeug_request.data == {'hello': 'world'}
        assert werkzeug_request.method == 'POST'
        assert werkzeug_request.uri == 'http://localhost/sample?x=1&y=2'
        assert werkzeug_request.args == {'x': '1', 'y': '2'}
        assert werkzeug_request.auth is None
        assert werkzeug_request.scheme == 'http'
        self.assert_environ(werkzeug_request.environ)

    def test_werkzeug_request_with_empty_data(self):
        initial_request = fake_werkzeug_request()
        werkzeug_request = WerkzeugRequest(initial_request, JSONParser)

        assert werkzeug_request.data == {}
        assert werkzeug_request.method == 'GET'
        assert werkzeug_request.uri == 'http://localhost/'
        assert werkzeug_request.args == {}
        assert werkzeug_request.auth is None
        assert werkzeug_request.scheme == 'http'
        self.assert_environ(werkzeug_request.environ)
