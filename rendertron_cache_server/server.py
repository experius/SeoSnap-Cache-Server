from typing import Tuple

from flask import Flask, Response, request
from rendertron_cache_server import cache


class Server:
    app: Flask
    cache: cache.Cache

    def __init__(self) -> None:
        self.cache = cache.Cache(cache.Resource())
        self.app = Flask('RENDERTRON_CACHE_SERVER')
        self.add_subroute('retrieve_cache', self.retrieve_cache, methods=['GET'])
        self.add_subroute('refresh_cache', self.refresh_cache, methods=['PUT'])

    def add_subroute(self, name, callback, methods):
        self.app.add_url_rule('/', name, callback, methods=methods, defaults={'path': ''}, )
        self.app.add_url_rule('/<path:path>', name, callback, methods=methods)

    def start(self):
        self.app.run(threaded=False)

    def get_app(self):
        return self.app
    
    def _request_doc(self) -> Tuple[cache.Query, cache.Document]:
        headers = {k: v for k, v in request.headers.items()}
        query = cache.Query(request.path.lstrip('/'), request.args, headers)
        document = self.cache.query(query)
        return query, document

    def retrieve_cache(self, path) -> Response:
        # try:
        query, document = self._request_doc()
        content = self.cache.retrieve(document, query)
        return Response(content.content, status=content.status, headers=content.headers)

    # except Exception as e:
    #     return Response(response='Cache server error', status=404)

    def refresh_cache(self, path) -> Response:
        # try:
        query, document = self._request_doc()
        content = self.cache.refresh(document, query)
        return Response(content.content, status=content.status, headers=content.headers)
    # except Exception as e:
    #     return Response(response='Cache server error', status=404)
