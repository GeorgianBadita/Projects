"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 17:40
"""
from abc import ABC
from abc import abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        """
        Function to execute a command
        :return:
        """
        raise NotImplementedError("Execute function not implemented")

    @abstractmethod
    def __str__(self):
        raise NotImplementedError("__str__ not implemented")


