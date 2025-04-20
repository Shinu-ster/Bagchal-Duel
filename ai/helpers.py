
import copy
from game import move

def evaluate_board(board):
    goats_remaining = board.get_goats_remaining()
    tigers_trapped = board.get_tigers_trapped()
    goats_eaten = board.get_goats_eaten()

    score = (goats_remaining * 10) - (goats_eaten * 20) + (tigers_trapped * 15)
    return score


def generate_valid_moves(current_board, turn):
    all_moves = []
    pieces = current_board.get_all_pieces(turn)

    for piece in pieces:
        for neighbor in current_board.get_surrounding_nodes(piece):
            if current_board.piece_exists_in_node(*neighbor, turn=False):
                if move.is_valid_move(piece, neighbor, turn):
                    all_moves.append((piece, neighbor))

            if turn == 0:
                dx = neighbor[0] - piece[0]
                dy = neighbor[1] - piece[1]
                jump_dest = (neighbor[0] + dx, neighbor[1] + dy)

                if move.is_valid_tiger_jump(piece, neighbor, jump_dest):
                    all_moves.append((piece, jump_dest))
    return all_moves


def apply_move(board, move):
    new_board = copy.deepcopy(board)

    src, dest = move

    if board.turn == 0:
        if new_board.is_tiger_jump(src, dest):
            jumped_goat = new_board.get_middle_position(src, dest)
            new_board.remove_piece(jumped_goat)
            new_board.eaten_goats += 1
        new_board.move_piece(src, dest, is_tiger=True)
    else:
        new_board.move_piece(src, dest, is_tiger=False)

    return new_board


def is_terminal(board):
    return board.eaten_goats >= 5 or board.get_tigers_trapped() == 4
