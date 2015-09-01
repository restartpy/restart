# Trello

A Trello example showing how to create sub-resources based on RESTArt.


## Usage

### 1. Run the API

```
$ cd examples/trello
$ restart api:api
 * Running on http://127.0.0.1:5000/
```

### 2. Consume the API

1. GET /lists

    ```
    $ curl -i http://127.0.0.1:5000/lists
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 56
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Tue, 01 Sep 2015 02:35:58 GMT

    [{"id": 1, "name": "list1"}, {"id": 2, "name": "list2"}]
    ```

2. GET /lists/1

    ```
    $ curl -i http://127.0.0.1:5000/lists/1
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 26
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Tue, 01 Sep 2015 02:39:11 GMT

    {"id": 1, "name": "list1"}
    ```

3. GET /lists/1/cards

    ```
    $ curl -i http://127.0.0.1:5000/lists/1/cards
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 84
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Tue, 01 Sep 2015 02:41:03 GMT

    [{"list_id": 1, "id": 1, "name": "card1"}, {"list_id": 1, "id": 2, "name": "card2"}]
    ```

4. GET /lists/1/cards/1

    ```
    $ curl -i http://127.0.0.1:5000/lists/1/cards/1
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 40
    Server: Werkzeug/0.10.4 Python/2.7.6
    Date: Tue, 01 Sep 2015 02:42:43 GMT

    {"list_id": 1, "id": 1, "name": "card1"}
    ```
