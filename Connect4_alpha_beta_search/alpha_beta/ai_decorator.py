"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 16:09
"""
from abc import ABC
from abc import abstractmethod

from alpha_beta.ai_interface import AI


class AiDecorator(AI, ABC):  # Decorator

    def __init__(self, ai):
        self.__ai = ai

    @abstractmethod
    def compute_move(self):
        pass
