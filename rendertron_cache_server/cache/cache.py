import logging
from typing import List
import urllib.parse as urllib
from posixpath import join as urljoin

from .. import constants
from . import Document, Query, Content, os, Resource
from rendertron_cache_server import get_logger


class Cache:
    storage_path: str
    resource: Resource
    log: logging.Logger

    def __init__(self, resource: Resource) -> None:
        self.storage_path = constants.RENDERTRON_CACHE_ROOT
        os.makedirs(self.storage_path, exist_ok=True)
        self.resource = resource
        self.log = get_logger()

    def query(self, q: Query, suffix=True) -> Document:
        """Builds a document from a query"""
        path = os.path.join(self.storage_path, q.get_key(suffix))
        return Document(path)

    def retrieve(self, doc: Document, q: Query, ignore_cache: bool = False) -> Content:
        """Retrives a document from cache. If miss then cache it"""
        if not ignore_cache and doc.exists():
            content = doc.read()
            content.headers['Rendertron-Cached'] = '1'
        else:
            content = self.resource.retrieve(doc, q)
            content.headers['Rendertron-Cached'] = '0'

        content.headers['Rendertron-Cached-At'] = content.cached_at
        return content

    def refresh(self, doc: Document, q: Query):
        """Deletes the cached document then retrieves it"""
        return self.retrieve(doc, q, True)

    def delete(self, doc: Document):
        doc.delete()

    def purge(self, doc: Document, q: Query):
        """Deletes a document and its children"""
        folder = self.query(q, False)
        file = self.query(q, True)

        self.log.log(logging.DEBUG, f'Purging: {folder.path} and {file.path}')
        folder.purge()
        file.delete()

    def list(self, doc: Document, q: Query) -> List[str]:
        root_path = os.path.abspath(os.path.join(self.storage_path, q.get_key(False)))
        if not os.path.isdir(root_path): return []

        root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=urllib.urlparse(q.url))
        suffix = constants.RENDERTRON_CACHE_FILE_SUFFIX

        result = []
        for (root, _, files) in os.walk(root_path):
            root = root[len(root_path):].lstrip('/')  # Strip the root path
            for file in files:
                file = file[:-len(suffix)].lstrip('/')  # Strip the
                url = urljoin(root_url, root, file)
                result.append(url)

        return result
