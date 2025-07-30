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


def alpha_beta(board, depth, alpha, beta, maximizing, turn, goats_remaining=0):
    if depth == 0 or is_terminal(board, goats_remaining):
        return evaluate_board(board, goats_remaining)

    moves = generate_valid_moves(board, turn, goats_remaining)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_board, eaten = apply_move(board, move, turn)
            # print('Calling alpha beta')
            eval = alpha_beta(new_board, depth - 1, alpha, beta, False, 1 - turn, goats_remaining)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_board, eaten = apply_move(board, move, turn)
            eval = alpha_beta(new_board, depth - 1, alpha, beta, True, 1 - turn, goats_remaining)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def evaluate_board(board, goats_remaining=0):
    tiger_moves = len(generate_valid_moves(board, 0, goats_remaining))
    goat_moves = len(generate_valid_moves(board, 1, goats_remaining))
    
    # Base score from captures
    score = (board.eaten_goats * 300)
    
    # Mobility score
    score += (tiger_moves * 2) - (goat_moves * 3)
    
    # Bonus for goats during placement phase
    if goats_remaining > 0:
        score -= goats_remaining * 50  # Encourage placing goats early
    
    # Bonus for blocking tiger movements
    if tiger_moves == 0 and board.eaten_goats < 5:
        score -= 1000  # Big bonus for goats if tigers are blocked
    
    return score


def is_terminal(board, goats_remaining=0):
    # Game ends if tigers eat 5 goats
    if board.eaten_goats >= 5:
        return True
    
    # Game ends if tigers have no moves (goats win)
    if len(generate_valid_moves(board, 0, goats_remaining)) == 0:
        return True
    
    # Game ends if goats have no moves and no goats left to place
    if goats_remaining == 0 and len(generate_valid_moves(board, 1, goats_remaining)) == 0:
        return True
    
    return False
