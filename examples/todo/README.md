# Todo

A Todo API as a basic example.


## Usage

### 1. Run the API

```
$ cd examples/todo
$ restart todo
 * Running on http://127.0.0.1:5000/
```

### 2. Consume the API

1. GET /todos

    ```
    $ curl -i http://127.0.0.1:5000/todos
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 55
    Server: Werkzeug/0.10.4 Python/2.7.3
    Date: Sun, 17 May 2015 04:28:40 GMT

    [{"id": 1, "name": "work"}, {"id": 2, "name": "sleep"}]
    ```

2. DELETE /todos

    ```
    curl -i -X DELETE http://127.0.0.1:5000/todos
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.3
    Date: Sun, 17 May 2015 04:33:55 GMT

    ```

3. POST /todos

    ```
    $ curl -i -X POST -H "Content-Type: application/json"-d '{"name":"eat"}' http://127.0.0.1:5000/todos
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 9
    Server: Werkzeug/0.10.4 Python/2.7.3
    Date: Sun, 17 May 2015 04:36:48 GMT

    {"id": 1}
    ```

4. GET /todos/1

    ```
    $ curl -i http://127.0.0.1:5000/todos/1
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 24
    Server: Werkzeug/0.10.4 Python/2.7.3
    Date: Sun, 17 May 2015 04:39:01 GMT

    {"name": "eat", "id": 1}
    ```

5. PUT /todos/1

    ```
    $ curl -i -X PUT -H "Content-Type: application/json" -d '{"name":"drink"}' http://127.0.0.1:5000/todos/1
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.3
    Date: Sun, 17 May 2015 04:40:49 GMT

    ```

6. PATCH /todos/1

    ```
    $ curl -i -X PATCH -H "Content-Type: application/json" -d '{"name":"sing"}' http://127.0.0.1:5000/todos/1
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.3
    Date: Sun, 17 May 2015 04:42:09 GMT

    ```

7. DELETE /todos/1

    ```
    curl -i -X DELETE http://127.0.0.1:5000/todos/1
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.10.4 Python/2.7.3
    Date: Sun, 17 May 2015 04:42:43 GMT

    ```
