.. _best-practices:

Best Practices
==============

Some best practices for using RESTArt are recommendated here.


Project structure
-----------------

There are many different ways to organize your RESTArt API, but here I will describe one that scales well with larger applications and maintains a nice level organization.

Here’s an example directory structure::

    blog/
        blog/
            __init__.py
            api.py               # contains the central API object
            wsgi.py              # contains the WSGI application
            resources/
                __init__.py
                posts/           # contains logic for /posts
                    __init__.py
                    resource.py
                tags/            # contains logic for /tags
                    __init__.py
                    resource.py
        tests/                   # optional, contains the test code

See `examples/trello`_ for details.


.. _examples/trello: https://github.com/RussellLuo/restart/tree/master/examples/trello
