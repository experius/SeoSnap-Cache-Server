from .. import constants
from . import Document, Query, Content, os, Resource


class Cache:
    storage_path: str
    resource: Resource

    def __init__(self, resource: Resource) -> None:
        self.storage_path = constants.RENDERTRON_CACHE_ROOT
        os.makedirs(self.storage_path, exist_ok=True)
        self.resource = resource

    def query(self, q: Query) -> Document:
        return Document(os.path.join(self.storage_path, q.get_key()))

    def retrieve(self, doc: Document, q: Query) -> Content:
        if doc.exists():
            content = doc.read()
            if constants.RENDERTRON_CACHE_DEBUG: content.headers['Rendertron-Cached'] = '1'
        else:
            content = self.resource.retrieve(doc, q)
            if constants.RENDERTRON_CACHE_DEBUG: content.headers['Rendertron-Cached'] = '0'

        return content

    def refresh(self, doc: Document, q: Query):
        self.delete(doc)
        return self.retrieve(doc, q)

    def delete(self, doc: Document):
        doc.delete()

    def purge(self, doc: Document):
        doc.purge()

