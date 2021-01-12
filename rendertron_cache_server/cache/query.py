import urllib.parse
from typing import Dict
import re

from rendertron_cache_server.utils import *
from .. import constants


def parse_url(urls):
    pass


class Query:
    url: str
    headers: Dict[str, str]
    mobile: bool

    def __init__(self, url: str, headers: Dict[str, str], mobile: bool = False) -> None:
        self.url = url
        self.headers = headers
        self.mobile = True if 'Rendertron-Mobile' in headers else mobile
        if self.headers.get('User-Agent', None):
            self.mobile = True if re.match(constants.RENDERTRON_MOBILE_REGEX, self.headers.get('User-Agent', None))\
                else self.mobile

    def get_key(self, suffix=True) -> str:
        """Builds a key used to store the document"""
        key = strip_schema(self.url)
        if self.mobile:
            key += '.mobile'
        if suffix:
            key += constants.RENDERTRON_CACHE_FILE_SUFFIX
        return key
