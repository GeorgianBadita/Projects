"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   20.05.2020 13:13
"""
from abc import ABC
from abc import abstractmethod


class BoardEvaluator(ABC):

    @abstractmethod
    def evaluate_board(self, board_builder) -> int:
        raise NotImplementedError("Evaluate board not implemented!")
