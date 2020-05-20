"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.05.2020 17:52
"""
from game.game_manager import GameManager
from game.memento.care_taker import Caretaker
from player.alliance_enum import Alliance
from player.player import Player
from player.type_enum import PlayerType
from ui.command_interface import Command
from ui.select_difficulty_command import SelectDifficultyCommand
from ui.undo_command import UndoCommand


class StartNewGameCommand(Command):

    def __print_format_table(self, gm):
        print("TABLE: ")
        print(gm)

    def __print_format_game_over(self, gm, winner):
        print(gm)
        print(f"\nNice player: {winner.name} has won")

    def __handle_move(self, move, gm, care_taker):
        if move == 'u':
            care_taker.undo()
            return None

        return gm.make_move(move)

    def execute(self):
        player1 = Player(Alliance.RED, PlayerType.HUMAN, name="Dia")
        player2 = Player(Alliance.YELLOW, PlayerType.COMPUTER)
        SelectDifficultyCommand().execute()
        gm = GameManager(player1, player2)
        care_taker = Caretaker(gm)
        winner = None
        while not gm.game_over and not gm.draw:
            self.__print_format_table(gm)
            move = gm.state.next_player.get_move

            if isinstance(move, str):
                UndoCommand(gm, care_taker).execute()
            care_taker.backup()
            winner = self.__handle_move(move, gm, care_taker)
        self.__print_format_game_over(gm, winner)

    def __str__(self):
        return "Start new game"
