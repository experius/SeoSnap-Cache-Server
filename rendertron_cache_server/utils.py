import re


def lrem(s, pattern) -> str:
    if s.startswith(pattern):
        s = s[len(pattern):]
    return s


def rrem(s, pattern) -> str:
    if s.endswith(pattern):
        s = s[:-len(pattern)]
    return s


URL_ROUTE_PATTERN = re.compile(r'^(((http|https):\/\/)?[^\/?&]*)')


def extract_route(url):
    """Extracts a route from a full url"""
    return URL_ROUTE_PATTERN.sub('', url)


def extract_route_url(url):
    """Extract a target url from rendertron supported route"""
    # Fix missing slashes
    if url.find('://') < 0 and url.find(':/') >= 0:
        url = url.replace(':/', '://')

    url = lrem(url, '/render/')
    url = rrem(url, '/')

    return url


def strip_schema(url):
    """Strips schema from a url"""
    return lrem(lrem(url, 'http://'), 'https://')


def filter_dict(d: dict, ks: set):
    return {k: v for k, v in d.items() if k.lower() not in ks}
