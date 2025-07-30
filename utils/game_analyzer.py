import os
from game.board import Board
from game.move import Move
from ai.helpers import get_best_ai_move, apply_move


class GameAnalyzer:
    def __init__(self, move_file):
        self.move_file = move_file
        self.moves = self.read_moves()
        self.analysis = []

    def read_moves(self):
        if not os.path.exists(self.move_file):
            return []
        with open(self.move_file, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def analyze_moves(self):
        self.analysis = []
        board = Board()
        move_obj = Move(board)
        goats_remaining = 20
        eaten_goats = 0
        turn = True  # True = Goat, False = Tiger
        for i, move in enumerate(self.moves):
            # Parse move
            from_str, to_str = move.split(') (')
            from_str = from_str.replace('(', '')
            to_str = to_str.replace(')', '')
            from_pos = tuple(map(int, from_str.split(',')))
            to_pos = tuple(map(int, to_str.split(',')))

            # Determine move type
            if from_pos == (0, 0):
                # Goat drop
                move_obj.drop_goat(to_pos)
                goats_remaining -= 1
            else:
                # Move (goat or tiger)
                apply_move(board, (from_pos, to_pos), not turn)
                if not turn:  # Tiger
                    # Check if it was a jump
                    if board.is_tiger_jump(from_pos, to_pos):
                        eaten_goats += 1
            # Evaluate move
            best_move = get_best_ai_move(board, turn, goats_remaining)
            if best_move == (from_pos, to_pos):
                quality = 'excellent'
            else:
                # Optionally, you can use evaluation score difference for more granularity
                quality = 'ok' if best_move else 'bad'
            self.analysis.append({'move': move, 'quality': quality})
            turn = not turn
        return self.analysis

    def get_move_quality(self, index):
        if 0 <= index < len(self.analysis):
            return self.analysis[index]['quality']
        return None

    def get_move(self, index):
        if 0 <= index < len(self.moves):
            return self.moves[index]
        return None
