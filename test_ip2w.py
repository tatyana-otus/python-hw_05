import sys
import unittest
import functools
import json

import ip2w as app


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except AssertionError as e:
                    raise AssertionError("{}: {} (test case: {})".format(e, f.__name__, c))
        return wrapper
    return decorator


class HandlerTest(unittest.TestCase):
    cfg = None

    @classmethod
    def setUpClass(cls):
        cls.cfg = app.init("ip2w.cfg")

    def test_valid_appid(self):
        """Reading weather_appid from cgf file"""
        self.assertNotEqual(type(self).cfg, None)
        self.assertNotEqual(type(self).cfg["weather_appid"], "")

    @cases(["/ip2w/qwqw", "/ip2w/8.8.8", "/ip2w/256.34.5.45S"])
    def test_invalid_request(self, url):
        """Invalid IP v4 address"""
        with self.assertRaises(Exception):
            app.request_handler(url, type(self).cfg["weather_appid"])

    @cases([{"url": "/ip2w/8.8.8.8", "city": "Mountain View"},
            {"url": "/ip2w/8.8.4.4", "city": "Cheney"}])
    def test_invalid_request(self, arg):
        """Valid IP v4 address"""
        res = app.request_handler(type(self).cfg["geo_url"],
                                  type(self).cfg["weather_url"],
                                  type(self).cfg["weather_appid"],
                                  arg["url"])
        raw_data = json.loads(res)
        city = raw_data.get("city", "")
        self.assertEqual(city, arg["city"])
        desc = raw_data.get("description", "")
        self.assertNotEqual(desc, "")
        temp = raw_data.get("temp", "")
        self.assertNotEqual(temp, "")


if __name__ == "__main__":
    unittest.main()
