"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 08:44
"""
import random


def ensure_move_exists(func):
    def func_(gm, depth: int):
        move = func(gm, depth)
        if move is None:
            return random.choice(gm.state.valid_moves)
        return move

    return func_
