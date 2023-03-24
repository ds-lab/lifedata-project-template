from abc import ABC
from abc import abstractmethod


class Explanation(ABC):
    @abstractmethod
    def __init__(self):
        """
        TODO
        """
        pass

    @abstractmethod
    def explain(self):
        pass


class Explanation_1(Explanation):
    def __init__(self):
        """
        TODO
        """
        pass

    def explain(self):
        """
        TODO
        """
        pass


class Explanation_2(Explanation):
    def __init__(self):
        """
        TODO
        """
        pass

    def explain(self):
        """
        TODO
        """
        pass


class NoExplanation(Explanation):
    def __init__(self):
        """
        TODO
        """
        pass

    def explain(self):
        """
        TODO
        """
        return
