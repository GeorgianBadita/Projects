from board import IBuilder
from board.adapter.board_adapter import BoardEvaluatorAdapter
from board.adapter.board_evaluator import Connect4BoardEvaluator
from player.player import Player


class GameState:
    """
    Class for representing our game state
    """

    def __init__(self, board_builder: IBuilder, next_player: Player):
        """
        Constructor for game state class
        :param board_builder: game sate's board builder
        :param next_player: next player to make a move
        """
        self.__board_builder = board_builder
        self.__next_player = next_player

    @property
    def board_builder(self) -> IBuilder:
        return self.__board_builder

    @board_builder.setter
    def board_builder(self, new_board_builder: IBuilder):
        self.__board_builder = new_board_builder

    @property
    def valid_moves(self):
        return self.__board_builder.valid_moves

    @property
    def next_player(self):
        return self.__next_player

    @next_player.setter
    def next_player(self, new_player: Player):
        self.__next_player = new_player

    @property
    def evaluate_board(self) -> int:
        """
        Function to evaluate the board from the perspective of the player
        who is ntext to move
        :return: board score
        """
        return BoardEvaluatorAdapter(Connect4BoardEvaluator(), self).evaluate_board(self.board_builder)

    def __str__(self) -> str:
        """
        String representation of the game state
        :return: string representing the game state
        """
        return f"{self.board_builder}-{self.__next_player}"
