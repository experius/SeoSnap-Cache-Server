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

    def get_key(self) -> str:
        route = self.route.lstrip('/').rstrip('/')
        suffix = constants.RENDERTRON_CACHE_FILE_SUFFIX
        key = route
        if len(self.params) != 0:
            params = urllib.parse.urlencode(self.params)
            key += f'?{params}'
        key += constants.RENDERTRON_CACHE_FILE_SUFFIX
        return key
