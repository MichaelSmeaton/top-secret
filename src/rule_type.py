from abc import ABC, abstractmethod, ABCMeta


class RuleType(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_rule(self, index): pass
