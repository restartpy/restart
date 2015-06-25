from __future__ import absolute_import

import pytest
from werkzeug.wrappers import Response as WerkzeugSpecificResponse

from restart.response import Response, WerkzeugResponse
from restart.renderer import JSONRenderer


class TestRequest(object):

    def test_response(self):
        response = Response({'hello': 'world'})

        with pytest.raises(NotImplementedError):
            response.finalize(JSONRenderer)

    def test_werkzeug_request(self):
        response = WerkzeugResponse({'hello': 'world'})
        final_response = response.finalize(JSONRenderer)

        assert isinstance(final_response, WerkzeugSpecificResponse)
        assert final_response.data == '{"hello": "world"}'
        assert final_response.status_code == 200
        assert final_response.status == '200 OK'
        assert final_response.headers['Content-Type'] == 'application/json'
