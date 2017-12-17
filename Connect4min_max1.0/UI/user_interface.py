"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 19:17
"""
from domain.AI.minimax import MiniMax
from domain.entities.player import Player
import copy

class UI(object):
    """
    Class for User Interface
    """
    def __init__(self, game_manager):
        self.__manager = game_manager


    def __print_table(self):
        """
        Function that prints the table and optins at any turn
        :return:
        """
        self.__manager.draw_board_mgr()


    def show_ui(self):
        """
        Function that controls the game
        :return:
        """
        player1 = Player("Human")
        player2 = Player("Computer")
        player1.set_turn(True)
        player2.set_turn(False)
        while self.__manager.is_game_over() is False:
            self.__print_table()
            try:
                new_move = self.__manager.new_move_mgr(self.__manager.get_board_mgr())

                if player1.get_turn() is True:
                    move = int(input("Please give a move: \n"))
                    if move < 1 or move > 7:
                        raise ValueError
                    self.__change_move(player1, player2, new_move, move)
                elif player2.get_turn() is True:
                    min_maxx_manager = copy.deepcopy(self.__manager)
                    min_maxx = MiniMax(min_maxx_manager)
                    move_calc = min_maxx.mini_max()
                    self.__change_move(player2, player1, new_move, move_calc)
            except ValueError:
                print("The move is incorrect")
        self.__print_table()
        print("\n\n" + self.__manager.is_game_over().get_type() + " won")


    def __change_move(self, player, ot_player, move, given_move):
        move.set_move(given_move - 1)
        move.set_player(player)
        move.make_move()
        player.set_turn(False)
        ot_player.set_turn(True)
        self.__manager.set_move(move)
