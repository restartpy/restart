from __future__ import absolute_import

from werkzeug.utils import import_string

from .config import config
from .negotiator import Negotiator
from .response import Response
from . import exceptions
from .utils import locked_cached_classproperty


class Resource(object):
    """The core class that represents a REST resource.

    :param action_map: the mapping of request methods to resource actions.
    """

    #: The name of the resource.
    name = None

    #: The parser classes used for parsing request data.
    parser_classes = tuple(
        import_string(parser_class)
        for parser_class in config.PARSER_CLASSES
    )

    #: The renderer classes used for rendering response data.
    renderer_classes = tuple(
        import_string(renderer_class)
        for renderer_class in config.RENDERER_CLASSES
    )

    #: The class used to select the proper parser or renderer
    negotiator_class = Negotiator

    #: The resource-level middleware classes
    middleware_classes = ()

    def __init__(self, action_map):
        self.action_map = action_map

    @locked_cached_classproperty(name='_middlewares')
    def middlewares(cls):
        """The instances of all middleware classes.

        The final order of middleware classes:
            The first is global middleware classes (in order) and
            then is resource-level middleware classes (in order).
        """
        global_middleware_classes = tuple(
            import_string(middleware_class_string)
            for middleware_class_string in config.MIDDLEWARE_CLASSES
        )
        middleware_classes = global_middleware_classes + cls.middleware_classes
        return tuple(
            middleware_class()
            for middleware_class in middleware_classes
        )

    @property
    def logger(self):
        """A :class:`logging.Logger` object for this API."""
        from .logging import global_logger
        return global_logger

    def _get_head(self):
        """Get the head message for logging."""
        query_string = self.request.environ['QUERY_STRING']
        separator = '?' if query_string else ''
        head = '[%s %s%s%s]' % (self.request.method, self.request.path,
                                separator, query_string)
        return head

    def log_message(self, msg):
        """Logs a message with `DEBUG` level.

        :param msg: the message to be logged.
        """
        if self.request.method in config.LOGGER_METHODS:
            self.logger.debug('%s %s' % (self._get_head(), msg))

    def log_exception(self, exc):
        """Logs an exception with `ERROR` level.

        :param exc: the exception to be logged.
        """
        self.logger.exception('Exception on %s' % self._get_head())

    def dispatch_request(self, request, *args, **kwargs):
        """Does the request dispatching. Matches the HTTP method and return
        the return value of the bound action.

        :param request: the request object.
        :param args: the positional arguments captured from the URI.
        :param kwargs: the keyword arguments captured from the URI.
        """
        negotiator = self.negotiator_class()
        self.format_suffix = kwargs.pop('format', None)

        self.request = request.parse(negotiator, self.parser_classes)
        self.log_message('<Request> %s' % request.data)

        try:
            rv = self.perform_action(*args, **kwargs)
        except Exception as exc:
            rv = self.handle_exception(exc)

        response = self.make_response(rv)
        self.log_message('<Response> %s %s' % (response.status, response.data))

        return response.render(negotiator, self.renderer_classes,
                               self.format_suffix)

    def http_method_not_allowed(self, request, *args, **kwargs):
        """The default action handler if the corresponding action for
        `request.method` is not implemented.

        See :meth:`dispatch_request` for the meanings of the parameters.
        """
        raise exceptions.MethodNotAllowed()

    def find_action(self, request):
        """Find the appropriate action according to the request method.

        :param request: the request object.
        """
        try:
            action_name = self.action_map[request.method]
        except KeyError as exc:
            exc.args = (
                'Config `ACTION_MAP` has no mapping for %r' % request.method,
            )
            raise

        action = getattr(self, action_name, self.http_method_not_allowed)
        return action

    def perform_action(self, *args, **kwargs):
        """Perform the appropriate action. Also apply all possible `process_*`
        methods of middleware instances in `self.middlewares`.

        During request phase:

            :meth:`process_request` methods are called on each request,
            before RESTArt calls the `action`, in order.

            It should return :attr:`None` or any other value that
            :attr:`~restart.resource.Resource.make_response` can recognize.
            If it returns :attr:`None`, RESTArt will continue processing
            the request, executing any other :meth:`process_request` and,
            then, the `action`. If it returns any other value (e.g.
            a :class:`~restart.response.Response` object), RESTArt won't
            bother calling any other middleware or the `action`.

        During response phase:

            :meth:`process_response` methods are called on all responses
            before they'are returned to the client, in reverse order.

            It must return a value that can be converted to a
            :class:`~restart.response.Response` object by
            :attr:`~restart.resource.Resource.make_response`. It could alter
            and return the given `response`, or it could create and return
            a brand-new value.

            Unlike :meth:`process_request` methods, the
            :meth:`process_response` method is always called, even if the
            :meth:`process_request` of the same middleware were skipped
            (because an earlier middleware method returned a
            :class:`~restart.response.Response`).

        :param args: a list of positional arguments that will be passed
                     to the action.
        :param kwargs: a dictionary of keyword arguments that will be passed
                       to the action.
        """
        rv = None

        # Call possible `process_request` methods of middlewares
        for middleware in self.middlewares:
            if hasattr(middleware, 'process_request'):
                rv = middleware.process_request(self.request)
                if rv is not None:
                    break

        # Call the `action`
        if rv is None:
            action = self.find_action(self.request)
            rv = action(self.request, *args, **kwargs)

        # Call all `process_response` methods of middlewares
        for middleware in reversed(self.middlewares):
            if hasattr(middleware, 'process_response'):
                # Ensure that the second parameter passed to the
                # `process_response` method is a `Response` object
                response = self.make_response(rv)
                rv = middleware.process_response(self.request, response)

        return rv

    def handle_exception(self, exc):
        """Handle any exception that occurs, by returning an appropriate
        response, or re-raising the error.

        :param exc: the exception to be handled.
        """
        if isinstance(exc, exceptions.HTTPException):
            headers = dict(exc.get_headers(self.request.environ))
            rv = ({'message': exc.description}, exc.code, headers)
            return rv
        else:
            self.log_exception(exc)
            raise

    def make_response(self, rv):
        """Converts the return value to a real response object that is
        an instance of :class:`~restart.response.Response`.

        The following types are allowed for `rv`:

        ======================  ============================================
        :class:`Response`       the object is returned unchanged
        :class:`str`            the string becomes the response body
        :class:`unicode`        the unicode string becomes the response body
        :class:`tuple`          A tuple in the form ``(data, status)``
                                or ``(data, status, headers)`` where
                                `data` is the response body, `status` is
                                an integer and `headers` is a dictionary
                                with header values.
        ======================  ============================================
        """
        status = 200
        headers = None

        if isinstance(rv, tuple):
            rv_len = len(rv)
            if rv_len == 2:
                rv, status = rv
            elif rv_len == 3:
                rv, status, headers = rv
            else:
                raise ValueError('Resource action return a wrong response')

        if rv is None:
            raise ValueError('Resource action did not return a response')
        elif not isinstance(rv, Response):
            rv = Response(rv, status=status, headers=headers)

        return rv
