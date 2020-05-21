"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   20.05.2020 13:16
"""
from board.adapter.adapter_interface import BoardEvaluator


class BoardEvaluatorAdapter(BoardEvaluator):

    def __init__(self, evaluator, state):
        self.__evaluator = evaluator
        self.__state = state

    def evaluate_board(self, board_builder) -> int:
        board = board_builder.board_config
        return self.__evaluator.evaluate_connect4_board(board, self.__state.next_player)
