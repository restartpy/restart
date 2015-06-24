from __future__ import absolute_import

import pytest

from restart.request import Request, WerkzeugRequest
from restart.parser import JSONParser


class FakeWerkzeugRequest(object):
    def __init__(self, data=None, method='GET', url='/'):
        self.data = data or {}
        self.method = method
        self.url = url


class TestRequest(object):

    def test_request(self):
        initial_request = FakeWerkzeugRequest('{"hello": "world"}')
        request = Request(initial_request, JSONParser)

        with pytest.raises(NotImplementedError):
            request.data
        with pytest.raises(NotImplementedError):
            request.method
        with pytest.raises(NotImplementedError):
            request.uri

    def test_werkzeug_request(self):
        initial_request = FakeWerkzeugRequest('{"hello": "world"}')
        werkzeug_request = WerkzeugRequest(initial_request, JSONParser)

        assert werkzeug_request.data == {'hello': 'world'}
        assert werkzeug_request.method == 'GET'
        assert werkzeug_request.uri == '/'
