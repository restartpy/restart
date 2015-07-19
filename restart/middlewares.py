from __future__ import absolute_import

from .config import config


class CORSMiddleware(object):
    """The middleware used for CORS (Cross-Origin Resource Sharing).

    The CORS behaviors are implemented according to the guidelines from
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
    """

    def make_preflight_headers(self, request_headers, allow_origin=None,
                               allow_credentials=None, allow_methods=None,
                               allow_headers=None, max_age=None):
        """Make reasonable CORS response headers for preflight requests.
        """
        if allow_origin is None:
            allow_origin = config.CORS_ALLOW_ORIGIN
        if allow_credentials is None:
            allow_credentials = config.CORS_ALLOW_CREDENTIALS
        if allow_methods is None:
            allow_methods = config.CORS_ALLOW_METHODS
        if allow_headers is None:
            allow_headers = config.CORS_ALLOW_HEADERS
            if not allow_headers and request_headers is not None:
                allow_headers = request_headers.split(', ')
        if max_age is None:
            max_age = config.CORS_MAX_AGE

        headers = {
            'Access-Control-Allow-Origin': allow_origin,
            'Access-Control-Allow-Methods': ', '.join(allow_methods),
            'Access-Control-Max-Age': '%d' % max_age,
        }
        if allow_headers:
            headers.update({
                'Access-Control-Allow-Headers': ', '.join(allow_headers)
            })
        if allow_credentials:
            headers.update({'Access-Control-Allow-Credentials': 'true'})
        if allow_origin != '*':
            headers.update({'Vary': 'Origin'})

        return headers

    def make_actual_headers(self, allow_origin=None, allow_credentials=None):
        """Make reasonable CORS response headers for actual requests.
        """
        if allow_origin is None:
            allow_origin = config.CORS_ALLOW_ORIGIN
        if allow_credentials is None:
            allow_credentials = config.CORS_ALLOW_CREDENTIALS

        headers = {
            'Access-Control-Allow-Origin': allow_origin,
        }
        if allow_credentials:
            headers.update({'Access-Control-Allow-Credentials': 'true'})
        if allow_origin != '*':
            headers.update({'Vary': 'Origin'})

        return headers

    def is_preflight_request(self, request):
        """Judge if the `request` object is a preflight request."""
        return (request.method == 'OPTIONS' and
                'Origin' in request.headers and
                'Access-Control-Request-Method' in request.headers)

    def process_request(self, request):
        """Handle the preflight request correctly.

        :param request: the request object.
        """
        if self.is_preflight_request(request):
            request_headers = request.headers.get(
                'Access-Control-Request-Headers'
            )
            headers = self.make_preflight_headers(request_headers)
            return '', 200, headers

    def process_response(self, request, response):
        """Add appropriate response headers for the actual request.

        :param request: the request object.
        :param response: the response object.
        """
        if not self.is_preflight_request(request):
            headers = self.make_actual_headers()
            response.headers.update(headers)
        return response
