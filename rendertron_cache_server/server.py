from typing import Tuple

import logging
from flask import Flask, Response, request
from rendertron_cache_server import cache, log, lremove, rremove


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

    def add_subroute(self, name, callback, methods):
        self.app.add_url_rule('/', name, callback, methods=methods, defaults={'path': ''}, )
        self.app.add_url_rule('/<path:path>', name, callback, methods=methods)

    def start(self):
        self.app.run(threaded=False)

    def get_app(self):
        return self.app
    
    def _request_doc(self) -> Tuple[cache.Query, cache.Document]:
        headers = {k: v for k, v in request.headers.items()}

        url = rremove(request.path, '/')
        url = lremove(url, '/render/')
        if url.find('://') < 0 and url.find(':/') >= 0:
            url = url.replace(':/', '://')

        query = cache.Query(url, request.args, headers)
        document = self.cache.query(query)
        return query, document

    def retrieve_cache(self, path) -> Response:
        try:
            query, document = self._request_doc()
            self.logger.log(logging.INFO, f'Requesting {query.route}')
            content = self.cache.retrieve(document, query)
            return Response(content.content, status=content.status, headers=content.headers)
        except Exception as e:
            self.logger.log(logging.ERROR, e)
            return Response(response='Cache server error', status=404)

    def refresh_cache(self, path) -> Response:
        try:
            query, document = self._request_doc()
            self.logger.log(logging.INFO, f'Refreshing {query.route}')
            content = self.cache.refresh(document, query)
            return Response(content.content, status=content.status, headers=content.headers)
        except Exception as e:
            self.logger.log(logging.ERROR, e)
            return Response(response='Cache server error', status=404)

    def purge_cache(self, path) -> Response:
        try:
            query, document = self._request_doc()
            self.cache.purge(document, query)
            self.logger.log(logging.INFO, f'Purging {query.route}')
            return Response('Purged cache', status=200)
        except Exception as e:
            self.logger.log(logging.ERROR, e)
            return Response(response='Cache server error', status=404)