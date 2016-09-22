import requests
import re
from bs4 import BeautifulSoup
from decimal import Decimal
from src.rule_type import *


class WebScraper:
    def is_correct(self, url):
        """`
        Method WebScraper.is_correct()'s docstring.
        Check if URL is missing scheme. Only for HTTP and HTTPS URLS
        Remove extra whitespaces
        """
        if ' ' in url:
            words = url.split()
            url = ""
            for li in words:
                url += li

        count = 0
        s = ["http://", "https://"]
        for i, x in enumerate(s):
            if not url.startswith(x) and i < len(s):
                count += 1
            if count == len(s):
                url = s[0] + url

        # print(url)
        return url

    def is_valid(self, url):
        """
        Method WebScraper.is_valid()'s docstring.
        Check if URL is valid and is in it's correct format. Supports HTTP and
        HTTPS
        """
        if re.match("((https?):(//)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?))", url,
                    re.I):
            # print("Good format")
            return True
        else:
            # print("Bad format")
            return False

    def is_connected(self, url):
        """
        Method WebScraper.is_connected()'s docstring.
        Check if HTTP response code is OK.
        """
        if self.is_valid(url):
            try:
                requests.head(url)
                return True
            except requests.ConnectionError:
                print("Error: Failed to connect.")
                raise
        return False

    def fetch_from_url(self, url='http://www.apple.com/nz/'
                                 'itunes/charts/albums/',
                       max1=0, max2=0, *tag):
        """
        Method WebScraper.fetch()'s docstring.
        Get data from Web page.
        """
        # html = ""
        # try:
        # file_handler = open(path, 'r+')
        # html = file_handler.read()
        # except FileNotFoundError:
        # req = requests.get(url)
        # html = req.content
        html = self.get_html_content(url)
        # finally:
        # soup = BeautifulSoup(html, 'html.parser')
        # results = []
        # results = self.fetch(html, maximum)
        results = self.fetch_data(html, max1, max2, *tag)
        # content = soup.find_all('div', {'id': 'main'})
        # for div in content:
        # li = div.find_all('li', limit=maximum)
        # li = self.fetch_data(html, maximum)
        # for data in li:
        # results.append(str(data))
        return results

    def fetch_from_file(self, path="", maximum=0):
        file_handler = open(path, 'r+')
        html = file_handler.read()
        # results = self.fetch_from_url(html, maximum)
        results = self.fetch_data(html, maximum)
        return results

        # def fetch_by_keyword(self, url, tag,
        # tag_class, css_class, maximum=10):
        # """
        # Method WebScraper.fetch()'s docstring.
        # Get data by keyword lookup from Web page.
        # """
        # req = requests.get(url)
        # html = req.content
        # html = self.get_html_content(url)
        # soup = BeautifulSoup(html, 'html.parser')
        # results = []
        # content = soup.find_all('div', {'id': 'main'})
        # for div in content:
        # ul = div.find_all('li')
        # for li in ul:
        # ul = self.fetch_data(html, 0)
        # results = self.fetch(html, 0,
        # maximum, tag, {tag_class: css_class})
        # for li in ul:
        # span = li.find_all('span', {attr: keyword}, limit=maximum)
        # for kw in span:
        # results.append(str(kw))
        # return results

    def fetch_data(self, html, max1=0, max2=0, *tag):
        #  li = []
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find_all('div', {'id': 'main'})
        for found in content:
            found = found.find_all("li", limit=max1)
            for data in found:
                # if tag:
                # li = div.find_all('li', limit=maximum)
                # li = div.find_all(*tag, limit=max2)
                good_data = data.find_all(*tag, limit=max2)
                # for kw in li:
                # for element in good_data:
                # results.append(str(element))
                # results.append(str(div))
                # else:
                # results.append(str(div))
                [results.append(str(element)) for element in good_data] \
                    if tag else results.append(str(data))
        return results

    def get_html_content(self, url):
        req = requests.get(url)
        return req.content

    def extract(self, raw_data, option):
        """
        Method WebScraper.extract()'s docstring.
        Find and extract useful data
        """
        results = []
        r = RuleType.create(option)
        for item in raw_data:
            data = str(item)
            try:
                results.append(r.extract(data))
            except AttributeError:
                continue
        return results
