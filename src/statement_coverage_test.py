from src.model import WebScraper

import unittest
import requests
from decimal import Decimal


class StatementCoverageTests(unittest.TestCase):
    def setUp(self):
        print("A test case is called.")
        self.model = WebScraper()

    def test_1(self):
        self.assertEqual("http://www.google.com",
                         self.model.is_correct("http://www.g o o g l e.com"))

    def test_2(self):
        self.assertEqual("http://www.google.com",
                         self.model.is_correct("www.google.com"))

    def test_3(self):
        self.assertEqual(True, self.model.is_valid("http://www.google.com"))

    def test_4(self):
        self.assertEqual(False, self.model.is_valid("www.google.com"))

    def test_5(self):
        self.assertEqual(True,
                         self.model.is_connected("http://www.google.com"))

    def test_6(self):
        self.assertEqual(False,
                         self.model.is_connected("http:\\qaz.wsx.edc.rfv"))

    def test_7(self):
        self.assertRaises(requests.ConnectionError,
                          self.model.is_connected, "http://qaz.wsx.edc.rfv")

    def test_8(self):
        self.assertRaises(AttributeError,
                          self.model.extract,
                          ["<li><strong>str</strong></li>"], "ranking")

    def test_9(self):
        self.assertEqual(["http://www.domain.com/image.jpg"],
                         self.model.extract
                         (['<a href="http://www.domain.com/image.jpg">'
                           '</a>'], "i"))

    def test_10(self):
        self.assertEqual(["album"],
                         self.model.extract
                         (["<li>album</li><li>artist<\li>"],
                          "a"))

    def test_11(self):
        self.assertEqual(["artist"], self.model.extract(
            ["<li>album</li><li>artist<\li>"], "ar"))

    def test_12(self):
        self.assertEqual(["http://www.domain.com"],
                         self.model.extract
                         (['<a href="http://www.domain.com"></a>'],
                          "l"))

    def test_13(self):
        self.assertEqual([Decimal('9.99')],
                         self.model.extract(['<span>$9.99</span>'], "p"))

    def tearDown(self):
        print("This test case is done!")

if __name__ == '__main__':
    unittest.main(verbosity=2)
