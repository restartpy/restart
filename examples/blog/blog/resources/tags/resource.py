from __future__ import absolute_import

from restart.resource import Resource

from blog.api import api


@api.register
class Tags(Resource):
    name = 'tags'

    def index(self, request):
        return []
