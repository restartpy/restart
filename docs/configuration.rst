.. _configuration:

Configuration
=============

This section covers all configuration options for you to customize the behavior of RESTArt APIs.


Options
-------

.. module:: restart.config.default


Action mapping
^^^^^^^^^^^^^^

===========  ==============================  ==================================
Option name  Default value                   Description
===========  ==============================  ==================================
ACTION_MAP   .. autodata_value:: ACTION_MAP  .. autodata_docstring:: ACTION_MAP
===========  ==============================  ==================================


Parser and Renderer
^^^^^^^^^^^^^^^^^^^

==============  ==================================  ======================================
Option name     Default value                       Description
==============  ==================================  ======================================
PARSER_CLASS    .. autodata_value:: PARSER_CLASS    .. autodata_docstring:: PARSER_CLASS
RENDERER_CLASS  .. autodata_value:: RENDERER_CLASS  .. autodata_docstring:: RENDERER_CLASS
==============  ==================================  ======================================


Logger
^^^^^^^^^^^^^^^^^^^

==================  ======================================  ==========================================
Option name         Default value                           Description
==================  ======================================  ==========================================
LOGGER_ENABLED      .. autodata_value:: LOGGER_ENABLED      .. autodata_docstring:: LOGGER_ENABLED
LOGGER_METHODS      .. autodata_value:: LOGGER_METHODS      .. autodata_docstring:: LOGGER_METHODS
LOGGER_LEVEL        .. autodata_value:: LOGGER_LEVEL        .. autodata_docstring:: LOGGER_LEVEL
LOGGER_FORMAT       .. autodata_value:: LOGGER_FORMAT       .. autodata_docstring:: LOGGER_FORMAT
LOGGER_DATE_FORMAT  .. autodata_value:: LOGGER_DATE_FORMAT  .. autodata_docstring:: LOGGER_DATE_FORMAT
==================  ======================================  ==========================================


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
