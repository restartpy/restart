from __future__ import absolute_import

import os
import sys
import glob
from threading import RLock

from werkzeug.utils import import_string


def load_resources(entrypoints):
    """Import all modules in `entrypoints` to load resources.

    Example usage:
        load_resources(['yourapi.resources.users.resource'])
        load_resources(['yourapi.resources.orders.resource'])

        # the equivalent of the above two lines
        load_resources(['yourapi.resources.*.resource'])
    """
    for entrypoint in entrypoints:
        if '*' in entrypoint:
            actual_entrypoints = expand_wildcards(entrypoint)
            if not actual_entrypoints:
                raise ImportError(
                    'No module found with wildcards %r' % entrypoint
                )
            for actual_entrypoint in actual_entrypoints:
                import_string(actual_entrypoint)
        else:
            import_string(entrypoint)


def expand_wildcards(entrypoint):
    """Expand the wildcards in `entrypoint` based on `sys.path`.

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
        modpath = entrypoint.replace('.', '/')
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
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value.  Works like the one in Werkzeug but has a lock for
    thread safety.

    Borrowed from `Flask`.
    """

    # sentinel
    _missing = object()

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func
        self.lock = RLock()

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        with self.lock:
            value = obj.__dict__.get(self.__name__, self._missing)
            if value is self._missing:
                value = self.func(obj)
                obj.__dict__[self.__name__] = value
            return value
