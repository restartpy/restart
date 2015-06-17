# RESTArt

A Python library with good intentions for building REST APIs.


## Philosophy

`RESTArt` try to help you build your Web APIs by following **the Art of REST**.


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

Check out the [documentation][1].


## License

[MIT][2]


[1]: https://restart.readthedocs.org
[2]: http://opensource.org/licenses/MIT
