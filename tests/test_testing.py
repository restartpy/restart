from __future__ import absolute_import

from werkzeug.wrappers import Request as WerkzeugSpecificRequest

from restart.api import RESTArt
from restart.resource import Resource
from restart.request import WerkzeugRequest
from restart.testing import Client, RequestFactory


api = RESTArt()


@api.register
class Case(Resource):
    name = 'cases'

    cases = [{'name': 'case_1'}]

    def index(self, request):
        return self.cases

    def create(self, request):
        return '', 201

    def read(self, request, pk):
        return self.cases[0]

    def replace(self, request, pk):
        return '', 204

    def update(self, request, pk):
        return '', 204

    def delete(self, request, pk):
        return '', 204


class TestClient(object):

    client = Client(api)

    def test_get_cases(self):
        response = self.client.get('/cases')
        assert response.data == '[{"name": "case_1"}]'
        assert response.status_code == 200

    def test_post_cases(self):
        response = self.client.post('/cases')
        assert response.data == '""'
        assert response.status_code == 201

    def test_get_case(self):
        response = self.client.get('/cases/1')
        assert response.data == '{"name": "case_1"}'
        assert response.status_code == 200

    def test_put_case(self):
        response = self.client.put('/cases/1')
        assert response.data == ''
        assert response.status_code == 204

    def test_patch_case(self):
        response = self.client.patch('/cases/1')
        assert response.data == ''
        assert response.status_code == 204

    def test_delete_case(self):
        response = self.client.delete('/cases/1')
        assert response.data == ''
        assert response.status_code == 204


class TestRequestFactory(object):

    initial_factory = RequestFactory(keep_initial_request=True)
    factory = RequestFactory()

    def assert_request(self, request, request_class, method, path,
                       data, args=None):
        args = args or {}

        assert isinstance(request, request_class)
        assert request.method == method
        assert request.path == path
        assert request.data == data
        assert request.args == args

    def test_get_cases(self):
        request = self.initial_factory.get('/cases')
        self.assert_request(request, WerkzeugSpecificRequest,
                            'GET', '/cases', '')

        request = self.factory.get('/cases')
        self.assert_request(request, WerkzeugRequest,
                            'GET', '/cases', '')

    def test_post_cases(self):
        request = self.initial_factory.post('/cases', data='{"name": "case"}')
        self.assert_request(request, WerkzeugSpecificRequest,
                            'POST', '/cases', '{"name": "case"}')

        request = self.factory.post('/cases', data='{"name": "case_2"}')
        self.assert_request(request, WerkzeugRequest,
                            'POST', '/cases', '{"name": "case_2"}')

    def test_get_case(self):
        request = self.initial_factory.get('/cases/1')
        self.assert_request(request, WerkzeugSpecificRequest,
                            'GET', '/cases/1', '')

        request = self.factory.get('/cases/1')
        self.assert_request(request, WerkzeugRequest,
                            'GET', '/cases/1', '')

    def test_put_case(self):
        request = self.initial_factory.put('/cases/1')
        self.assert_request(request, WerkzeugSpecificRequest,
                            'PUT', '/cases/1', '')

        request = self.factory.put('/cases/1')
        self.assert_request(request, WerkzeugRequest,
                            'PUT', '/cases/1', '')

    def test_patch_case(self):
        request = self.initial_factory.patch('/cases/1')
        self.assert_request(request, WerkzeugSpecificRequest,
                            'PATCH', '/cases/1', '')

        request = self.factory.patch('/cases/1')
        self.assert_request(request, WerkzeugRequest,
                            'PATCH', '/cases/1', '')

    def test_delete_case(self):
        request = self.initial_factory.delete('/cases/1')
        self.assert_request(request, WerkzeugSpecificRequest,
                            'DELETE', '/cases/1', '')

        request = self.factory.delete('/cases/1')
        self.assert_request(request, WerkzeugRequest,
                            'DELETE', '/cases/1', '')
