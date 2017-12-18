"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 19:17
"""
from domain.AI.minimax import MiniMax
from domain.entities.color import Color
from domain.entities.player import Player

class UI(object):
    """
    Class for User Interface
    """
    def __init__(self, game_manager):
        self.__manager = game_manager
        self.clr = Color("some_clr")

    def __print_table(self):
        """
        Function that prints the table and optins at any turn
        :return:
        """

        print(self.clr.GREEN + "Table:\n" + self.clr.END)
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
            try:
                self.__print_table()

                new_move = self.__manager.new_move_mgr(self.__manager.get_board_mgr())

                if player1.get_turn() is True:
                    move = int(input("Please give a move: \n"))
                    if move < 1 or move > 7:
                        raise ValueError
                    print("You made a move on C" + str(move) + "\n\n")
                    self.__change_move(player1, player2, new_move, move)
                elif player2.get_turn() is True:
                    min_maxx = MiniMax()
                    move_calc = min_maxx.mini_max(new_move, 4)
                    print("Computer made a move on C" + str(move_calc) + "\n\n")
                    self.__change_move(player2, player1, new_move, move_calc + 1)
            except ValueError:
                print(self.clr.RED + "The move is incorrect\n" + self.clr.END)
        self.__print_table()
        if self.__manager.is_game_over().get_type() == "Computer":
            print("Computer won!")
        else:
            print("You won!")



    def __change_move(self, player, ot_player, move, given_move):
        move.set_move(given_move - 1)
        move.set_player(player)
        move.make_move()
        player.set_turn(False)
        ot_player.set_turn(True)
        self.__manager.set_move(move)
