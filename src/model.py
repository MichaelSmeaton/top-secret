import requests
from bs4 import BeautifulSoup
from src.rule_type import *


class WebScraper:
    __rules = [Album(), Artist(), Price(), Image(), Link(), Ranking()]

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
        html = self.get_html_content(url)
        results = self.fetch_data(html, max1, max2, *tag)
        return results

    def fetch_from_file(self, path="", maximum=0):
        file_handler = open(path, 'r+')
        html = file_handler.read()
        results = self.fetch_data(html, maximum)
        return results

    def fetch_data(self, html, max1=0, max2=0, *tag):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find_all('div', {'id': 'main'})
        for found in content:
            found = found.find_all("li", limit=max1)
            for data in found:
                good_data = data.find_all(*tag, limit=max2)
                [results.append(str(element)) for element in good_data] \
                    if tag else results.append(str(data))
        return results

    def get_html_content(self, url):
        req = requests.get(url)
        return req.content

    def extract(self, raw_data, rule_code):
        """
        Method WebScraper.extract()'s docstring.
        Find and extract useful data
        """
        results = []
        selected_rule = self.select_rule(rule_code)
        for item in raw_data:
            data = str(item)
            try:
                results.append(selected_rule.extract(data))
            except AttributeError:
                continue
        return results

    def select_rule(self, rule_code):
        selected_rule = ""
        for rule in self.get_rules():
            if rule.get_code() == rule_code:
                selected_rule = rule
        return selected_rule

    def get_rules(self):
        return self.__rules

    def set_rules(self, rule_list):
        self.__rules = rule_list
