def handle_ai_move(board, turn, goats_remaining, eaten_goats):
    if turn:  # Goat
        print('Getting moves for goat AI')
        move,updated_goats_remaining = get_best_goat_ai_move(board, turn, goats_remaining)
    else:  # Tiger
        print('Getting moves for tiger AI')
        move = get_best_ai_move(board, turn, goats_remaining)

    if move:
        eaten = apply_move_in_place(board, move, turn)
        return move, not turn, updated_goats_remaining, eaten_goats + eaten

    return None, not turn, goats_remaining, eaten_goats


def get_best_goat_ai_move(board, turn, goats_remaining):
    from ai.alpha_beta import alpha_beta
    best_score = float('-inf')
    best_move = None

    moves = generate_valid_moves(board, turn, goats_remaining)
    for move in moves:
        new_board, eaten, updated_goats_remaining = apply_move(
            board, move, turn, goats_remaining)
        score = alpha_beta(
            new_board,
            depth=6,
            alpha=-999,
            beta=-999,
            maximizing=True,  # goat wants to maximize safety
            turn=1 - turn,
            goats_remaining=updated_goats_remaining
        )
        if score > best_score:
            best_score = score
            best_move = move
    return best_move, updated_goats_remaining


def get_best_ai_move(board, turn, goats_remaining):
    from ai.alpha_beta import alpha_beta
    best_score = float('-inf')
    best_move = None

    # print('Calling to get moves')
    moves = generate_valid_moves(board, turn, goats_remaining)
    print('After getting moves')
    for move in moves:
        new_board, eaten = apply_move(board, move, turn)
        score = alpha_beta(new_board, depth=4, alpha=-999,
                           beta=-999, maximizing=False, turn=1-turn, goats_remaining=goats_remaining)

        if score > best_score:
            best_score = score
            best_move = move
    # print(f'Best MOve {best_move}')
    return best_move


def get_best_move_for_analysis(board, turn, goats_remaining):
    from ai.alpha_beta import alpha_beta
    best_score = float('-inf') if turn else float('inf')
    best_move = None

    moves = generate_valid_moves(board, turn, goats_remaining)

    for move in moves:
        new_board, eaten = apply_move(board, move, turn, goats_remaining)
        score = alpha_beta(
            new_board,
            depth=4,
            alpha=float('-inf'),
            beta=float('inf'),
            maximizing=not turn,
            turn=not turn,
            goats_remaining=goats_remaining
        )

        if turn:  # Goat's turn (maximizing)
            if score > best_score:
                best_score = score
                best_move = move
        else:  # Tiger's turn (minimizing)
            if score < best_score:
                best_score = score
                best_move = move

    return best_move


def generate_valid_moves(board, turn, goats_remaining):
    moves = []
    pieces = board.get_all_pieces(turn)
    # print(f'Getting all the pieces {pieces}')

    if turn == True:
        if goats_remaining > 0:
            # print('Testing here')Testing
            for node in board.nodes:
                piece_at_node = board.get_piece_at(*node)
                # print(f'Node {node} has piece: {piece_at_node}')
                if piece_at_node == 0:
                    # print(f'is empty Node {node}')
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


def apply_move(board, move, turn, goats_remaining):
    new_board = board.clone()
    from game.move import Move
    move_obj = Move(new_board)

    # Carry over current eaten goats count (if your clone() doesn't do it)
    new_board.eaten_goats = board.eaten_goats

    # print(f'AI: Original board state: {board.board}')
    # print(f'AI: Cloned board state: {new_board.board}')

    src, dest = move
    eaten = 0

    if turn:  # Goat
        if src is None:
            # Goat placement
            # print(f'Drop goat at {dest}')
            move_obj.drop_goat(dest)
            goats_remaining -= 1
            # print('Executed the function drop_goat')
        else:
            # Goat movement
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

    return new_board, eaten, goats_remaining


def apply_move_in_place(board, move, turn):
    from game.move import Move
    move_obj = Move(board)
    src, dest = move
    eaten = 0

    if turn:  # Goat
        if src is None:
            move_obj.drop_goat(dest)
        else:
            i, j = board.node_to_index(src, dest)
            board.update_board((i, j))
    else:  # Tiger
        if board.is_tiger_jump(src, dest):
            jumped = board.get_middle_position(src, dest)
            board.remove_piece(jumped)
            eaten = 1
            board.eaten_goats += 1
        i, j = board.node_to_index(src, dest)
        board.update_board((i, j))
    return eaten


def get_possible_tiger_jumps(boardIns, tiger_pos):
    from game.board import Board
    # print(f'Calling Board')
    allNodes = boardIns.calculate_nodes()
    # print(f'After calling board Ins ',allNodes)
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
                    # print(f'Jump pos {jump_pos}')
                    # print(f'Curent pos {allNodes[current_index]}')
                    if boardIns.get_piece_at(*jump_pos) == 0:  # empty
                        jumps.append((goat_pos, jump_pos))

    # print(f'Returning jumps {jumps}')
    return jumps
