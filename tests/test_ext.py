from __future__ import absolute_import

import os
import sys
import shutil
import tempfile


def mkdir(path):
    os.mkdir(path)


def mkfile(path, content=''):
    with open(path, 'w') as f:
        f.write(content)


class TestUtils(object):

    def setup_class(cls):
        cls.tempdir = tempfile.mkdtemp()

        # build the directory structure
        origin_cwd = os.getcwd()
        os.chdir(cls.tempdir)

        # restart extension module
        mkfile('restart_module.py', 'ext_id = "restart_module"')

        # restart extension package
        mkdir('restart_package')
        mkfile('restart_package/__init__.py', 'ext_id = "restart_package"')
        mkfile('restart_package/module.py', 'mod_id = "restart_package_module"')

        os.chdir(origin_cwd)

        # add cls.tempdir into sys.path
        sys.path.insert(0, cls.tempdir)

    def teardown_class(cls):
        sys.path.remove(cls.tempdir)
        shutil.rmtree(cls.tempdir)

    def test_restart_ext_module_import_normal(self):
        from restart.ext.module import ext_id
        assert ext_id == 'restart_module'

    def test_restart_ext_module_import_module(self):
        from restart.ext import module
        assert module.ext_id == 'restart_module'
        assert module.__name__ == 'restart_module'

    def test_restart_ext_package_import_normal(self):
        from restart.ext.package import ext_id
        assert ext_id == 'restart_package'

    def test_restart_ext_package_import_module(self):
        from restart.ext import package
        assert package.ext_id == 'restart_package'
        assert package.__name__ == 'restart_package'

    def test_restart_ext_package_import_inner_normal(self):
        from restart.ext.package.module import mod_id
        assert mod_id == 'restart_package_module'

    def test_restart_ext_package_import_inner_module(self):
        from restart.ext.package import module
        assert module.mod_id == 'restart_package_module'
        assert module.__name__ == 'restart_package.module'
