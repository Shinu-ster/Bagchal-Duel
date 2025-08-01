# from ai.helpers import evaluate_board, generate_valid_moves, apply_move, is_terminal
# from game.move import Move
from ai.helpers import generate_valid_moves, apply_move

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
            new_board, eaten, updated_goats_remaining = apply_move(
                board, move, turn, goats_remaining)
            # print('Calling alpha beta')
            eval = alpha_beta(new_board, depth - 1, alpha, beta, False,
                              1 - turn, goats_remaining = updated_goats_remaining)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_board, eaten, updated_goats_remaining = apply_move(board, move, turn, goats_remaining)
            eval = alpha_beta(new_board, depth - 1, alpha,
                              beta, True, 1 - turn, goats_remaining = updated_goats_remaining)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def evaluate_board(board, goats_remaining=0):
    tiger_moves = len(generate_valid_moves(board, 0, goats_remaining))
    goat_moves = len(generate_valid_moves(board, 1, goats_remaining))

    score = (board.eaten_goats * 300)
    score += (tiger_moves * 2) - (goat_moves * 3)

    # Penalize unsafe goat placements (goats near tigers and vulnerable to being jumped)
    danger_penalty = 0
    tiger_positions = board.get_tiger_positions()
    # print(f'tiger Position {tiger_positions}')

    for tiger in tiger_positions:
        # print('Tiger Position ', tiger)
        # print(f'Converting index to node {board.index_to_single_node(*tiger)}')
        tiger_at_node = board.index_to_single_node(*tiger)
        surrounding = board.get_surrounding_nodes(tiger_at_node)
        # print(f'surrounding Nodes {surrounding}')
        for neighbor in surrounding:
            # print(f'neighbor {neighbor}')
            if board.is_goat_at_node(*neighbor):
                jump_pos = board.get_jump_position_ai(tiger, neighbor)
                # print('---------------')
                # print('Tiger is at Node ', {tiger})
                # print('Goat is at Node ', {neighbor})
                # print(f'Returned Jumped Position {jump_pos}')
                # print('---------------')
                if jump_pos and board.is_empty_at_node(jump_pos):
                    # This goat is in danger
                    danger_penalty += 450
                

    score -= danger_penalty

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
