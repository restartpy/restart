# -- Server --

#: The server name (scheme + domain + port)
SERVER_NAME = ''


# -- Action mapping --

#: The mapping from request methods to resource actions, which is
#: used to find the specified action to handle the request.
ACTION_MAP = {
    'POST': 'create',
    'GET': 'read',
    'PUT': 'replace',
    'PATCH': 'update',
    'DELETE': 'delete',
    'OPTIONS': 'options',
    'HEAD': 'head',
    'TRACE': 'trace'
}


# -- Parser and Renderer --

#: The default Parser classes.
PARSER_CLASSES = (
    'restart.parsers.JSONParser',
    'restart.parsers.URLEncodedParser',
    'restart.parsers.MultiPartParser',
)

#: The default Renderer classes.
RENDERER_CLASSES = (
    'restart.renderers.JSONRenderer',
)


# -- Logger --

#: Enable or disable the global logger.
LOGGER_ENABLED = True

#: A sequence of HTTP methods whose messages should be logged
LOGGER_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

#: The logging level.
LOGGER_LEVEL = 'INFO'

#: The logging format for strings.
LOGGER_FORMAT = '%(asctime)s.%(msecs)03d %(name)-10s %(levelname)-8s %(message)s'

#: The logging format for date/time.
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


# -- Middlewares --

#: The middleware classes used to alter RESTArt's requests and responses.
MIDDLEWARE_CLASSES = ()


# -- CORS (Cross-Origin Resource Sharing) --

#: Access control options for CORS
CORS_ALLOW_ORIGIN = '*'  # any domain
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
CORS_ALLOW_HEADERS = ()  # any headers
CORS_MAX_AGE = 864000  # 10 days
