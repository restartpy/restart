# Trello

A Blog example showing how to manage larger applications.


## Usage

### 1. Run the API

```
$ cd examples/blog
$ restart blog.api:api
 * Running on http://127.0.0.1:5000/
```

### 2. Consume the API

1. GET /posts

    ```
    $ curl -i http://127.0.0.1:5000/posts
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Tue, 01 Sep 2015 03:11:40 GMT

    []
    ```

2. GET /tags

    ```
    $ curl -i http://127.0.0.1:5000/tags
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Tue, 01 Sep 2015 03:16:27 GMT

    []
    ```

### 3. Deploy the API

```
$ gunicorn blog.wsgi -b 127.0.0.1:5000
```
