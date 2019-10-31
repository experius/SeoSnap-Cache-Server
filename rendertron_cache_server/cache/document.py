from typing import Dict
import os, json, portalocker
from shutil import rmtree


from ..constants import RENDERTRON_CACHE_LOCK_TIMEOUT


class Content:
    status: int
    headers: Dict[str, str]
    content: str

    def __init__(self, status: int, headers: Dict[str, str], content: str):
        self.status = status
        self.headers = headers
        self.content = content


class Document:
    path: str

    def __init__(self, path: str):
        self.path = path

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def read(self) -> Content:
        with portalocker.Lock(self.path, 'r', timeout=RENDERTRON_CACHE_LOCK_TIMEOUT, flags=portalocker.LOCK_SH) as f:
            content = Content(**json.load(f))
        return content

    def write(self, c: Content):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with portalocker.Lock(self.path, 'w', timeout=RENDERTRON_CACHE_LOCK_TIMEOUT, flags=portalocker.LOCK_EX) as f:
            json.dump(c.__dict__, f)

    def delete(self):
        if self.exists():
            os.remove(self.path)

    def purge(self):
        path = os.path.dirname(self.path)
        if os.path.exists(path):
            rmtree(path, ignore_errors=False)