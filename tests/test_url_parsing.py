import unittest
from rendertron_cache_server.utils import *

class ParsingTestCase(unittest.TestCase):
    def test_route_extract(self):
        cases = [
            ('0.0.0.0:5001', ''),
            ('0.0.0.0:5001/render/', '/render/'),
            ('http://0.0.0.0:5001', ''),
            ('http://0.0.0.0:5001/render/', '/render/'),
            ('http://0.0.0.0:5001/render/', '/render/'),
            ('https://0.0.0.0:5001/render/', '/render/'),
            ('/render/', '/render/'),
            ('https://0.0.0.0:5001/render/http://helloworld.com', '/render/http://helloworld.com'),
            ('http://0.0.0.0:5001/render/http://helloworld.com', '/render/http://helloworld.com'),
            ('http://0.0.0.0:5001/render/http://helloworld.com?hello=1', '/render/http://helloworld.com?hello=1'),
            ('http://0.0.0.0:5001/render/http://helloworld.com?hello=1::1', '/render/http://helloworld.com?hello=1::1'),
            ('http://helloworld.com/render/http://hw.com?hello=1::1', '/render/http://hw.com?hello=1::1'),
        ]

        for (i, o) in cases:
            self.assertEqual(extract_route(i), o)

    def test_urls_parse(self):
        cases = [
            ('/render/', ''),
            ('/render/http:/helloworld.com', 'http://helloworld.com'),
            ('/render/https:/helloworld.com', 'https://helloworld.com'),
            ('/render/https://helloworld.com', 'https://helloworld.com'),
            ('/render/https://helloworld.com/some-path', 'https://helloworld.com/some-path'),
            ('/render/https://helloworld.com/some-path?foo=bar&foo', 'https://helloworld.com/some-path?foo=bar&foo'),
            ('/render/https://helloworld.com/some-path/?foo=bar&foo', 'https://helloworld.com/some-path/?foo=bar&foo'),
        ]

        for (i, o) in cases:
            self.assertEqual(extract_route_url(i), o)


if __name__ == '__main__':
    unittest.main()
