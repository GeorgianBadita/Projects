"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/18/2017 20:26
"""
import copy

from domain.entities.player import Player


class AlphaBeta:

    def alpha_beta_search(self, game_state, player_to_max, depth):

        moves = game_state.get_pos_moves()
        game_state.set_player(player_to_max)
        best_move = moves[0]
        best_score = float('-inf')
        beta = float('inf')

        for move in moves:
            clone = self.next_state(game_state, move)
            score = self.__min_value(clone, best_score, beta, depth - 1)
            if score > best_score:
                best_score = score
                best_move = move
            print("value: ", score)
        return best_move


    def __min_value(self, game_state, alpha, beta, depth):
        #game_state.get_board().draw_board()
        if game_state.check_if_win() is not None:
            return float('inf')
        if game_state.check_if_draw() is True:
            return 0
        if depth == 0:
            return game_state.get_board().evaluate_board()
        moves = game_state.get_pos_moves()
        infinity = float('inf')
        score = infinity
        for move in moves:
            #game_state.set_player(Player("Human"))
            clone = self.next_state(game_state, move)
            score = min(score, self.__max_value(clone, alpha, beta, depth - 1))
            if score <= alpha:
                return score
            beta = min(beta, score)

        return score

    def __max_value(self, game_state, alpha, beta, depth):
        #game_state.get_board().draw_board()
        if game_state.check_if_win() is not None:
            return float('-inf')
        if game_state.check_if_draw() is True:
            return 0
        if depth == 0:
            return game_state.get_board().evaluate_board()
        moves = game_state.get_pos_moves()
        score = float('-inf')
        for move in moves:
            #game_state.set_player(Player("Computer"))
            clone = self.next_state(game_state, move)
            score = max(score, self.__min_value(clone, alpha, beta, depth - 1))
            if score >= beta:
                return score
            alpha = max(score, alpha)
        return score

    def next_state(self, state, move):
        clone = copy.deepcopy(state)
        clone.set_move(move)
        clone.make_move()
        clone.alternate_turn()
        return clone