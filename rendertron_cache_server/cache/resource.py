import logging

from requests import Session, Request

import urllib
from urllib.parse import urlparse
from . import Document, Query, Content
from .. import constants
from rendertron_cache_server import get_logger
import os

class Resource:
    session: Session
    logger: logging.Logger

    def __init__(self) -> None:
        self.session = Session()
        self.logger = get_logger()


    def retrieve(self, doc: Document, q: Query) -> Content:
        host = urlparse(q.route).netloc
        q.headers['Host'] = host if host else urlparse(constants.RENDERTRON_CACHE_RESOURCE_URL).netloc

        url = f'{constants.RENDERTRON_CACHE_RESOURCE_URL}/{q.route}'
        if len(q.params) > 0:
            params = urllib.parse.urlencode(q.params)
            url += urllib.parse.quote_plus(f'?{params}')

        self.logger.log(logging.DEBUG, f'[MISS] Retrieving resource {url}')
        request = Request(
            method=constants.RENDERTRON_CACHE_RESOURCE_METHOD,
            url=url,
            headers=q.headers
        ).prepare()

        response = self.session.send(request)
        headers = {k: v for k, v in response.headers.items() if k.lower() not in constants.RENDERTRON_CACHE_HEADER_RESPONSE_BLACKLIST}
        content = Content(response.status_code, headers, response.text)

        self.logger.log(logging.DEBUG, f'[MISS] Retrieved resource {request.url} - {response.status_code}')

        if response.status_code // 100 == 2:
            doc.write(content)

        return content
