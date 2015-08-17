from __future__ import absolute_import

import pytest

from restart.renderers import Renderer, JSONRenderer


class TestRenderers(object):

    def test_renderer(self):
        renderer = Renderer()

        with pytest.raises(NotImplementedError):
            renderer.render({'hello': 'world'})

    def test_json_renderer(self):
        renderer = JSONRenderer()
        rendered = renderer.render({'hello': 'world'})

        assert rendered == '{"hello": "world"}'
