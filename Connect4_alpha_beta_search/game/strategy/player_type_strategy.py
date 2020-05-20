"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 08:51
"""
from abc import ABC
from abc import abstractmethod


class PlayerTypeStrategy(ABC):
    """
    Class for playing strategy
    """

    @abstractmethod
    def choose_move(self) -> int:
        """
        Method to choose a move based on player type
        :return: int representing move
        """
        raise NotImplementedError("Choose move not implemented")
