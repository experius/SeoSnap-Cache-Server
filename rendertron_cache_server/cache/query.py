import urllib.parse
from typing import Dict
from .. import constants

class Query:
    route: str
    params: Dict[str, str]
    headers: Dict[str, str]

    def __init__(self, route: str, params: Dict[str, str], headers: Dict[str, str]) -> None:
        self.route = route
        self.params = params
        self.headers = headers

    def get_key(self, suffix=True) -> str:
        route = lremove(self.route.lstrip('/').rstrip('/'), 'render').lstrip('/')
        route = lremove(lremove(route, 'http://'), 'https://')
        key = route
        if len(self.params) != 0:
            params = urllib.parse.urlencode(self.params)
            key += f'?{params}'
        if suffix:
            key += constants.RENDERTRON_CACHE_FILE_SUFFIX
        return key


def lremove(s, pattern) -> str:
    if s.startswith(pattern):
        s = s[len(pattern):]
    return s