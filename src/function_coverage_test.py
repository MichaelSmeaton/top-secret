from src.model import WebScraper
from src.rule_type import *

import unittest


class FunctionCoverageTests(unittest.TestCase):
    def setUp(self):
        print("A test case is called.")
        self.model = WebScraper()
        self.rule = Album()

    def test_1(self):
        self.assertEqual("http://www.google.com",
                         self.model.is_correct("http://www.g o o g l e.com"))

    def test_2(self):
        self.assertEqual(True,
                         self.model.is_valid("http://www.google.com"))

    def test_3(self):
        self.assertEqual(True,
                         self.model.is_connected("http://www.google.com"))

    def test_4(self):
        self.assertEqual(["<li>One</li>"],
                         self.model.fetch_from_file("data.txt", 1))

    def test_5(self):
        self.assertEqual(['<span class="price">$18.99</span>'],
                         self.model.fetch_from_url
                         ('https://itunes.apple.com/nz/'
                          'album/poi-e/id256565680?'
                          'i=256566239&v0='
                          'WWW-NZ-ITSTOP100-'
                          'SONGS&l=en&ign-mpt=uo%3D4', 0, 1, "span",
                          {"class": "price"}, 1))

    def test_6(self):
        self.assertEqual([1], self.model.extract(
            ['<li><strong>1.</strong></li>'],
            "r"))

    def test_7(self):
        self.assertEqual("<strong>1.</strong>",
                         self.rule.get_tags(
                             "strong", "strong", "<li><strong>1.</strong>"))

    def test_8(self):
        self.assertEqual("li", self.rule.clean(['<li>'], 0))

    def tearDown(self):
        print("This test case is done!")

if __name__ == '__main__':
    unittest.main(verbosity=2)
