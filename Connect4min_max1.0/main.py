"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 19:17
"""
from UI.user_interface import UI
from domain.entities.board import Board
from domain.entities.move import Move
from manager.game_manager import GameManager

board = Board(6, 7)
move = Move(board)
game_manager = GameManager()
game_manager.set_move(move)
ui = UI(game_manager)
ui.show_ui()