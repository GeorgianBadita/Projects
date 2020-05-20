"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 08:54
"""
from game.strategy.player_type_strategy import PlayerTypeStrategy
from utils.utils import read_move_from_keyboard


class HumanStrategy(PlayerTypeStrategy):
    def choose_move(self) -> int:
        return read_move_from_keyboard()
