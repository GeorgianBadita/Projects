"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 08:57
"""
from alpha_beta.alpha_beta_pruning import AlphaBetaPruning
from alpha_beta.alpha_beta_pruning import AlphaBetaWithEnsureMove
from game.strategy.player_type_strategy import PlayerTypeStrategy


class ComputerStrategy(PlayerTypeStrategy):
    def __init__(self, gm, depth: int):
        self.__gm = gm
        self.__depth = depth

    def choose_move(self) -> int:
        return AlphaBetaWithEnsureMove(AlphaBetaPruning(self.__gm, self.__depth)).compute_move()
