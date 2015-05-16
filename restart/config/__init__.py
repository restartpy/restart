from __future__ import absolute_import

from easyconfig import Config, envvar_object

from . import default


config = Config()
config.from_object(default)

# Override the default configuration if `RESTART_CONFIG_MODULE` is given
config.from_object(envvar_object('RESTART_CONFIG_MODULE', silent=True))
