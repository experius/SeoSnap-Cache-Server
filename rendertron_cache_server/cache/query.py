import urllib.parse
from typing import Dict

from rendertron_cache_server.utils import *
from .. import constants


def parse_url(urls):
    pass


class Query:
    url: str
    headers: Dict[str, str]

    def __init__(self, url: str, headers: Dict[str, str]) -> None:
        self.url = url
        self.headers = headers

    def get_key(self, suffix=True) -> str:
        """Builds a key used to store the document"""
        key = strip_schema(self.url)
        if suffix:
            key += constants.RENDERTRON_CACHE_FILE_SUFFIX
        return key
