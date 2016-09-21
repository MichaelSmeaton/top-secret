from abc import ABC, abstractmethod, ABCMeta


class RuleType(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rule(self, index): pass

    @abstractmethod
    def get_code(self): pass


class Name(RuleType):
    rules = [">[-\w`~!@#$%^&amp;*\(\)+={}|\[\]\\:"
             "&quot;;'&lt;&gt;?,.\/ ]+<",
             "(<strong>)(.*)(</strong>)"]
    code = "a"

    def get_rule(self, index):
        return self.rules

    def get_code(self):
        return self.code


class Price(RuleType):
    rules = ["[0-9]+\.[0-9]+", "a href a"]
    code = "p"

    def get_rule(self, index):
        return self.rules

    def get_code(self):
        return self.code


class Image(RuleType):
    rules = ["(https?):(//)+[^\s]+\.(jpg|jpeg|jif|jfif|gif|tif|tiff|png)"]
    code = "i"

    def get_rule(self, index):
        return self.rules

    def get_code(self):
        return self.code


class Link(RuleType):
    rules = ["((https?):(//)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"]
    code = "l"

    def get_rule(self, index):
        return self.rules

    def get_code(self):
        return self.code


class Ranking(RuleType):
    rules = ["[0-9]+"]
    code = "r"

    def get_rule(self, index):
        return self.rules

    def get_code(self):
        return self.code
