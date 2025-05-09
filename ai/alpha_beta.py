from ai.helpers import evaluate_board, generate_valid_moves, apply_move, is_terminal
from game.move import Move

def alpha_beta(board, depth, alpha, beta, maximizing_player, turn, move_obj,goats_remaining):
    if depth == 0 or is_terminal(board, move_obj):
        return evaluate_board(board)

    possible_moves = generate_valid_moves(board, turn,goats_remaining)

    if maximizing_player:
        max_eval = float('-inf')
        for m in possible_moves:
            print(f'All Possible moves: {m}')
            new_board = apply_move(board, m, turn)
            new_move_obj = Move(new_board)  # Create updated Move object
            eval = alpha_beta(new_board, depth - 1, alpha, beta, False, not turn, new_move_obj)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for m in possible_moves:
            new_board = apply_move(board, m, turn)
            new_move_obj = Move(new_board)
            eval = alpha_beta(new_board, depth - 1, alpha, beta, True, not turn, new_move_obj)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
