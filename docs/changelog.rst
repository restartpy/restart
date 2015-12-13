RESTArt Changelog
=================

Here you can see the full list of changes between each RESTArt release.


Version 0.1.1 - Dev
-------------------

(release date to be announced)

- Refactor the Adapter module for better usage
- Add `-a, --adapter` argument to the restart utility
- Select the first renderer class if no format suffix is specified
- Add `context` keyword argument to :meth:`restart.parsers.Parser.parse` and :meth:`restart.renderers.Renderer.render`


Version 0.1.0
-------------

Released on Oct 3rd 2015.

- Add support for resource-level middleware classes
- Bind a mutable attribute (whose name starts with an underscore) to each request property
- Fix bugs for importing extensions
- Refactor the logic for parsing request data or files
- Refactor the logic for rendering response data
- Add the `SERVER_NAME` :ref:`configuration` option
- Add support for registering URIs with format suffixes
- Add changelog
- Add support for Python 2/3 compatibility
- Re-raise unhandled exceptions with their tracebacks
- Add :meth:`restart.resource.Resource.http_method_not_allowed` as the default action
- Get multiple query arguments from the request correctly


Version 0.0.8
-------------

Released on Jul 19th 2015.

- Update documentation
- Add makefile
- Add support for extension development
- Add the :class:`restart.adapter.Adapter` classes to handle framework adaptions
- Add testing tools
- Add support for Middleware
- Add support for CORS


Version 0.0.5
-------------

Released on Jun 26th 2015.

- Add :class:`restart.api.RESTArt` and :class:`restart.serving.Service`
- Refactor :class:`restart.request.Request` and :class:`restart.response.Response`
- Add :class:`restart.parsers.Parser` and :class:`restart.renderers.Renderer`
- Handle exceptions
- Add documentation
- Add more tests
- Add logging


Version 0.0.2
-------------

Released on May 17th 2015.

The first release.
