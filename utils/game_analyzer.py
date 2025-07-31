import os
import copy
from game.board import Board
from game.move import Move
from ai.helpers import get_best_move_for_analysis, apply_move, generate_valid_moves


class GameAnalyzer:
    def __init__(self, move_file):
        self.move_file = move_file
        self.moves = self.read_moves()
        self.analysis = [None] * len(self.moves)

    def read_moves(self):
        if not os.path.exists(self.move_file):
            return []
        with open(self.move_file, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def analyze_moves(self):
        """Lazy evaluation for each move - only compute when requested."""
        return [self.analyze_move_at_index(i) for i in range(len(self.moves))]

    def analyze_move_at_index(self, index):
        if self.analysis[index] is not None:
            return self.analysis[index]

        board = Board()
        move_obj = Move(board)
        goats_remaining = 20
        eaten_goats = 0
        turn = True  # True = Goat, False = Tiger

        # Rebuild board state up to move before current index
        for i in range(index):
            move = self.moves[i]
            from_str, to_str = move.split(') (')
            from_str = from_str.replace('(', '')
            to_str = to_str.replace(')', '')
            from_pos = tuple(map(int, from_str.split(',')))
            to_pos = tuple(map(int, to_str.split(',')))

            if from_pos == (0, 0):
                move_obj.drop_goat(to_pos)
                goats_remaining -= 1
            else:
                apply_move(board, (from_pos, to_pos), not turn)
                if not turn and board.is_tiger_jump(from_pos, to_pos):
                    eaten_goats += 1
            turn = not turn

        move = self.moves[index]
        from_str, to_str = move.split(') (')
        from_str = from_str.replace('(', '')
        to_str = to_str.replace(')', '')
        from_pos = tuple(map(int, from_str.split(',')))
        to_pos = tuple(map(int, to_str.split(',')))

        board_before = board.clone()
        goats_before = goats_remaining
        turn_before = turn

        is_blunder = False
        blunder_reason = None

        if from_pos == (0, 0):
            move_obj.drop_goat(to_pos)
            goats_remaining -= 1
            tiger_moves = generate_valid_moves(board, False, goats_remaining)
            for tiger_move in tiger_moves:
                src, dest = tiger_move
                if board.is_tiger_jump(src, dest):
                    middle = board.get_middle_position(src, dest)
                    if middle == to_pos:
                        is_blunder = True
                        blunder_reason = "Tiger can eat dropped goat"
                        break
        else:
            apply_move(board, (from_pos, to_pos), not turn)
            if not turn and board.is_tiger_jump(from_pos, to_pos):
                eaten_goats += 1

        best_move = get_best_move_for_analysis(board_before, turn_before, goats_before)
        best_move_str = str(best_move) if best_move else "None"

        from ai.alpha_beta import alpha_beta

        if best_move is None:
            valid_moves = generate_valid_moves(board_before, turn_before, goats_before)
            if not valid_moves:
                quality = "ok"
            else:
                is_blunder = True
                blunder_reason = "No best move found but game not over"
        else:
            best_board, _ = apply_move(board_before, best_move, turn_before)
            score_best = alpha_beta(best_board, depth=3, alpha=-9999, beta=9999,
                                    maximizing=not turn_before, turn=not turn_before,
                                    goats_remaining=goats_before)

            played_move = (None, to_pos) if from_pos == (0, 0) else (from_pos, to_pos)
            try:
                played_board, _ = apply_move(board_before, played_move, turn_before)
                score_played = alpha_beta(played_board, depth=3, alpha=-9999, beta=9999,
                                          maximizing=not turn_before, turn=not turn_before,
                                          goats_remaining=goats_before)
            except Exception:
                score_played = None

            if is_blunder:
                quality = "blunder"
            elif score_best is not None and score_played is not None:
                diff = abs(score_played - score_best)
                if diff < 50:
                    quality = "excellent"
                elif diff < 150:
                    quality = "good"
                elif diff < 300:
                    quality = "bad"
                else:
                    quality = "blunder"
            elif best_move == played_move:
                quality = "excellent"
            else:
                quality = "ok"

        self.analysis[index] = {
            "move": move,
            "quality": quality,
            "best_move": best_move_str,
            "blunder_reason": blunder_reason,
        }

        return self.analysis[index]
