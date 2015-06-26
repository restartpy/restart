# The mapping of request methods to resource actions.
ACTION_MAP = {
    'POST': 'create',
    'GET': 'read',
    'PUT': 'replace',
    'PATCH': 'update',
    'DELETE': 'delete',
    'OPTIONS': 'options',
    'HEAD': 'head',
    'TRACE': 'trace',
}


# The default Parser class and Renderer class
PARSER_CLASS = 'restart.parser.JSONParser'
RENDERER_CLASS = 'restart.renderer.JSONRenderer'


# The settings for the global logger
LOGGER_ENABLED = True
LOGGER_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
LOGGER_LEVEL = 'INFO'
LOGGER_FORMAT = '%(asctime)s.%(msecs)03d %(name)-10s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
