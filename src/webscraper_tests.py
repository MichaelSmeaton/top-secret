import unittest
from src.controller import WebScrapingController
from src.model import WebScraper
import requests


class UnitTest(unittest.TestCase):
    def test_url_string(self):
        self._model = WebScraper()
        self.expected = True
        self.assertEqual(self._model.is_valid("http://www.google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("https://www.google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("https://google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("http://WWW.GoOgLe.cOm"),
                         self.expected)
        self.assertEqual(self._model.is_valid("http://www.google.com/maps"),
                         self.expected)
        self.assertEqual(self._model.is_valid("http://maps.google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("http://www.google.domain.com"),
                         self.expected)
        self.expected = False
        self.assertEqual(self._model.is_valid("www.google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("//www.google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("google.http://www.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("www.http://.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("http:\\\\www.google.com"),
                         self.expected)
        self.assertEqual(self._model.is_valid("htps://www.google.com"),
                         self.expected)

    def test_url_whitespace(self):
        self._model = WebScraper()
        self.expected = "http://www.google.com"
        self.assertEqual(self.expected, self._model.is_correct(
            "http://www.g o o g l e.com"))
        self.assertEqual(self.expected, self._model.is_correct(
            "http : / / www.google . com"))

    def test_url_missing_scheme(self):
        self._model = WebScraper()
        self.expected = "http://www.google.com"
        self.actual = self._model.is_correct("www.google.com")
        self.assertEqual(self.expected,
                         self.actual)

    def test_url_https_scheme(self):
        self._model = WebScraper()
        self.expected = "https://www.google.com"
        self.actual = self._model.is_correct("https://www.google.com")
        self.assertEqual(self.expected,
                         self.actual)

    def test_fetch_data_from_file(self):
        self._model = WebScraper()
        self.expected = ['<li>One</li>']
        self.actual = self._model.fetch(maximum=1, path='data.txt')

        self.assertEqual(self.expected,
                         self.actual)

    # Requires internet connection
    def test_url_fetch_data(self):
        self._model = WebScraper()
        self.expected = 1
        self.actual = len(self._model.fetch(maximum=1))
        self.assertEqual(self.expected,
                         self.actual)

    def test_url_found(self):
        self._model = WebScraper()
        self.expected = True
        self.actual = self._model.is_connected("http://www.google.com")
        self.assertEqual(self.expected,
                         self.actual)

    def test_url_not_found_1(self):
        self._model = WebScraper()
        self.expected = False
        self.actual = self._model.is_connected("http:\\qaz.wsx.edc.rfv")
        self.assertEqual(self.expected,
                         self.actual)

    def test_url_not_found_2(self):
        self._model = WebScraper()
        self.assertRaises(requests.ConnectionError,
                          self._model.is_connected, "http://qaz.wsx.edc.rfv")

    def test_pickle(self):
        self.controller = WebScrapingController(WebScraper())
        self.controller.get_data()
        self.controller.save_pickle_data()
        self.controller._container = {}
        self.controller.load_pickle_data()
        self.expected = 10
        self.assertEqual(self.expected,
                         len(self.controller.get_container(0)))


if __name__ == '__main__':
    unittest.main()
