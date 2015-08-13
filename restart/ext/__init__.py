class ExtensionImporter(object):
    """This importer object redirects imports from ``original_module`` to
    ``target_module``.
    More specifically, when a user does ``from restart.ext.foo import bar``,
    the importer will actually do ``from restart_foo import bar`` instead.

    Inspired by `Flask`.
    """

    sys = __import__('sys')
    importlib = __import__('importlib')

    def __init__(self, target_module, original_module):
        self.target_module = target_module
        self.original_module = original_module
        self.prefix = original_module + '.'
        self.prefix_cutoff = original_module.count('.') + 1

    def install(self):
        if self not in self.sys.meta_path:
            self.sys.meta_path.append(self)

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.prefix):
            return self

    def load_module(self, fullname):
        # Check the cache first
        if fullname in self.sys.modules:
            return self.sys.modules[fullname]

        modname = fullname.split('.', self.prefix_cutoff)[self.prefix_cutoff]
        realname = self.target_module % modname
        module = self.importlib.import_module(realname)

        # Map `fullname` to `module` (used as a cache later)
        self.sys.modules[fullname] = module

        return module


# Install the importer
importer = ExtensionImporter('restart_%s', __name__)
importer.install()


# Delete all symbols
del importer
del ExtensionImporter
