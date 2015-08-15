from __future__ import absolute_import

import os
import sys
import glob
from threading import RLock

from werkzeug.utils import import_string


def load_resources(module_names):
    """Import all modules in `module_names` to load resources.

    Example usage:
        load_resources(['yourapi.resources.users.resource'])
        load_resources(['yourapi.resources.orders.resource'])

        # the equivalent of the above two lines
        load_resources(['yourapi.resources.*.resource'])
    """
    for module_name in module_names:
        if '*' in module_name:
            actual_module_names = expand_wildcards(module_name)
            if not actual_module_names:
                raise ImportError(
                    'No module found with wildcards %r' % module_name
                )
            for actual_module_name in actual_module_names:
                import_string(actual_module_name)
        else:
            import_string(module_name)


def expand_wildcards(module_name):
    """Expand the wildcards in `module_name` based on `sys.path`.

    Suppose the directory structure of "yourapi" is as below:
        yourapi
        |-- __init__.py
        `-- resources
            |-- users
            |   |-- __init__.py
            |   `-- resource.py
            `-- orders
                |-- __init__.py
                `-- resource.py
    Then:
        expand_wildcards('yourapi.resources.*.resource')
        =>
        ['yourapi.resources.users.resource',
         'yourapi.resources.orders.resource']
    """
    for basedir in sys.path:
        modpath = module_name.replace('.', '/')
        filepath = os.path.join(basedir, modpath)
        modfile = filepath + '.py'
        pkgfile = os.path.join(filepath, '__init__.py')
        pyfiles = glob.glob(modfile) + glob.glob(pkgfile)
        if pyfiles:
            break

    modnames = []
    for pyfile in pyfiles:
        relpath = pyfile[len(basedir) + 1:]
        modpath = relpath.rstrip('/__init__.py')
        modpath = modpath.rstrip('.py')
        modname = modpath.replace('/', '.')
        modnames.append(modname)
    return modnames


class locked_cached_property(object):
    """A decorator that converts a method into a lazy property.

    The method wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value.

    This decorator has a lock for thread safety.

    Inspired by `Flask`.
    """

    # sentinel
    _missing = object()

    def __init__(self, method=None, name=None):
        self.name = name
        self.lock = RLock()

        if method is not None:
            self.__call__(method)

    def __call__(self, method):
        self.method = method
        self.name = self.name or method.__name__
        return self

    def __get__(self, obj, cls):
        if obj is None:
            return self
        with self.lock:
            value = obj.__dict__.get(self.name, self._missing)
            if value is self._missing:
                value = self.method(obj)
                obj.__dict__[self.name] = value
            return value


class classproperty(property):
    """A decorator that converts a method into a read-only class property.

    Note:
        You ought not to set the value of classproperty-decorated attributes!
        The result of the behavior is undefined.
    """

    def __init__(self, fget, *args, **kwargs):
        super(classproperty, self).__init__(classmethod(fget),
                                            *args, **kwargs)

    def __get__(self, obj, cls):
        return self.fget.__get__(obj, cls)()


class locked_cached_classproperty(locked_cached_property):
    """The lazy version of classproperty, like `locked_cached_property`.
    """

    def __init__(self, method=None, name=None):
        super(locked_cached_classproperty, self).__init__(method, name)

    def __call__(self, method):
        self.method = classproperty(method)
        self.name = self.name or method.__name__
        return self

    def __get__(self, obj, cls):
        with self.lock:
            value = cls.__dict__.get(self.name, self._missing)
            if value is self._missing:
                value = self.method.__get__(obj, cls)
                setattr(cls, self.name, value)
            return value


def make_location_header(request, pk):
    """Make the Location header for the newly-created resource.

    :param request: the POST request object.
    :param pk: the primary key of the resource.
    """
    return '%s/%s' % (request.uri.rstrip('/'), pk)
