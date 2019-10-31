from requests import Session, Request

from urllib.parse import urlparse
from . import Document, Query, Content
from .. import constants
import os

class Resource:
    session: Session

    def __init__(self) -> None:
        self.session = Session()

    def retrieve(self, doc: Document, q: Query) -> Content:
        host = urlparse(q.route).netloc
        q.headers['Host'] = host if host else urlparse(constants.RENDERTRON_CACHE_RESOURCE_URL).netloc

        request = Request(
            method=constants.RENDERTRON_CACHE_RESOURCE_METHOD,
            url=f'{constants.RENDERTRON_CACHE_RESOURCE_URL}/{q.route}',
            headers=q.headers,
            params=q.params
        ).prepare()

        print(f'{constants.RENDERTRON_CACHE_RESOURCE_URL}/{q.route}')

        response = self.session.send(request)
        headers = {k: v for k, v in response.headers.items() if k.lower() not in constants.RENDERTRON_CACHE_HEADER_RESPONSE_BLACKLIST}
        content = Content(response.status_code, headers, response.text)


        if response.status_code // 100 == 2:
            doc.write(content)

        return content
