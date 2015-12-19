RESTArt Changelog
=================

Here you can see the full list of changes between each RESTArt release.


Version 0.1.1 - Dev
-------------------

(release date to be announced)

- Refactor the Adapter module for better usage
- Add ``-a, --adapter`` argument to the restart utility
- Select the first renderer class if no format suffix is specified
- Add ``context`` keyword argument to :meth:`Parser.parse() <restart.parsers.Parser.parse>`
  and :meth:`Renderer.render() <restart.renderers.Renderer.render>`
- Use ``_locked_cached_classproperty_<method-name>`` (instead of ``<method-name>``)
  as the default name of the cached class property, which holds the calculated result for the
  :class:`locked_cached_classproperty <restart.utils.locked_cached_classproperty>`
  decorated class property
- Update documentation
- Update examples


Version 0.1.0
-------------

Released on Oct 3rd 2015.

- Add support for resource-level middleware classes
- Bind a mutable attribute (whose name starts with an underscore) to each request property
- Fix bugs for importing extensions
- Refactor the logic for parsing request data or files
- Refactor the logic for rendering response data
- Add the :ref:`SERVER_NAME <configuration>` configuration option
- Add support for registering URIs with format suffixes
- Add changelog
- Add support for Python 2/3 compatibility
- Re-raise unhandled exceptions with their tracebacks
- Add :meth:`http_method_not_allowed <restart.resource.Resource.http_method_not_allowed>` as the default action
- Get multiple query arguments from the request correctly


Version 0.0.8
-------------

Released on Jul 19th 2015.

- Update documentation
- Add makefile
- Add support for extension development
- Add the :class:`Adapter <restart.adapter.Adapter>` classes to handle framework adaptions
- Add testing tools
- Add support for Middleware
- Add support for CORS


Version 0.0.5
-------------

Released on Jun 26th 2015.

- Add :class:`RESTArt <restart.api.RESTArt>` and :class:`Service <restart.serving.Service>`
- Refactor :class:`Request <restart.request.Request>` and :class:`Response <restart.response.Response>`
- Add :class:`Parser <restart.parsers.Parser>` and :class:`Renderer <restart.renderers.Renderer>`
- Handle exceptions
- Add documentation
- Add more tests
- Add logging


Version 0.0.2
-------------

Released on May 17th 2015.

The first release.
