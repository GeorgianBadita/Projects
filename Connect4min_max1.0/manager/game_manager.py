"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 17:07
"""
from domain.entities.move import Move
from domain.entities.player import Player
from utils.helper import check_4_col, check_4_line, check_4_diag


class GameManager(object):

    def __init__(self):
        self.__move = None

    def set_move(self, new_move):
        self.__move = new_move

    def draw_board_mgr(self):
        self.__move.get_board().draw_board()

    def is_game_over(self):

        is_over = self.__move.check_if_win()
        if is_over is None:
            return False
        return is_over

    def get_board_mgr(self):
        return self.__move.get_board()

    def new_move_mgr(self, board):
        new_move = Move(board)
        return new_move

    def get_pos_moves_mgr(self):
        return self.__move.get_pos_moves()

    def next_state(self, move, player):
        to_move = self.new_move_mgr(self.__move.get_board())
        to_move.set_move(move)
        to_move.set_player(Player(player))
        to_move.make_move()
        self.__move = to_move
        return self
