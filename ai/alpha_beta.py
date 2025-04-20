from ai.helpers import evaluate_board, generate_valid_moves, apply_move, is_terminal


def alpha_beta(board, depth, alpha, beta, maximizing_player, turn):
    if depth == 0 or is_terminal(board):
        return evaluate_board(board)

    moves = generate_valid_moves(board, turn)

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval = alpha_beta(new_board, depth - 1, alpha, beta, False, not turn)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval = alpha_beta(new_board, depth - 1, alpha, beta, True, not turn)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
