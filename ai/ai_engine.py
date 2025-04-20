from ai.alpha_beta import alpha_beta
from ai.helpers import evaluate_board, generate_valid_moves, apply_move, is_terminal



def get_best_ai_move(board, turn):
    best_score = float('-inf') if turn == 0 else float('inf')
    best_move = None

    for move in generate_valid_moves(board, turn):
        new_board = apply_move(board, move)
        score = alpha_beta(new_board, 3, float('-inf'), float('inf'), turn == 0, not turn)
        if (turn == 0 and score > best_score) or (turn == 1 and score < best_score):
            best_score = score
            best_move = move
    return best_move


