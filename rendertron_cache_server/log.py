import json
import logging
import logging.config
import os

LOGGER_NAME = 'experius.rendertron.cache_server'


def init():
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log_config.json')
    logging.config.dictConfig(json.load(open(config_file, 'r')))


def get_logger():
    return logging.getLogger(LOGGER_NAME)
