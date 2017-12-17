"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   12/17/2017 20:58
"""
class MiniMax:

    def __init__(self, gm):
        self.__manager = gm

    def mini_max(self):
        moves = self.__manager.get_pos_moves_mgr()
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            #print(move)
            clone = self.__manager.next_state(move, "Computer")
            score = self.__min_play(clone)
            if score > best_score:
                best_move = move
                best_score = score

        return best_move + 1

    def __min_play(self, game_state):
        if game_state.is_game_over():
            return game_state.get_board_mgr().evaluate_board()

        moves = game_state.get_pos_moves_mgr()
        best_score = float('inf')
        best_move = moves[0]
        for move in moves:
            clone = game_state.next_state(move, "Human")
            score = self.__max_play(clone)
            if score < best_score:
                best_score = score
                best_move = move

        return best_score

    def __max_play(self, game_state):
        if game_state.is_game_over():
            return game_state.get_board_mgr().evaluate_board()

        moves = game_state.get_pos_moves_mgr()
        best_score = float('-inf')
        best_move = moves[0]
        for move in moves:
            clone = game_state.next_state(move, "Computer")
            score = self.__min_play(clone)
            if score > best_score:
                best_score = score
                best_move = move

        return best_score