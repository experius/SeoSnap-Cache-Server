import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '/../.env', override=False)
load_dotenv(find_dotenv(), override=False)

RENDERTRON_CACHE_DEBUG = bool(int(os.getenv('RENDERTRON_CACHE_DEBUG', 1)))
RENDERTRON_CACHE_LOCK_TIMEOUT = float(os.getenv('RENDERTRON_CACHE_LOCK_TIMEOUT', 1))
RENDERTRON_CACHE_ROOT = os.getenv('RENDERTRON_CACHE_ROOT', './cache')
RENDERTRON_CACHE_FILE_SUFFIX = os.getenv('RENDERTRON_CACHE_FILE_SUFFIX', '.json')
RENDERTRON_CACHE_RESOURCE_URL = os.getenv('RENDERTRON_CACHE_RESOURCE_URL', 'https://stackoverflow.com').rstrip('/')
RENDERTRON_CACHE_RESOURCE_METHOD = os.getenv('RENDERTRON_CACHE_RESOURCE_URL_METHOD', 'GET')
RENDERTRON_CACHE_HEADER_REQUEST_BLACKLIST = os.getenv('RENDERTRON_CACHE_HEADER_REQUEST_BLACKLIST', '').lower().split(',')
RENDERTRON_CACHE_HEADER_RESPONSE_BLACKLIST = os.getenv('RENDERTRON_CACHE_HEADER_RESPONSE_BLACKLIST', 'Set-Cookie,Content-Encoding,Transfer-Encoding').lower().split(',')
RENDERTRON_CACHE_ALLOWED_STATUS = map(lambda x: int(x), os.getenv('RENDERTRON_CACHE_ALLOWED_STATUS', '404,403').split(','))
