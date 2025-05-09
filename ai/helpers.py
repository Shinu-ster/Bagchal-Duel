
import copy
from game.move import Move


def evaluate_board(board):
    goats_remaining = board.get_goats_remaining()
    tigers_trapped = board.get_tigers_trapped()
    goats_eaten = board.get_goats_eaten()

    score = (goats_remaining * 10) - (goats_eaten * 20) + (tigers_trapped * 15)
    return score


def generate_valid_moves(current_board, turn, goats_remaining):
    all_moves = []
    pieces = current_board.get_all_pieces(turn)
    print(f'Getting all the pieces: {pieces}')
    
    move_instance = Move(current_board)
    
    if turn == 1:  # Goat turn
        if goats_remaining > 0:
            for node in current_board.nodes:
                if current_board.get_piece_at(*node) == 0:
                    all_moves.append((None, node))  # Goat placement (None as src)
        else:
            for piece in pieces:    
                print(f"[DEBUG] node passed to index_to_single_node: {piece}")
                # Convert from board indices to screen coordinates
                node = current_board.index_to_single_node(*piece)
                neighbors = current_board.get_surrounding_nodes(node)

                for neighbor in neighbors:
                    if isinstance(neighbor, (list, tuple)) and len(neighbor) == 1:
                        neighbor = neighbor[0]

                    if current_board.get_piece_at(*neighbor) == 0:
                        if move_instance.is_valid_move(piece, neighbor, turn):
                            all_moves.append((piece, neighbor))  # Board index piece, screen coord neighbor
    else:  # Tiger turn
        for piece in pieces:
            print(f'Printing pieces: {piece}')
            print(f'Printing pieces: {piece[0]} {piece[1]}')

            # Convert from board indices to screen coordinates
            node = current_board.index_to_single_node(piece[0], piece[1])
            print(f"Node of that index is {node}")
            neighbors = current_board.get_surrounding_nodes(node)

            for neighbor in neighbors:
                if isinstance(neighbor, (list, tuple)) and len(neighbor) == 1:
                    neighbor = neighbor[0]

                if current_board.get_piece_at(*neighbor) == 0:
                    if move_instance.is_valid_move(node, neighbor, turn):
                        all_moves.append((node, neighbor))  # Add valid move in screen coords

            # Get valid tiger jumps
            jumps = get_possible_tiger_jumps(current_board, node)
            for jump in jumps:
                # assuming jump = (middle_pos, landing_pos)
                if move_instance.is_valid_tiger_jump(piece, jump[0], jump[1]):
                    all_moves.append((node, jump[1]))  # Add valid tiger jump in screen coords

    return all_moves



def get_possible_tiger_jumps(board, tiger_pos):
    possible_jumps = []
    nodes = board.calculate_nodes()  # Or use board.nodes if it's precomputed
    current_index = nodes.index(tiger_pos)

    # Determine valid offsets using your existing logic
    pos_y, pos_x = tiger_pos  # Reversed, as per your setup

    num_columns = 5
    num_rows = 5
    row = current_index // num_columns
    col = current_index % num_columns

    # These offset sets must match your jump logic in is_valid_tiger_jump
    middle_offsets = [-5, -4, +1, +6, +5, +4, -1, -6]
    middle_offsets_no_diagonal = [+1, -1, +5, -5]
    top_left_corner_offsets = [+1, +5, +6]
    top_right_corner_offsets = [-1, +4, +5]
    bottom_left_corner_offsets = [+1, -4, -5]
    bottom_right_corner_offsets = [-1, -5, -6]
    left_edge_offsets = [+5, +1, -5]
    right_edge_offsets = [+5, -5, -1]
    top_edge_offsets = [+1, -1, +5]
    bottom_edge_offsets = [+1, -1, -5]
    bottom_edge_with_diagonal_offsets = [+1, -1, -4, -5, -6]
    left_edge_with_diagonal_offsets = [+1, +5, +6, -4, -5]
    right_edge_with_diagonal_offsets = [-1, -5, -6, +4, +5]
    top_edge_with_diagonal_offsets = [+1, -1, +4, +5, +6]

    # Assign offsets based on location
    if row == 0 and col == 0:
        offsets = top_left_corner_offsets
    elif row == 0 and col == num_columns - 1:
        offsets = top_right_corner_offsets
    elif row == num_rows - 1 and col == 0:
        offsets = bottom_left_corner_offsets
    elif row == num_rows - 1 and col == num_columns - 1:
        offsets = bottom_right_corner_offsets
    elif row == 0:
        offsets = top_edge_with_diagonal_offsets if col == 2 else top_edge_offsets
    elif row == num_rows - 1:
        offsets = bottom_edge_with_diagonal_offsets if col == 2 else bottom_edge_offsets
    elif col == 0:
        offsets = left_edge_with_diagonal_offsets if row == 2 else left_edge_offsets
    elif col == num_columns - 1:
        offsets = right_edge_with_diagonal_offsets if row == 2 else right_edge_offsets
    else:
        offsets = middle_offsets if ((pos_x + pos_y) // 100) % 2 == 0 else middle_offsets_no_diagonal

    for offset in offsets:
        middle_index = current_index + offset
        landing_index = current_index + 2 * offset

        if 0 <= middle_index < len(nodes) and 0 <= landing_index < len(nodes):
            goat_pos = nodes[middle_index]
            jump_pos = nodes[landing_index]

            # Check if there's a goat to jump over and the landing spot is empty
            if board.get_piece_at(*goat_pos) == 1 and board.get_piece_at(*jump_pos) == 0:
                possible_jumps.append((goat_pos, jump_pos))

    return possible_jumps


def apply_move(board, move,turn):
    new_board = board.clone()

    src, dest = move

    if turn == 0:
        if new_board.is_tiger_jump(src, dest):
            jumped_goat = new_board.get_middle_position(src, dest)
            new_board.remove_piece(jumped_goat)
            new_board.eaten_goats += 1
            print(f'Src is : {src}')
            index_src = board.single_node_to_index(src)
            index_dest = board.single_node_to_index(dest)
            new_board.update_board((index_src, index_dest))

        # new_board.update_board((src, dest))
    else:
        # new_board.update_board((src, dest))
        index_src = board.single_node_to_index(src)
        index_dest = board.single_node_to_index(dest)
        new_board.update_board((index_src, index_dest))

    return new_board


def is_terminal(board,move):
    return move.check_game_over() is not None


def handle_ai_move(board,turn,goats_remaining):
    print('This function called')
    print('Board')
    print(board)
    print(f'Turn is {turn}')
    print(f'Goats Remaining {goats_remaining}')
    pass