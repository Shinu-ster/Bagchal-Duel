
# import copy
# from game.move import Move


# def evaluate_board(board):
#     goats_remaining = board.get_goats_remaining()
#     tigers_trapped = board.get_tigers_trapped()
#     goats_eaten = board.get_goats_eaten()

#     score = (goats_remaining * 10) - (goats_eaten * 20) + (tigers_trapped * 15)
#     return score


# def generate_valid_moves(current_board, turn, goats_remaining):
#     print()
#     print('Reaches Generate Valid Moves:')
#     print()
#     all_moves = []
#     pieces = current_board.get_all_pieces(turn)
#     print(f'Getting all the pieces: {pieces}')

#     move_instance = Move(current_board)

#     if turn == 1:  # Goat turn
#         if goats_remaining > 0:
#             for node in current_board.nodes:
#                 print()
#                 print(
#                     f'Working on node {node} still in function generate valid moves')
#                 print()
#                 if current_board.get_piece_at(*node) == 0:
#                     # Goat placement (None as src)
#                     all_moves.append((None, node))
#                     print(f'All moves are such {all_moves}')
#         else:
#             for piece in pieces:
#                 print(f"[DEBUG] node passed to index_to_single_node: {piece}")
#                 # Convert from board indices to screen coordinates
#                 node = current_board.index_to_single_node(*piece)
#                 neighbors = current_board.get_surrounding_nodes(node)

#                 for neighbor in neighbors:
#                     if isinstance(neighbor, (list, tuple)) and len(neighbor) == 1:
#                         neighbor = neighbor[0]

#                     if current_board.get_piece_at(*neighbor) == 0:
#                         if move_instance.is_valid_move(piece, neighbor, turn):
#                             # Board index piece, screen coord neighbor
#                             all_moves.append((piece, neighbor))
#     else:  # Tiger turn
#         for piece in pieces:
#             print(f'Printing pieces: {piece}')
#             print(f'Printing pieces: {piece[0]} {piece[1]}')

#             # Convert from board indices to screen coordinates
#             node = current_board.index_to_single_node(piece[0], piece[1])
#             print(f"Node of that index is {node}")
#             neighbors = current_board.get_surrounding_nodes(node)

#             for neighbor in neighbors:
#                 if isinstance(neighbor, (list, tuple)) and len(neighbor) == 1:
#                     neighbor = neighbor[0]

#                 if current_board.get_piece_at(*neighbor) == 0:
#                     if move_instance.is_valid_move(node, neighbor, turn):
#                         # Add valid move in screen coords
#                         all_moves.append((node, neighbor))

#             # Get valid tiger jumps
#             jumps = get_possible_tiger_jumps(current_board, node)
#             for jump in jumps:
#                 # assuming jump = (middle_pos, landing_pos)
#                 if move_instance.is_valid_tiger_jump(piece, jump[0], jump[1]):
#                     # Add valid tiger jump in screen coords
#                     all_moves.append((node, jump[1]))

#     print()
#     print('Returned all Moves')
#     print(f'Returning Moves are {all_moves}')
#     print()
#     return all_moves


# def get_possible_tiger_jumps(board, tiger_pos):
#     possible_jumps = []
#     nodes = board.calculate_nodes()  # Or use board.nodes if it's precomputed
#     current_index = nodes.index(tiger_pos)

#     # Determine valid offsets using your existing logic
#     pos_y, pos_x = tiger_pos  # Reversed, as per your setup

#     num_columns = 5
#     num_rows = 5
#     row = current_index // num_columns
#     col = current_index % num_columns

#     # These offset sets must match your jump logic in is_valid_tiger_jump
#     middle_offsets = [-5, -4, +1, +6, +5, +4, -1, -6]
#     middle_offsets_no_diagonal = [+1, -1, +5, -5]
#     top_left_corner_offsets = [+1, +5, +6]
#     top_right_corner_offsets = [-1, +4, +5]
#     bottom_left_corner_offsets = [+1, -4, -5]
#     bottom_right_corner_offsets = [-1, -5, -6]
#     left_edge_offsets = [+5, +1, -5]
#     right_edge_offsets = [+5, -5, -1]
#     top_edge_offsets = [+1, -1, +5]
#     bottom_edge_offsets = [+1, -1, -5]
#     bottom_edge_with_diagonal_offsets = [+1, -1, -4, -5, -6]
#     left_edge_with_diagonal_offsets = [+1, +5, +6, -4, -5]
#     right_edge_with_diagonal_offsets = [-1, -5, -6, +4, +5]
#     top_edge_with_diagonal_offsets = [+1, -1, +4, +5, +6]

#     # Assign offsets based on location
#     if row == 0 and col == 0:
#         offsets = top_left_corner_offsets
#     elif row == 0 and col == num_columns - 1:
#         offsets = top_right_corner_offsets
#     elif row == num_rows - 1 and col == 0:
#         offsets = bottom_left_corner_offsets
#     elif row == num_rows - 1 and col == num_columns - 1:
#         offsets = bottom_right_corner_offsets
#     elif row == 0:
#         offsets = top_edge_with_diagonal_offsets if col == 2 else top_edge_offsets
#     elif row == num_rows - 1:
#         offsets = bottom_edge_with_diagonal_offsets if col == 2 else bottom_edge_offsets
#     elif col == 0:
#         offsets = left_edge_with_diagonal_offsets if row == 2 else left_edge_offsets
#     elif col == num_columns - 1:
#         offsets = right_edge_with_diagonal_offsets if row == 2 else right_edge_offsets
#     else:
#         offsets = middle_offsets if (
#             (pos_x + pos_y) // 100) % 2 == 0 else middle_offsets_no_diagonal

#     for offset in offsets:
#         middle_index = current_index + offset
#         landing_index = current_index + 2 * offset

#         if 0 <= middle_index < len(nodes) and 0 <= landing_index < len(nodes):
#             goat_pos = nodes[middle_index]
#             jump_pos = nodes[landing_index]

#             # Check if there's a goat to jump over and the landing spot is empty
#             if board.get_piece_at(*goat_pos) == 1 and board.get_piece_at(*jump_pos) == 0:
#                 possible_jumps.append((goat_pos, jump_pos))

#     return possible_jumps


# def apply_move(board, move, turn):
#     new_board = board.clone()
#     print(f'Getting Moves: {move}')
#     src, dest = move

#     if turn == 0:
#         # Tiger move
#         if new_board.is_tiger_jump(src, dest):
#             jumped_goat = new_board.get_middle_position(src, dest)
#             new_board.remove_piece(jumped_goat)
#             new_board.eaten_goats += 1
#             print(f'Src is : {src}')

#         index_src = board.single_node_to_index(src)
#         index_dest = board.single_node_to_index(dest)
#         new_board.update_board((index_src, index_dest))

#     else:
#         # Goat move or placement
#         if src is None:
#             # Goat placement case
#             print("Placing new goat at:", dest)
#             index_dest = board.single_node_to_index(dest)
#             new_board.place_goat(index_dest)  # Assuming such a method exists
#         else:
#             # Regular goat move
#             index_src = board.single_node_to_index(src)
#             index_dest = board.single_node_to_index(dest)
#             new_board.update_board((index_src, index_dest))

#     return new_board


# def is_terminal(board, move):
#     return move.check_game_over() is not None


# def get_best_ai_move(board, turn, goats_remaining, depth=3):
#     """
#     Chooses the best move using Alpha-Beta pruning.
#     turn = 0 → Tiger's turn
#     turn = 1 → Goat's turn
#     """
#     from ai.alpha_beta import alpha_beta
#     best_move = None
#     best_eval = float('-inf') if turn == 0 else float('inf')
#     print('Reached Get Best ai move function')
#     print()

#     possible_moves = generate_valid_moves(board, turn, goats_remaining)
#     print("Helloooooooooooooooo")
#     print(f'Got possible moves {possible_moves}')

#     for move in possible_moves:
#         new_board = apply_move(board, move, turn)
#         move_obj = Move(new_board)

#         score = alpha_beta(
#             new_board,
#             depth - 1,
#             alpha=float('-inf'),
#             beta=float('inf'),
#             maximizing_player=(turn == 0),
#             turn=not turn,
#             move_obj=move_obj,
#             goats_remaining=goats_remaining if move[0] else goats_remaining - 1
#         )

#         if (turn == 0 and score > best_eval) or (turn == 1 and score < best_eval):
#             best_eval = score
#             best_move = move

#     return best_move


# def handle_ai_move(board, turn, goats_remaining):
#     """
#     Handles the AI move, updates the board.
#     `game` is an object that contains .board, .turn, .move, etc.
#     """
#     print(f'Handling turn of {turn}')
#     best_move = get_best_ai_move(board, turn, goats_remaining)

#     if best_move is not None:
#         src, dest = best_move

#         if src is None:
#             # Goat placement
#             Move.drop_goat(dest)
#         else:
#             # Movement (for goat or tiger)
#             sx, sy = board.single_node_to_index(src)
#             tx, ty = board.single_node_to_index(dest)

#             if turn == 0:  # Tiger move
#                 is_eat_move, goat_to_remove = Move.is_valid_tiger_eat_move(
#                     (sx, sy), (tx, ty))
#                 if is_eat_move:
#                     gx, gy = goat_to_remove
#                     board.update_board(((gx, gy), (gx, gy)))  # Remove goat

#             board.update_board(((sx, sy), (tx, ty)))  # Apply actual move

#     game.turn = not game.turn
#     game.selected_piece = None


def handle_ai_move(board, turn, goats_remaining):
    move = get_best_ai_move(board, turn, goats_remaining)
    if move:
        new_board = apply_move(board, move, turn)
        return new_board,not turn
    return board,not turn


def get_best_ai_move(board, turn, goats_remaining):
    from ai.alpha_beta import alpha_beta
    best_score = float('-inf')
    best_move = None

    print('Calling to get moves')
    moves = generate_valid_moves(board, turn, goats_remaining)
    print('After getting moves')
    for move in moves:
        new_board = apply_move(board, move, turn)
        score = alpha_beta(new_board, depth=3, alpha=-999,
                           beta=-999, maximizing=False, turn=1-turn)

        if score > best_score:
            best_score = score
            best_move = move
    print(f'Best MOve {best_move}')
    return best_move


def generate_valid_moves(board, turn, goats_remaining):
    moves = []
    pieces = board.get_all_pieces(turn)
    # print(f'Getting all the pieces {pieces}')

    if turn == True:
        if goats_remaining > 0:
            for node in board.nodes:
                if board.get_piece_at(*node) == 0:
                    moves.append((None, node))  # Placement for goats
        else:  # if can't drop any more goats
            for row, col in pieces:
                node = board.index_to_single_node(row, col)
                neighbors = board.get_surrounding_nodes(node)
                for neighbor in neighbors:
                    # If neighboring nodes are empty
                    if board.get_piece_at(*neighbor) == 0:
                        moves.append((node, neighbor))

    else:  # Tigers move
        for row, col in pieces:
            node = board.index_to_single_node(row, col)
            neighbors = board.get_surrounding_nodes(node)
            for neighbor in neighbors:
                if board.get_piece_at(*neighbor) == 0:
                    moves.append((node, neighbor))
            jumps = get_possible_tiger_jumps(board, node)
            # print(f'jumps can be done from {jumps}')

            for jump in jumps:
                moves.append((node, jump[1]))

    return moves


def apply_move(board, move, turn):
    # print(f'Cloning Board')
    new_board = board.clone()
    src, dest = move

    if turn == True:  # Goat
        if src is None:
            index_dest = board.single_node_to_index(dest)
            new_board.place(index_dest)
        else:
            i,j = board.node_to_index(src,dest)
            new_board.update_board((i, j))
    else:  # Tiger
        if new_board.is_tiger_jump(src, dest):
            jumped = new_board.get_middle_position(src, dest)
            new_board.remove_piece(jumped)  # Removing the middle Goat
            new_board.eaten_goats += 1
        
        i,j = board.node_to_index(src,dest)
        # print(f'Index to move {i} {j}')
        new_board.update_board((i, j))
    # print('New board',new_board)
    return new_board


def get_possible_tiger_jumps(boardIns, tiger_pos):
    from game.board import Board
    # print(f'Calling Board')
    allNodes = boardIns.calculate_nodes()
    # print(f'After calling board Ins')
    jumps = []

    if tiger_pos not in allNodes:
        return jumps

    current_index = allNodes.index(tiger_pos)
    pos_x, pos_y = tiger_pos

    num_cols = 5
    num_rows = 5
    row = current_index // num_cols
    col = current_index % num_cols

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

    if row == 0 and col == 0:
        offsets = top_left_corner_offsets
    elif row == 0 and col == num_cols - 1:
        offsets = top_right_corner_offsets
    elif row == num_rows - 1 and col == 0:
        offsets = bottom_left_corner_offsets
    elif row == num_rows - 1 and col == num_cols - 1:
        offsets = bottom_right_corner_offsets
    elif row == 0:
        offsets = top_edge_with_diagonal_offsets if col == 2 else top_edge_offsets
    elif row == num_rows - 1:
        offsets = bottom_edge_with_diagonal_offsets if col == 2 else bottom_edge_offsets
    elif col == 0:
        offsets = left_edge_with_diagonal_offsets if row == 2 else left_edge_offsets
    elif col == num_cols - 1:
        offsets = right_edge_with_diagonal_offsets if row == 2 else right_edge_offsets
    else:
        if ((pos_x + pos_y) // 100) % 2 == 0:
            offsets = middle_offsets
        else:
            offsets = middle_offsets_no_diagonal

    for offset in offsets:
        neighbor_index = current_index + offset
        if 0 <= neighbor_index < len(allNodes):
            goat_pos = allNodes[neighbor_index]
            if boardIns.get_piece_at(*goat_pos) == 1:  # goat
                double_jump_index = current_index + 2 * offset
                if 0 <= double_jump_index < len(allNodes):
                    jump_pos = allNodes[double_jump_index]
                    if boardIns.get_piece_at(*jump_pos) == 0:  # empty
                        jumps.append((goat_pos, jump_pos))

    # print(f'Returning jumps {jumps}')
    return jumps
