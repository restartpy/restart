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
