import logging
from typing import Callable

from requests import Session, Request, Response

from datetime import datetime
from urllib.parse import urlparse, quote_plus
from . import Document, Query, Content
from .. import constants
from rendertron_cache_server import get_logger
from rendertron_cache_server.utils import *


class Resource:
    session: Session
    logger: logging.Logger
    after_retrieve_fn: Callable[[Content], Content]

    def __init__(self) -> None:
        self.session = Session()
        self.logger = get_logger()

        try:
            from plugins import after_retrieve
            self.after_retrieve_fn = after_retrieve
            print('Plugin found: after_retrieve')
        except Exception as e:
            print(e)  # No plugins found. Do nothing

    def retrieve(self, doc: Document, q: Query) -> Content:
        """Request rendertron server for a url"""
        # Set host so server knows which website to serve
        host = urlparse(q.url).netloc
        q.headers['Host'] = host if host else urlparse(constants.RENDERTRON_CACHE_RESOURCE_URL).netloc

        # Quote target url so rendetron doesnt confuse anything
        url_parts = q.url.split('?')
        url = f'{constants.RENDERTRON_CACHE_RESOURCE_URL}/{url_parts[0]}'
        if len(url_parts) > 1: url += quote_plus(f'?{url_parts[1]}')

        # Append a rendertron no cache parameter
        url += '?refreshCache=true'

        # Retrive resource
        self.logger.log(logging.DEBUG, f'[MISS] Retrieving resource {url}')
        request = Request(
            method=constants.RENDERTRON_CACHE_RESOURCE_METHOD,
            url=url,
            headers=q.headers
        ).prepare()
        response = self.session.send(request)

        # Transform response into a document
        cached_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        headers = filter_dict(response.headers, constants.RENDERTRON_CACHE_HEADER_RESPONSE_BLACKLIST)
        content = Content(response.status_code, headers, response.text, cached_at)

        self.logger.log(logging.DEBUG, f'[MISS] Retrieved resource {request.url} - {response.status_code}')

        if response.status_code // 100 == 2 or response.status_code in constants.RENDERTRON_CACHE_ALLOWED_STATUS:
            doc.write(content)

        if self.after_retrieve_fn:
            content = self.after_retrieve_fn(content)
        return content
