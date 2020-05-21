"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   20.05.2020 13:12
"""
from board.piece.piece import Piece
from player.alliance_enum import Alliance


class Connect4BoardEvaluator:

    def evaluate_connect4_board(self, board, next_player):
        utility = 0
        player = next_player
        util_table = [[3, 4, 5, 7, 5, 4, 3],
                      [4, 6, 8, 10, 8, 6, 4],
                      [5, 8, 11, 13, 11, 8, 5],
                      [5, 8, 11, 13, 11, 8, 5],
                      [4, 6, 8, 10, 8, 6, 4],
                      [3, 4, 5, 7, 5, 4, 3]]
        player_piece_type = Piece.YELLOW if player.alliance == Alliance.YELLOW else Piece.RED
        table = board
        for line in range(len(table)):
            for col in range(len(table[0])):
                if table[line][col] == player_piece_type:
                    utility += util_table[line][col]
                elif table[line][col] != Piece.EMPTY:
                    utility -= util_table[line][col]
        return utility
