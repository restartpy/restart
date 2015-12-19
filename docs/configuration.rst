.. _configuration:

Configuration
=============

This section covers all configuration options for you to customize the behavior of RESTArt APIs.


Options
-------

.. module:: restart.config.default


Server
^^^^^^

===========  ===============================  ========================================
Option name  Default value                    Description
===========  ===============================  ========================================
SERVER_NAME  .. autodata_value:: SERVER_NAME  The server name (scheme + domain + port)
===========  ===============================  ========================================


.. _action-mapping:

Action mapping
^^^^^^^^^^^^^^

===========  ==============================  ==================================
Option name  Default value                   Description
===========  ==============================  ==================================
ACTION_MAP   .. autodata_value:: ACTION_MAP  The mapping from request methods
                                             to resource actions, which is used
                                             to find the specified action to
                                             handle the request.
===========  ==============================  ==================================


Parsers and Renderers
^^^^^^^^^^^^^^^^^^^^^

================  ====================================  =============================
Option name       Default value                         Description
================  ====================================  =============================
PARSER_CLASSES    .. autodata_value:: PARSER_CLASSES    The default Parser classes.
RENDERER_CLASSES  .. autodata_value:: RENDERER_CLASSES  The default Renderer classes.
================  ====================================  =============================


Logger
^^^^^^

==================  ======================================  ====================================
Option name         Default value                           Description
==================  ======================================  ====================================
LOGGER_ENABLED      .. autodata_value:: LOGGER_ENABLED      Enable or disable the global logger.
LOGGER_METHODS      .. autodata_value:: LOGGER_METHODS      A sequence of HTTP methods whose
                                                            messages should be logged.
LOGGER_LEVEL        .. autodata_value:: LOGGER_LEVEL        The logging level.
LOGGER_FORMAT       .. autodata_value:: LOGGER_FORMAT       The logging format for strings.
LOGGER_DATE_FORMAT  .. autodata_value:: LOGGER_DATE_FORMAT  The logging format for date/time.
==================  ======================================  ====================================


Middlewares
^^^^^^^^^^^

==================  ======================================  ====================================
Option name         Default value                           Description
==================  ======================================  ====================================
MIDDLEWARE_CLASSES  .. autodata_value:: MIDDLEWARE_CLASSES  The middleware classes used to alter
                                                            RESTArt's requests and responses.
==================  ======================================  ====================================


CORS (Cross-Origin Resource Sharing)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

======================  ==========================================  =====================================
Option name             Default value                               Description
======================  ==========================================  =====================================
CORS_ALLOW_ORIGIN       .. autodata_value:: CORS_ALLOW_ORIGIN       The option that determines the header
                                                                    ``Access-Control-Allow-Origin``.
CORS_ALLOW_CREDENTIALS  .. autodata_value:: CORS_ALLOW_CREDENTIALS  The option that determines the header
                                                                    ``Access-Control-Allow-Credentials``.
CORS_ALLOW_METHODS      .. autodata_value:: CORS_ALLOW_METHODS      The option that determines the header
                                                                    ``Access-Control-Allow-Methods``.
CORS_ALLOW_HEADERS      .. autodata_value:: CORS_ALLOW_HEADERS      The option that determines the header
                                                                    ``Access-Control-Allow-Headers``.
CORS_MAX_AGE            .. autodata_value:: CORS_MAX_AGE            The option that determines the header
                                                                    ``Access-Control-Max-Age``.
======================  ==========================================  =====================================


Customization
-------------

You can customize all of the above configuraion options by following the steps below:

1. Create a Python module to set your preferred values::

    $ vi restart_config.py

    LOGGER_METHODS = ['POST', 'PUT', 'PATCH']
    LOGGER_LEVEL = 'DEBUG'

2. Set the environment variable ``RESTART_CONFIG_MODULE`` to the Python path of the above module::

    $ export RESTART_CONFIG_MODULE=pythonpath.to.restart_config

That's all. Then, while your API is running, messages with DEBUG (or higher) level will be logged for any request whose HTTP method is `POST`, `PUT` or `PATCH`.
