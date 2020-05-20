"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   17.05.2020 23:38
"""
import random

from alpha_beta.ai_decorator import AiDecorator
from alpha_beta.ai_interface import AI


class AlphaBetaPruning(AI):  # Concrete component

    def __init__(self, state, depth):
        self.__state = state
        self.__depth = depth

    @property
    def state(self):
        return self.__state

    def compute_move(self):
        return self.__alpha_beta(self.__state, self.__depth)

    def __alpha_beta(self, state, depth) -> int:

        moves = state.state.valid_moves
        best_move = None
        best_score = float('-inf')
        beta = float('inf')

        for move in moves:
            clone = state.make_move_new_state(move)
            score = self.__minimize(clone, best_score, beta, depth - 1)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def __minimize(self, state, alpha: float, beta: float, depth: int) -> float:
        if state.game_over:
            return float('inf')
        if state.draw:
            return 0

        if depth == 0:
            return state.state.evaluate_board

        moves = state.state.valid_moves
        score = float('inf')
        for move in moves:
            clone = state.make_move_new_state(move)
            score = min(score, self.__maximize(clone, alpha, beta, depth - 1))
            if score <= alpha:
                return score
            beta = min(beta, score)
        return score

    def __maximize(self, state, alpha: float, beta: float, depth: int) -> float:
        if state.game_over:
            return float('-inf')
        if state.draw:
            return 0
        if depth == 0:
            return state.state.evaluate_board
        moves = state.state.valid_moves
        score = float('-inf')
        for move in moves:
            clone = state.make_move_new_state(move)
            score = max(score, self.__minimize(clone, alpha, beta, depth - 1))
            if score >= beta:
                return score
            alpha = max(score, alpha)
        return score


class AlphaBetaWithEnsureMove(AiDecorator):

    def __init__(self, ai_alg: AI):
        super().__init__(ai_alg)
        self.__ai_alg = ai_alg

    def compute_move(self):
        move = self.__ai_alg.compute_move()
        if move is None:
            return random.choice(self.__ai_alg.state.state.valid_moves)
        return move
