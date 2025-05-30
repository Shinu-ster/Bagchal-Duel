# from ai.helpers import evaluate_board, generate_valid_moves, apply_move, is_terminal
# from game.move import Move
from ai.helpers import generate_valid_moves,apply_move

# def alpha_beta(board, depth, alpha, beta, maximizing_player, turn, move_obj,goats_remaining):
#     if depth == 0 or is_terminal(board, move_obj):
#         return evaluate_board(board)

#     possible_moves = generate_valid_moves(board, turn,goats_remaining)

#     if maximizing_player:
#         max_eval = float('-inf')
#         for m in possible_moves:
#             print(f'All Possible moves: {m}')
#             new_board = apply_move(board, m, turn)
#             new_move_obj = Move(new_board)  # Create updated Move object
#             eval = alpha_beta(new_board, depth - 1, alpha, beta, False, not turn, new_move_obj)
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for m in possible_moves:
#             new_board = apply_move(board, m, turn)
#             new_move_obj = Move(new_board)
#             eval = alpha_beta(new_board, depth - 1, alpha, beta, True, not turn, new_move_obj)
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval


def alpha_beta(board, depth, alpha, beta, maximizing, turn):
    if depth == 0 or is_terminal(board):
        return evaluate_board(board)

    moves = generate_valid_moves(board, turn, goats_remaining=0)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move, turn)
            print('Calling alpha beta')
            eval = alpha_beta(new_board, depth - 1, alpha, beta, False, 1 - turn)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move, turn)
            eval = alpha_beta(new_board, depth - 1, alpha, beta, True, 1 - turn)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def evaluate_board(board):
    tiger_moves = len(generate_valid_moves(board, 0, 0))
    goat_moves = len(generate_valid_moves(board, 1, 0))
    score = (board.eaten_goats * 100) + tiger_moves - goat_moves
    return score


def is_terminal(board):
    return board.eaten_goats >= 5 or len(generate_valid_moves(board, 0, 0)) == 0
