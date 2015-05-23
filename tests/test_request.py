from __future__ import absolute_import

import pytest

from restart.request import ProxyRequest, WerkzeugProxyRequest
from restart.parser import JSONParser


class FakeWerkzeugRequest(object):
    def __init__(self, data=None, method='GET', url='/'):
        self.data = data or {}
        self.method = method
        self.url = url


class TestRequest(object):

    def test_proxy_request(self):
        raw_request = FakeWerkzeugRequest('{"hello": "world"}')
        proxy_request = ProxyRequest(raw_request, JSONParser)

        with pytest.raises(NotImplementedError):
            proxy_request.data
        with pytest.raises(NotImplementedError):
            proxy_request.method
        with pytest.raises(NotImplementedError):
            proxy_request.uri

    def test_werkzeug_proxy_request(self):
        raw_request = FakeWerkzeugRequest('{"hello": "world"}')
        proxy_request = WerkzeugProxyRequest(raw_request, JSONParser)

        assert proxy_request.data == {'hello': 'world'}
        assert proxy_request.method == 'GET'
        assert proxy_request.uri == '/'
