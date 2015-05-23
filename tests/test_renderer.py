from __future__ import absolute_import

import pytest

from restart.renderer import Renderer, JSONRenderer


class TestParser(object):

    def test_parser(self):
        renderer = Renderer()

        with pytest.raises(NotImplementedError):
            renderer.render({'hello': 'world'})

    def test_json_parser(self):
        renderer = JSONRenderer()
        rendered = renderer.render({'hello': 'world'})

        assert rendered == '{"hello": "world"}'
