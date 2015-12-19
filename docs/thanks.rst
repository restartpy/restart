Thanks
======

RESTArt is not an innovative product created from scratch. It is based on `Werkzeug`_,
and is inspired by many other awesome libraries and frameworks.

RESTArt has learned from:

- `Flask`_

        How to use `Werkzeug`_ properly, how to elegantly support extensions and :ref:`testing`, and
        how to write documentations based on `Sphinx`_.

- `Django REST framework`_

        How to support :ref:`Parsers <parser-objects>` and :ref:`Renderers <renderer-objects>`.

- `RestExpress`_

        How to map HTTP methods to resource actions, which is the inspiration of :ref:`action-mapping`.

- `Nameko`_

        The convenience of providing a helper command-line utility :ref:`restart <command-line-utility>` (like the ``nameko`` utility),
        and the simplicity and consistency of class-based REST :class:`resources <restart.resource.Resource>` (like the class-based nameko services).

- `Django`_

        How to support :ref:`Middlewares <middleware>`.

- `Flask-API`_

        The last paragraph of the `Roadmap`_ gives me the original inspiration to
        create framework-agnostic REST libraries, such as `Resource`_ and RESTArt.

- `Resource`_

        Its experimental work about REST, which is valuable for RESTArt. The
        MongoDB-related part also becomes the predecessor of `RESTArt-Mongo`_.

- `Flask-RESTful`_

        The good style of its documentations.


.. _Werkzeug: http://werkzeug.pocoo.org
.. _Flask: http://flask.pocoo.org
.. _Sphinx: http://sphinx-doc.org
.. _Django REST framework: http://www.django-rest-framework.org
.. _RestExpress: https://github.com/RestExpress/RestExpress
.. _Nameko: https://github.com/onefinestay/nameko
.. _Django: https://www.djangoproject.com
.. _Resource: https://github.com/RussellLuo/resource
.. _Flask-API: http://www.flaskapi.org
.. _Roadmap: http://www.flaskapi.org/#roadmap
.. _RESTArt-Mongo: https://github.com/RussellLuo/restart-mongo
.. _Flask-RESTful: http://flask-restful.readthedocs.org
