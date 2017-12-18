"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 20:58
"""
import copy

from domain.entities.player import Player


class MiniMax:

    def mini_max(self, game_state, depth):

        moves = game_state.get_pos_moves()
        game_state.set_player(Player("Computer"))
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = self.next_state(game_state, move)
            #print("##########")
            #print("move " + str(move))
            score = self.__min_play(clone, depth - 1)
            #print(str(move) + ":" + str(score))
            if score > best_score:
                best_score = score
                best_move = move
        return best_move


    def __min_play(self, game_state, depth):
        #game_state.get_board().draw_board()
        if game_state.check_if_win() is not None:
            return float('inf')
        if game_state.check_if_draw() is True:
            return 0
        if depth == 0:
            return game_state.get_board().evaluate_board()
        moves = game_state.get_pos_moves()
        best_score = float('inf')
        for move in moves:
            game_state.set_player(Player("Human"))
            clone = self.next_state(game_state, move)
            score = self.__max_play(clone, depth - 1)

            if score < best_score:
                best_score = score
                best_move = move

        return best_score

    def __max_play(self, game_state, depth):
        #game_state.get_board().draw_board()
        if game_state.check_if_win() is not None:
            return float('-inf')
        if game_state.check_if_draw() is True:
            return 0
        if depth == 0:
            return game_state.get_board().evaluate_board()
        moves = game_state.get_pos_moves()
        best_score = float('-inf')
        for move in moves:
            game_state.set_player(Player("Computer"))
            clone = self.next_state(game_state, move)
            score = self.__min_play(clone, depth - 1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score

    def next_state(self, state, move):
        clone = copy.deepcopy(state)
        clone.set_move(move)
        clone.make_move()
        clone.alternate_turn()
        clone.get_board()
        return clone