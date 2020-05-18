"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 16:54
"""
from domain.entities.board import Board
from domain.entities.move import Move
from domain.entities.player import Player
from utils.helper import check_4_col, check_4_diag, check_4_line


def test_create_player():
    pl = Player("Human")
    assert pl.get_type() == "Human"
    pl.set_turn(True)
    assert pl.get_turn() is True


def test_create_board():
    board = Board(6, 7)
    table = board.get_table()
    assert board.get_height() == 6
    assert board.get_width() == 7
    assert len(table) == board.get_height()
    assert len(table[0]) == board.get_width()


def test_check_win():
    board = Board(6, 7)
    table = board.get_table()
    # assert check_4_line(table) is True
    # assert check_4_col(table) is True
    # assert check_4_diag(table) is True

    matrix = [[x for x in range(6)]] * 6

    assert check_4_diag(matrix) is False
    assert check_4_col(matrix) is True
    assert check_4_line(matrix) is False

    board.set_table(0, 1, 1)
    board.set_table(0, 2, 2)
    board.set_table(0, 3, 3)
    board.set_table(1, 0, 1)
    board.set_table(1, 1, 2)
    board.set_table(1, 2, 3)
    board.set_table(2, 0, 1)
    board.set_table(2, 1, 3)
    board.set_table(3, 0, 3)

    assert check_4_diag(table) is True


def test_create_move():
    pl = Player("Computer")
    pl2 = Player("Human")
    pl.set_turn(True)
    board = Board(6, 7)
    mv = Move(board)
    mv.set_player(pl)
    mv.set_move(1)
    assert len(mv.get_pos_moves()) == 7
    mv.make_move()
    # table = board.get_table()
    pl2.set_turn(True)
    mv1 = Move(board)
    mv1.set_player(pl2)
    mv1.set_move(1)
    mv1.make_move()
    mv1.make_move()
    mv1.make_move()
    mv1.make_move()
    assert mv1.check_if_win() == mv1.get_player()


test_check_win()
test_create_board()
test_create_move()
test_create_player()
