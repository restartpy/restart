from __future__ import absolute_import

from easyconfig import Config, str_object

from . import default


config = Config(default)

# Override the default configuration if `RESTART_CONFIG_MODULE` is given
config.load(str_object('RESTART_CONFIG_MODULE', silent=True, is_envvar=True))
