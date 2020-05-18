"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 16:53
"""
from domain.entities.player import Player
from utils.helper import check_4_col, check_4_line, check_4_diag


class Move(object):

    def __init__(self, board):
        self.__board = board
        self.__player = None
        self.__move = None

    def make_move(self):
        legal_moves = self.get_pos_moves()
        col = self.get_move()
        board = self.get_board()
        player = self.get_player()
        if col not in legal_moves:
            raise ValueError("The move is incorrect!")
        if col in legal_moves:
            table = board.get_table()
            for line in range(len(table) - 1, -1, -1):
                if table[line][col] == 0:
                    if player.get_type() == "Computer":
                        value = 2
                    else:
                        value = 1
                    board.set_table(line, col, value)
                    break
        else:
            return None

    def get_board(self):
        return self.__board

    def get_player(self):
        return self.__player

    def get_move(self):
        return self.__move

    def get_pos_moves(self):
        '''
        Function that returns a list with all possible moves
        :return:
        '''
        moves_l = []
        board = self.get_board()
        table = board.get_table()
        for col in range(len(table[0])):
            if table[0][col] == 0:
                moves_l.append(col)
        return moves_l

    def check_if_win(self):
        '''
        Function that checks if the game has ended
        :return:
        '''
        board = self.get_board()
        table = board.get_table()

        if check_4_col(table) is not False:
            return self.__player
        elif check_4_line(table) is not False:
            return self.__player
        elif check_4_diag(table) is not False:
            return self.__player
        return None

    def check_if_draw(self):
        """
        Function that checks if the game is draw
        :return:
        """

        if len(self.get_pos_moves()) == 0:
            return True
        return False

    def set_move(self, new_move):
        self.__move = new_move

    def set_player(self, new_player):
        self.__player = new_player

    def alternate_turn(self):
        if self.__player.get_type() == "Computer":
            self.set_player(Player("Human"))
        else:
            self.set_player(Player("Computer"))
