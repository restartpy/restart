from __future__ import absolute_import

from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFound


api = RESTArt()


lists = {
    1: {'id': 1, 'name': 'list1'},
    2: {'id': 2, 'name': 'list2'}
}

cards = {
    1: {'id': 1, 'name': 'card1', 'list_id': 1},
    2: {'id': 2, 'name': 'card2', 'list_id': 1},
    3: {'id': 3, 'name': 'card3', 'list_id': 2},
}


@api.register(pk='<int:list_id>')
class List(Resource):
    name = 'lists'

    def index(self, request):
        return lists.values()

    def read(self, request, list_id):
        try:
            return lists[list_id]
        except KeyError:
            raise NotFound()


@api.register(prefix='/lists/<int:list_id>/cards', pk='<int:card_id>')
class Card(Resource):
    name = 'cards'

    def index(self, request, list_id):
        query_func = lambda c: c['list_id'] == list_id
        result_cards = filter(query_func, cards.values())
        return result_cards

    def read(self, request, list_id, card_id):
        query_func = lambda c: c['list_id'] == list_id and c['id'] == card_id
        result_cards = filter(query_func, cards.values())
        if result_cards:
            return result_cards[0]
        else:
            raise NotFound()
