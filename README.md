# RESTArt

A Python library with good intentions for building REST APIs.


## Philosophy

`RESTArt` try to help you build your Web APIs by following **the Art of REST**.


## RESTArt is Simple

```python

# helloworld.py

from restart import router
from restart.resource import Resource

@router.route(methods=['GET'])
class Greeting(Resource):
    name = 'greeting'

    def read(self, request):
        return {'hello': 'world'}

```

Run the API via command `restart`:

```
$ restart helloworld
```

Consume the API now:

```
$ curl http://127.0.0.1:5000/greeting
{"hello": "world"}
```


## Installation

Install `RESTArt` with `pip`:

    $ pip install Python-RESTArt

Install development version from `GitHub`:

    $ git clone https://github.com/RussellLuo/restart.git
    $ cd restart
    $ python setup.py install


## License

[MIT][1]


[1]: http://opensource.org/licenses/MIT
