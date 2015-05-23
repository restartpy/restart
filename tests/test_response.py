from __future__ import absolute_import

import pytest
from werkzeug.wrappers import Response as WerkzeugResponse

from restart.response import Response, ProxyResponse, WerkzeugProxyResponse
from restart.renderer import JSONRenderer


class TestRequest(object):

    def test_proxy_response(self):
        raw_response = Response({'hello': 'world'})
        proxy_response = ProxyResponse(raw_response, JSONRenderer)

        assert proxy_response.data == '{"hello": "world"}'
        assert proxy_response.status == 200
        assert proxy_response.headers == {}
        with pytest.raises(NotImplementedError):
            proxy_response.make_response()

    def test_werkzeug_proxy_request(self):
        raw_response = Response({'hello': 'world'})
        proxy_response = WerkzeugProxyResponse(raw_response, JSONRenderer)

        actual_response = proxy_response.make_response()
        assert isinstance(actual_response, WerkzeugResponse)
        assert actual_response.data == '{"hello": "world"}'
        assert actual_response.status_code == 200
        assert actual_response.status == '200 OK'
