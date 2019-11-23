import json
import logging
import logging.config
import os

from . import constants


def init():
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log_config.json')
    logging.config.dictConfig(json.load(open(config_file, 'r')))
    get_logger().setLevel(logging.INFO if not constants.RENDERTRON_CACHE_DEBUG else logging.DEBUG)


def get_logger():
    return logging.getLogger()