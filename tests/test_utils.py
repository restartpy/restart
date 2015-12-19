from __future__ import absolute_import

import os
import sys
import uuid
import shutil
import tempfile

import six
import pytest

from restart.utils import (
    load_resources, expand_wildcards,
    locked_cached_property, classproperty,
    locked_cached_classproperty, make_location_header
)


def mkdir(path):
    os.mkdir(path)


def mkfile(path):
    open(path, 'w').close()


class TestUtils(object):

    def setup_class(cls):
        cls.tempdir = tempfile.mkdtemp()

        # build the directory structure
        origin_cwd = os.getcwd()
        os.chdir(cls.tempdir)

        mkdir('testapi')
        mkfile('testapi/__init__.py')
        mkdir('testapi/resources')
        mkfile('testapi/resources/__init__.py')
        mkdir('testapi/resources/users')
        mkfile('testapi/resources/users/__init__.py')
        mkfile('testapi/resources/users/resource.py')
        mkdir('testapi/resources/orders')
        mkfile('testapi/resources/orders/__init__.py')
        mkfile('testapi/resources/orders/resource.py')

        os.chdir(origin_cwd)

        # add cls.tempdir into sys.path
        sys.path.insert(0, cls.tempdir)

    def teardown_class(cls):
        sys.path.remove(cls.tempdir)
        shutil.rmtree(cls.tempdir)

    def test_load_resources(self):
        load_resources(['testapi.resources.users.resource'])

    def test_load_resources_with_nonexistent_module_names(self):
        with pytest.raises(ImportError):
            load_resources(['testapi.resources.counts.resource'])

    def test_load_resources_with_wildcards_module_names(self):
        load_resources(['testapi.resources.*.resource'])

    def test_load_resources_with_nonexistent_wildcards_module_names(self):
        module_name = 'testapi.resources.users.*.resource'
        with pytest.raises(ImportError) as exc:
            load_resources([module_name])
        expected_exc_msg = 'No module found with wildcards %r' % module_name
        assert str(exc.value) == expected_exc_msg

    def test_expand_wildcards(self):
        module_names = expand_wildcards('testapi.resources.*.resource')
        assert module_names == ['testapi.resources.users.resource',
                                'testapi.resources.orders.resource']

        module_names = expand_wildcards('testapi.*.*.resource')
        assert module_names == ['testapi.resources.users.resource',
                                'testapi.resources.orders.resource']

    def test_expand_wildcards_with_nonexistent_module_name(self):
        module_names = expand_wildcards('testapi.resources.users.*.resource')
        assert not module_names

    def test_expand_wildcards_package(self):
        module_names = expand_wildcards('testapi.resources.*')
        assert module_names == ['testapi.resources',
                                'testapi.resources.users',
                                'testapi.resources.orders']

    def test_locked_cached_property(self):
        class Sample(object):
            @locked_cached_property
            def identifier(self):
                return str(uuid.uuid4())

        s = Sample()
        assert s.identifier == s.identifier

    def test_locked_cached_property_with_alias(self):
        class Sample(object):
            @locked_cached_property(name='_identifier')
            def identifier(self):
                return str(uuid.uuid4())

        s = Sample()
        assert s.identifier == s.identifier

        s._identifier = 'foo'
        assert s.identifier == 'foo'

    def test_classproperty(self):
        class Sample(object):
            _name = 'sample'

            @classproperty
            def name(cls):
                return cls._name

        assert Sample.name == 'sample'

        class SubSample(Sample):
            _name = 'sub_sample'

        assert SubSample.name == 'sub_sample'

    def test_locked_cached_classproperty_vs_classproperty(self):
        class Sample(object):
            @locked_cached_classproperty
            def static(cls):
                return str(uuid.uuid4())

            @classproperty
            def dynamic(cls):
                return str(uuid.uuid4())

        assert isinstance(Sample.static, six.string_types)
        assert Sample.static == Sample.static

        assert isinstance(Sample.dynamic, six.string_types)
        assert Sample.dynamic != Sample.dynamic

    def test_locked_cached_classproperty_with_default_alias(self):
        class Sample(object):
            @locked_cached_classproperty
            def static(cls):
                return str(uuid.uuid4())

        assert isinstance(Sample.static, six.string_types)
        assert Sample.static == Sample.static

        # The property value always equals the value of its alias property
        assert Sample.static == Sample._locked_cached_classproperty_static

        # Even if the value of the alias property changes
        Sample._locked_cached_classproperty_static = 'changed'
        assert Sample.static == 'changed'

    def test_locked_cached_classproperty_with_specified_alias(self):
        class Sample(object):
            @locked_cached_classproperty(name='_static')
            def static(cls):
                return str(uuid.uuid4())

        assert isinstance(Sample.static, six.string_types)
        assert Sample.static == Sample.static

        # The property value always equals the value of its alias property
        assert Sample.static == Sample._static

        # Even if the value of the alias property changes
        Sample._static = 'changed'
        assert Sample.static == 'changed'

    def test_make_location_header(self):
        from restart.testing import RequestFactory
        factory = RequestFactory()
        request = factory.post('/tests', data={})
        assert 'http://localhost/tests/1' == make_location_header(request, 1)
        assert ('http://localhost/tests/id' ==
                make_location_header(request, 'id'))
