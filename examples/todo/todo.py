from __future__ import absolute_import

from restart import status
from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFound


api = RESTArt()


todos = {
    1: {'id': 1, 'name': 'work'},
    2: {'id': 2, 'name': 'sleep'}
}


@api.register(pk='<int:todo_id>')
class Todo(Resource):
    name = 'todos'

    def index(self, request):
        return todos.values()

    def create(self, request):
        todo_id = max(todos.keys()) + 1
        item = dict(id=todo_id, **request.data)
        todos[todo_id] = item
        return {'id': todo_id}, status.HTTP_201_CREATED

    def read(self, request, todo_id):
        try:
            return todos[todo_id]
        except KeyError:
            raise NotFound()

    def replace(self, request, todo_id):
        item = dict(id=todo_id, **request.data)
        todos[todo_id] = item
        return '', status.HTTP_204_NO_CONTENT

    def update(self, request, todo_id):
        try:
            todos[todo_id].update(request.data)
            return '', status.HTTP_204_NO_CONTENT
        except KeyError:
            raise NotFound()

    def delete(self, request, todo_id):
        try:
            del todos[todo_id]
            return '', status.HTTP_204_NO_CONTENT
        except KeyError:
            raise NotFound()
