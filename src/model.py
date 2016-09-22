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
        code = r.get_code()
        for item in raw_data:
            no_tags = str(item)
            if code == "r":
                try:
                    results.append(int(re.search(r.get_rule(),
                                                 self.tag_content("strong",
                                                                  "strong",
                                                                  no_tags)).
                                       group(0)))
                except AttributeError:
                    continue
            elif code == "i":
                try:
                    results.append(re.search(
                        r.get_rule(),
                        self.tag_content("a href", "a",
                                         no_tags), re.I)
                                   .group(0))
                except AttributeError:
                    continue
            elif code == "a":
                no_tags = re.sub('(<strong>)(.*)'
                                 '(</strong>)', '', no_tags, re.I)
                data = (re.findall(r.get_rule(), no_tags, re.I))
                results.append(self.clean(data, 0))
            elif code == "ar":
                no_tags = re.sub('(<strong>)(.*)'
                                 '(</strong>)', '', no_tags, re.I)
                data = (re.findall(r.get_rule(), no_tags, re.I))
                results.append(self.clean(data, 1))
            elif code == "l":
                try:
                    results.append(re.search(r.get_rule(),
                                             self.tag_content("a href", "a",
                                                              no_tags), re.I)
                                   .group(0))
                except AttributeError:
                    continue
            elif code == "p":
                results.append(Decimal(re.search(r.get_rule(),
                                                 self.tag_content(
                                                     "span", "span", no_tags))
                                       .group(0)))
        return results

    def tag_content(self, open_tag, close_tag, data):
        """
        Method WebScraper.fetch()'s docstring.
        Should return a substring of string between and including tags
        """
        regex = r"(<" + \
                re.escape(open_tag) + r")(.*)(</" + \
                re.escape(close_tag) + ">)"
        return re.search(regex, data, re.I | re.M).group(0)

    def clean(self, data, x):
        """
        Method WebScraper.clean()'s docstring.
        Removes unwanted sequence of characters from a list of strings
        """
        chars = ['>', '<', "&amp;"]
        for i, items in enumerate(data):
            for c in chars:
                if c == "&amp;":
                    data[i] = data[i].replace(c, '&')
                else:
                    data[i] = data[i].replace(c, '')
        return data[x]
