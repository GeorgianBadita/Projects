"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 16:03
"""
from abc import ABC
from abc import abstractmethod


class AI(ABC):  # Component interface
    """
    Abstract class for Artificial Intelligence
    """

    @abstractmethod
    def compute_move(self):
        """
        Function to compute a move
        :return: move
        """

        raise NotImplementedError("Compute move not implemented")
