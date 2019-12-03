import logging

from requests import Session, Request

from urllib.parse import urlparse, quote_plus
from . import Document, Query, Content
from .. import constants
from rendertron_cache_server import get_logger
from rendertron_cache_server.utils import *


class Resource:
    session: Session
    logger: logging.Logger

    def __init__(self) -> None:
        self.session = Session()
        self.logger = get_logger()

    def retrieve(self, doc: Document, q: Query) -> Content:
        """Request rendertron server for a url"""
        # Set host so server knows which website to serve
        host = urlparse(q.url).netloc
        q.headers['Host'] = host if host else urlparse(constants.RENDERTRON_CACHE_RESOURCE_URL).netloc

        # Quote target url so rendetron doesnt confuse anything
        url_parts = q.url.split('?')
        url = f'{constants.RENDERTRON_CACHE_RESOURCE_URL}/{url_parts[0]}'
        if len(url_parts) > 1: url += quote_plus(f'?{url_parts[1]}')

        # Retrive resource
        self.logger.log(logging.DEBUG, f'[MISS] Retrieving resource {url}')
        request = Request(
            method=constants.RENDERTRON_CACHE_RESOURCE_METHOD,
            url=url,
            headers=q.headers
        ).prepare()
        response = self.session.send(request)

        # Transform response into a document
        headers = filter_dict(response.headers, constants.RENDERTRON_CACHE_HEADER_RESPONSE_BLACKLIST)
        content = Content(response.status_code, headers, response.text)

        self.logger.log(logging.DEBUG, f'[MISS] Retrieved resource {request.url} - {response.status_code}')

        if response.status_code // 100 == 2:
            doc.write(content)

        return content
