from typing import Tuple

import logging
from functools import wraps
from flask import Flask, Response, request
from rendertron_cache_server import cache, log
from rendertron_cache_server.utils import *


def document_middleware(f):
    """Adds query and document as arguments to the route function"""
    @wraps(f)
    def middleware(server, *args, **kwargs):
        query, document = request_to_doc(server)
        return f(server, query, document)
    return middleware


class Server:
    app: Flask
    cache: cache.Cache
    logger: logging.Logger

    def __init__(self) -> None:
        self.logger = log.get_logger()
        self.cache = cache.Cache(cache.Resource())
        self.app = Flask('RENDERTRON_CACHE_SERVER')
        self.add_subroute('retrieve_cache', self.retrieve_cache, methods=['GET'])
        self.add_subroute('refresh_cache', self.refresh_cache, methods=['PUT'])
        self.add_subroute('purge_cache', self.purge_cache, methods=['DELETE'])
        self.add_error_handler()

    def add_error_handler(self):
        @self.app.errorhandler(Exception)
        def handle_error(e: Exception):
            self.logger.exception(e, exc_info=True)
            return Response(response='Cache server error', status=404)

    def add_subroute(self, name, callback, methods):
        self.app.add_url_rule('/', name, callback, methods=methods, defaults={'path': ''}, )
        self.app.add_url_rule('/<path:path>', name, callback, methods=methods)

    def start(self):
        self.app.run(threaded=False)

    def get_app(self):
        return self.app

    @document_middleware
    def retrieve_cache(self, query, document) -> Response:
        """Retrieves a document from cache. If miss then cache it"""
        self.logger.log(logging.INFO, f'[Server] Requesting {query.url}')
        content = self.cache.retrieve(document, query)
        return Response(content.content, status=content.status, headers=content.headers)

    @document_middleware
    def refresh_cache(self, query, document) -> Response:
        """Deletes the cached document then retrieves it"""
        self.logger.log(logging.INFO, f'[Server] Refreshing {query.url}')
        content = self.cache.refresh(document, query)
        return Response(content.content, status=content.status, headers=content.headers)

    @document_middleware
    def purge_cache(self, query, document) -> Response:
        """Deletes a document and its children"""
        self.cache.purge(document, query)
        self.logger.log(logging.INFO, f'[Server] Purging {query.url}')
        return Response('Purged cache', status=200)


def request_to_doc(server: Server) -> Tuple[cache.Query, cache.Document]:
    """Extracts a rendertron query and a document from current request"""
    headers = dict(request.headers.items())
    route = extract_route(request.url)
    url = extract_route_url(route)

    query = cache.Query(url, headers)
    document = server.cache.query(query)
    return query, document
