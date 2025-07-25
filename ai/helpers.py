def handle_ai_move(board, turn, goats_remaining, eaten_goats):
    move = get_best_ai_move(board, turn, goats_remaining)
    if move:
        new_board, eaten = apply_move(board, move, turn)
        return new_board, not turn, goats_remaining, eaten_goats + eaten
    return board, not turn, goats_remaining, eaten_goats


def get_best_ai_move(board, turn, goats_remaining):
    from ai.alpha_beta import alpha_beta
    best_score = float('-inf')
    best_move = None

    print('Calling to get moves')
    moves = generate_valid_moves(board, turn, goats_remaining)
    print('After getting moves')
    for move in moves:
        new_board, eaten = apply_move(board, move, turn)
        score = alpha_beta(new_board, depth=4, alpha=-999,
                           beta=-999, maximizing=False, turn=1-turn)

        if score > best_score:
            best_score = score
            best_move = move
    #print(f'Best MOve {best_move}')
    return best_move


def generate_valid_moves(board, turn, goats_remaining):
    moves = []
    pieces = board.get_all_pieces(turn)
    # print(f'Getting all the pieces {pieces}')

    if turn == True:
        if goats_remaining > 0:
            print('Testing here')
            for node in board.nodes:
                print(f'Printing board.nodes {board.nodes}')
                if board.get_piece_at(*node) == 0:
                    print(f'is empty Node {node}')
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
            # print(f'Node {node}')
            # print(f'jumps can be done from {jumps}')

            for jump in jumps:
                moves.append((node, jump[1]))

    return moves


def apply_move(board, move, turn):
    new_board = board.clone()
    from game.move import Move
    move_obj = Move(new_board)

    # Carry over current eaten goats count (if your clone() doesn't do it)
    new_board.eaten_goats = board.eaten_goats

    src, dest = move
    eaten = 0

    if turn:  # Goat
        if src is None:
            index_dest = board.single_node_to_index(dest)
            print(f'Drop goat at index {index_dest}')
            move_obj.drop_goat(index_dest)
            print('Excuted the function drop_goat')
        else:
            i, j = board.node_to_index(src, dest)
            new_board.update_board((i, j))
    else:  # Tiger
        if new_board.is_tiger_jump(src, dest):
            jumped = new_board.get_middle_position(src, dest)
            new_board.remove_piece(jumped)
            eaten = 1
            new_board.eaten_goats += 1

        i, j = board.node_to_index(src, dest)
        new_board.update_board((i, j))

    return new_board, eaten


def get_possible_tiger_jumps(boardIns, tiger_pos):
    from game.board import Board
    # print(f'Calling Board')
    allNodes = boardIns.calculate_nodes()
    # print(f'After calling board Ins')
    jumps = []

    # print(f'Tiger Pos is {tiger_pos}')
    # print(f'All Nodes {allNodes}')
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
        # print(f'Top left corner')
    elif row == 0 and col == num_cols - 1:
        offsets = top_right_corner_offsets
        # print(f'Top right corner')
    elif row == num_rows - 1 and col == 0:
        offsets = bottom_left_corner_offsets
        # print(f'bottom left corner')
    elif row == num_rows - 1 and col == num_cols - 1:
        offsets = bottom_right_corner_offsets
        # print(f'bottom right corner')

    elif row == 0:
        offsets = top_edge_with_diagonal_offsets if col == 2 else top_edge_offsets

    elif row == num_rows - 1:
        offsets = bottom_edge_with_diagonal_offsets if col == 2 else bottom_edge_offsets

    elif col == 0:
        offsets = left_edge_with_diagonal_offsets if row == 2 else left_edge_offsets

    elif col == num_cols - 1:
        offsets = right_edge_with_diagonal_offsets if row == 2 else right_edge_offsets

        # print('right edge with diagonal')
    else:
        if ((pos_x + pos_y) // 100) % 2 == 0:
            offsets = middle_offsets
            # print('Middle offset')
        else:
            offsets = middle_offsets_no_diagonal
            # print('Middle offset with diagonal')

    for offset in offsets:
        neighbor_index = current_index + offset
        if 0 <= neighbor_index < len(allNodes):
            # print('Neighbour Index ',neighbor_index)
            goat_pos = allNodes[neighbor_index]
            # print('Goats Positions are ',goat_pos)
            if boardIns.get_piece_at(*goat_pos) == 2:  # goat
                double_jump_index = current_index + 2 * offset
                if 0 <= double_jump_index < len(allNodes):
                    jump_pos = allNodes[double_jump_index]
                    if boardIns.get_piece_at(*jump_pos) == 0:  # empty
                        jumps.append((goat_pos, jump_pos))

    # print(f'Returning jumps {jumps}')
    return jumps
