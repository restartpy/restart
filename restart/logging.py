from __future__ import absolute_import

from logging import getLogger, StreamHandler, NullHandler, Formatter


def create_logger(name=None, handler_class=StreamHandler,
                  level='DEBUG', fmt=None, datefmt=None):
    """Create a logger with the specified attributes."""
    handler = handler_class()
    handler.setFormatter(Formatter(fmt, datefmt))

    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def create_logger_from_config(name=None):
    """Create a logger with attributes from the configuration."""
    from .config import config
    logger = create_logger(
        name,
        StreamHandler if config.LOGGER_ENABLED else NullHandler,
        config.LOGGER_LEVEL,
        config.LOGGER_FORMAT,
        config.LOGGER_DATE_FORMAT
    )
    return logger


# The global logger for RESTArt
global_logger = create_logger_from_config('restart')
