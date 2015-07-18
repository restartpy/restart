from __future__ import absolute_import

import pytest
from werkzeug.wrappers import Response as WerkzeugSpecificResponse

from restart.response import Response, WerkzeugResponse
from restart.renderer import JSONRenderer


class TestResponse(object):

    def test_normal_response(self):
        response = Response({'hello': 'world'})
        assert str(response) == '<Response [200 OK]>'
        assert response.data == {'hello': 'world'}
        assert response.status_code == 200
        assert response.status == '200 OK'

    def test_rendered_response(self):
        response = Response({'hello': 'world'})
        rendered_response = response.render(JSONRenderer)

        assert rendered_response.data == '{"hello": "world"}'

    def test_specific_response(self):
        response = Response({'hello': 'world'})

        with pytest.raises(NotImplementedError):
            response.get_specific_response()


class TestWerkzeugResponse(object):

    def test_specific_rendered_response(self):
        response = WerkzeugResponse({'hello': 'world'})
        rendered_response = response.render(JSONRenderer)
        specific_response = rendered_response.get_specific_response()

        assert isinstance(specific_response, WerkzeugSpecificResponse)
        assert str(response) == '<WerkzeugResponse [200 OK]>'
        assert specific_response.data == '{"hello": "world"}'
        assert specific_response.status_code == 200
        assert specific_response.status == '200 OK'
        assert specific_response.headers['Content-Type'] == 'application/json'
