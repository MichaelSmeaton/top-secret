from abc import ABC, abstractmethod, ABCMeta


class RuleType(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rule(self): pass

    @abstractmethod
    def get_code(self): pass

    @staticmethod
    def create(code):
        if code == "a":
            return Album()
        elif code == "ar":
            return Artist()
        elif code == "p":
            return Price()
        elif code == "i":
            return Image()
        elif code == "l":
            return Link()
        elif code == "r":
            return Ranking()


class Album(RuleType):
    def __init__(self):
        self.rule = ">[-\w`~!@#$%^&amp;*\(\)+={}|\[\]\\:" \
                    "&quot;;'&lt;&gt;?,.\/ ]+<"
        self.code = "a"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code


class Artist(RuleType):
    def __init__(self):
        self.rule = ">[-\w`~!@#$%^&amp;*\(\)+={}|\[\]\\:" \
                    "&quot;;'&lt;&gt;?,.\/ ]+<"
        self.code = "ar"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code


class Price(RuleType):
    def __init__(self):
        self.rule = "[0-9]+\.[0-9]+"
        self.code = "p"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code


class Image(RuleType):
    def __init__(self):
        self.rule = "(https?):(//)+[^\s]+\." \
                    "(jpg|jpeg|jif|jfif|gif|tif|tiff|png)"
        self.code = "i"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code


class Link(RuleType):
    def __init__(self):
        self.rule = "((https?):(//)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)"
        self.code = "l"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code


class Ranking(RuleType):
    def __init__(self):
        self.rule = "[0-9]+"
        self.code = "r"

    def get_rule(self):
        return self.rule

    def get_code(self):
        return self.code
