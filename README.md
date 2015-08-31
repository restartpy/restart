# RESTArt

A Python library with good intentions for building REST APIs.


## Philosophy

1. Elegant

    `RESTArt` follows the art of [Flask][1]. It tries to help you build REST APIs by writing simple, clean and Pythonic code.

2. Light

    Only the essentials for REST APIs are included, no assumptions are made for you. The frameworks, databases and the business logic are all up to you.

3. Flexible

    Customizations and extensions are made easy. The limit is your imagination!


## RESTArt is Simple

A `RESTArt` resource is just a class:

```python

# helloworld.py

from restart.api import RESTArt
from restart.resource import Resource

api = RESTArt()

@api.route(methods=['GET'])
class Greeting(Resource):
    name = 'greeting'

    def read(self, request):
        return {'hello': 'world'}

```

Run the `Greeting` resource as an API via command `restart`:

```
$ restart helloworld:api
```

Consume the API now:

```
$ curl http://127.0.0.1:5000/greeting
{"hello": "world"}
```


## Documentation

Check out the [documentation][2].


## License

[MIT][3]


[1]: http://flask.pocoo.org/
[2]: https://restart.readthedocs.org
[3]: http://opensource.org/licenses/MIT
