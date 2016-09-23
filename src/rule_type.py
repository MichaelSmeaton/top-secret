from abc import ABC, abstractmethod, ABCMeta
import re
from decimal import Decimal


class RuleType(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rule(self): pass

    @abstractmethod
    def get_code(self): pass

    @abstractmethod
    def extract(self, data): pass

    def get_tags(self, open_tag, close_tag, data):
        """
        Method RuleType.get_tags()'s docstring.
        Should return a substring of string between and including tags
        """
        regex = r"(<" + \
                re.escape(open_tag) + r")(.*)(</" + \
                re.escape(close_tag) + ">)"
        return re.search(regex, data, re.I | re.M).group(0)

    def clean(self, data, x):
        """
        Method RuleType.clean()'s docstring.
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


class Album(RuleType):
    def __init__(self):
        self.rule = ">[-\w`~!@#$%^&amp;*\(\)+={}|\[\]\\:" \
                    "&quot;;'&lt;&gt;?,.\/ ]+<"
        self.code = "a"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code

    def extract(self, data):
        data = re.sub('(<strong>)(.*)(</strong>)', '', data, re.I)
        data = re.findall(self.get_rule(), data, re.I)
        return super(Album, self).clean(data, 0)


class Artist(RuleType):
    def __init__(self):
        self.rule = ">[-\w`~!@#$%^&amp;*\(\)+={}|\[\]\\:" \
                    "&quot;;'&lt;&gt;?,.\/ ]+<"
        self.code = "ar"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code

    def extract(self, data):
        data = re.sub('(<strong>)(.*)(</strong>)', '', data, re.I)
        data = re.findall(self.get_rule(), data, re.I)
        return super(Artist, self).clean(data, 1)


class Price(RuleType):
    def __init__(self):
        self.rule = "[0-9]+\.[0-9]+"
        self.code = "p"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code

    def extract(self, data):
        data = super(Price, self).get_tags("span", "span", data)
        return Decimal(re.search(self.get_rule(), data).group(0))


class Image(RuleType):
    def __init__(self):
        self.rule = "(https?):(//)+[^\s]+\." \
                    "(jpg|jpeg|jif|jfif|gif|tif|tiff|png)"
        self.code = "i"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code

    def extract(self, data):
        data = super(Image, self).get_tags("a href", "a", data)
        return re.search(self.get_rule(), data, re.I).group(0)


class Link(RuleType):
    def __init__(self):
        self.rule = "((https?):(//)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"
        self.code = "l"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code

    def extract(self, data):
        data = super(Link, self).get_tags("a href", "a", data)
        return re.search(self.get_rule(), data, re.I).group(0)


class Ranking(RuleType):
    def __init__(self):
        self.rule = "[0-9]+"
        self.code = "r"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code

    def extract(self, data):
        data = super(Ranking, self).get_tags("strong", "strong", data)
        return int(re.search(self.get_rule(), data).group(0))
