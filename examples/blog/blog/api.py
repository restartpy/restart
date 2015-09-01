from __future__ import absolute_import

from restart.api import RESTArt
from restart.utils import load_resources


api = RESTArt()


# Load all resources
load_resources(['blog.resources.*.resource'])
