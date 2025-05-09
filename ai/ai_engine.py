from ai.alpha_beta import alpha_beta
from ai.helpers import evaluate_board, generate_valid_moves, apply_move, is_terminal
from game.move import Move


def get_best_ai_move(board, turn, goats_remaining):
    move_obj = Move(board)  # create the Move object using current board state
    best_score = float('-inf')
    best_move = None

    valid_moves = generate_valid_moves(board, turn,goats_remaining)
    for m in valid_moves:
        new_board = apply_move(board, m, turn)
        new_move_obj = Move(new_board)  # updated Move object for new board state
        score = alpha_beta(new_board, 3, float('-inf'), float('inf'), turn == 0, not turn, new_move_obj,goats_remaining)
        
        if score > best_score:
            best_score = score
            best_move = m

    return best_move


