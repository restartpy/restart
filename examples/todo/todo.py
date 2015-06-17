from __future__ import absolute_import

from restart import status
from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFoundError


api = RESTArt()


todos = {
    1: {'id': 1, 'name': 'work'},
    2: {'id': 2, 'name': 'sleep'}
}


@api.register
class Todo(Resource):
    name = 'todos'

    def index(self, request):
        return todos.values()

    def create(self, request):
        pk = len(todos) + 1
        item = dict(id=pk, **request.data)
        todos[pk] = item
        return {'id': pk}, status.HTTP_201_CREATED

    def read(self, request, pk):
        pk = int(pk)
        try:
            return todos[pk]
        except KeyError:
            raise NotFoundError()

    def replace(self, request, pk):
        pk = int(pk)
        item = dict(id=pk, **request.data)
        todos[pk] = item
        return '', status.HTTP_204_NO_CONTENT

    def update(self, request, pk):
        pk = int(pk)
        try:
            todos[pk].update(request.data)
            return '', status.HTTP_204_NO_CONTENT
        except KeyError:
            raise NotFoundError()

    def delete(self, request, pk):
        pk = int(pk)
        try:
            del todos[pk]
            return '', status.HTTP_204_NO_CONTENT
        except KeyError:
            raise NotFoundError()
