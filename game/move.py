import numpy as np
# from .board import Board


class Move:
    def __init__(self, board,goats_remaining=20,eaten_goats=0):
        self.board = board
        self.goats_remaining = goats_remaining
        self.eaten_goats = eaten_goats

    def is_valid_move(self, from_pos, to_pos, player_turn):

        # from_x, from_y = from_pos
        to_x, to_y = to_pos

        # print("move is valid from ", from_x, from_y, "to ",
        #   to_x, to_y, "Player turn ", player_turn)
        piece_at_destination = self.board.get_piece_at(to_x, to_y)
        if player_turn == False:  # Turn of Tiger
            if piece_at_destination in (1,2):
                print("Invalid tiger move piece exists in the node")
                return False
            else:
                surrounding_node = self.board.get_surrounding_nodes(from_pos)
                # print(f'Gettin piece of surroundin node: {surrounding_node}')
                pieces = self.board.get_surrounding_node_piece(
                    surrounding_node)
                # for (row,col),piece in pieces:
                #     print(f'pieces at ({row},{col}):{piece}')

                if to_pos in surrounding_node:
                    initial_pos, final_pos = self.board.node_to_index(
                        from_pos, to_pos)
                    self.move_piece(initial_pos, final_pos, player_turn)
                    return True
                else:
                    print('Invalid Move')
        else:  # Turn of Goat
            if piece_at_destination is not None and piece_at_destination == 2 or piece_at_destination == 1:
                print("Invalid Goat move piece exists in the node")

                return False
            elif self.goats_remaining > 0:
                initial_pos, final_pos = self.board.node_to_index(
                    from_pos, to_pos)
                self.drop_goat(to_pos)
                self.goats_remaining -= 1
                print(f'Remaining Goats are: {self.goats_remaining}')

            elif self.goats_remaining == 0:
                surrounding_node = self.board.get_surrounding_nodes(from_pos)

                if to_pos in surrounding_node:
                    initial_pos, final_pos = self.board.node_to_index(
                        from_pos, to_pos)
                    self.move_piece(initial_pos, final_pos, player_turn)
                    return True
                else:
                    print('Invalid Goat move')

    def move_piece(self, from_pos, to_pos, player_turn):
        from_x, from_y = from_pos
        to_x, to_y = to_pos

        if player_turn:
            print(
                f'Moving Goat from pos x {from_x} y num_columns{from_y} to pos x {to_x} y {to_y}')
            self.board.update_board((from_pos, to_pos))

        else:
            print(
                f'Moving Tiger from pos x {from_x} y {from_y} to pos x {to_x} y {to_y}')
            self.board.update_board((from_pos, to_pos))

        print('updated board \n', self.board)

    def drop_goat(self, to_pos):

        to_x, to_y = to_pos
        if self.board.piece_exists_in_node(to_x, to_y, False):
            print('Piece exists ni thhe node')
            return self.goats_remaining, False

        else:
            print("Pece doesn't' exsts in the board")
            index = self.board.single_node_to_index(to_pos)
            print('index of board is ', index)
            self.board.update_goat(index)
            self.goats_remaining -= 1
            if self.goats_remaining >= 0:
                print(
                    f'Goats remaining are (in move class){self.goats_remaining}')
                return self.goats_remaining, True
            else:
                return self.goats_remaining, False

    def is_valid_tiger_eat_move(self, selected_piece, target_node):
        print(
            f'Checking tiger eat andcurrent pos {selected_piece},{target_node}')
        sx, sy = selected_piece
        tx, ty = target_node

        dx = tx - sx
        dy = ty - sy

        if not self.board.get_piece_at(tx,ty):
            if abs(dx) == 2 or abs(dy) == 2:
                mid_x = sx + dx // 2
                mid_y = sy + dy // 2

                # Checkin if its in bound
                if 0 <= mid_x < 5 and 0 <= mid_y < 5 and 0 <= tx < 5 and 0 <= ty < 5:
                    mid_piece = self.board.get_piece_at_index(mid_x, mid_y)
                    dest_piece = self.board.get_piece_at_index(tx, ty)

                    # Checking middle node is goat and destination is empty
                    if mid_piece == 2 and dest_piece == 0:
                        return True, (mid_x, mid_y)

        return False, None

    # def is_valid_tiger_jump(self,current_pos,goat_pos,jump_pos):
    #     print('------------------')
    #     print(f'Current pos {current_pos} goat position is {goat_pos} destination positition{jump_pos}')

    #     print('------------------')

    def is_valid_tiger_jump(self, current_pos, goat_pos, jump_pos):
        from .board import Board
        self.boardIns = Board()
        self.nodes = self.boardIns.calculate_nodes()

        print('------------------')
        print(
            f'Current pos: {current_pos}, Goat pos: {goat_pos}, Destination pos: {jump_pos}')
        print('------------------')

        print(f'Nodes are: {self.nodes}')

        if current_pos not in self.nodes or goat_pos not in self.nodes or jump_pos not in self.nodes:
            print("One or more positions are invalid")
            return False

        current_index = self.nodes.index(current_pos)
        goat_index = self.nodes.index(goat_pos)
        jump_index = self.nodes.index(jump_pos)

        index_diff = goat_index - current_index

        print(f'Offset from current to goat: {index_diff}')

        # Get surrounding nodes with offsets similar to get_surrounding_nodes
        pos_y, pos_x = current_pos  # ⬅️ Reversed here!

        num_columns = 5
        num_rows = 5
        index = current_index
        row = index // num_columns
        col = index % num_columns

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
            # print(f'offset was top left corner')
        elif row == 0 and col == num_columns - 1:
            # print(f'offset was top right corner')
            offsets = top_right_corner_offsets
        elif row == num_rows - 1 and col == 0:
            # print(f'offset was bottom left corner')
            offsets = bottom_left_corner_offsets
        elif row == num_rows - 1 and col == num_columns - 1:
            # print(f'offset was bottom right corner')
            offsets = bottom_right_corner_offsets
        elif row == 0:
            # print(f'Printing col for top edge {col}')
            if col == 2:
                offsets = top_edge_with_diagonal_offsets
            else:
                offsets = top_edge_offsets

            # print(f'offset is top edgeg')
            
        elif row == num_rows - 1:
            # print(f'Printing col for bottom edge {col}')
            if col == 2:
                offsets = bottom_edge_with_diagonal_offsets
            else: 
                offsets = bottom_edge_offsets
            
            # print(f'offset is bottom edgeg')
        elif col == 0:
            # print(f'Printing col for left edge {col}')
            if row == 2:
                offsets = left_edge_with_diagonal_offsets
            else: 
                offsets = left_edge_offsets

            # print(f'offset is left edgeg')
        elif col == num_columns - 1:
            # print(f'Printing col for right edge {col}')
            if row == 2:
                offsets = right_edge_with_diagonal_offsets
            else:        
             offsets = right_edge_offsets
        else:
            # Middle node - choose diagonal or no-diagonal based on pattern
            if ((pos_x + pos_y) // 100) % 2 == 0:  # Note: this still uses swapped values!

                offsets = middle_offsets
                # print('Offset middle offset')
            else:
                # print('offset is middle with no diagonal')
                offsets = middle_offsets_no_diagonal

        # print(f"Possible offsets from current node: {offsets}")

        for offset in offsets:
            neighbor_index = current_index + offset
            if 0 <= neighbor_index < len(self.nodes) and self.nodes[neighbor_index] == goat_pos:
                print(f"Matched offset to goat: {offset}")
                double_jump_index = current_index + 2 * offset
                if 0 <= double_jump_index < len(self.nodes):
                    print(
                        f"Doubled jump destination index: {double_jump_index}")
                    expected_jump_pos = self.nodes[double_jump_index]
                    print(f"Expected jump pos: {expected_jump_pos}")
                    # return expected_jump_pos == jump_pos
                    if expected_jump_pos == jump_pos:
                        print('Tiger ate a goat!')
                        # self.eaten_goats += 1
                        return True
                else:
                    print("Jump destination is out of bounds.")
                    return False

        print("No matching offset from current to goat.")
        return False

    def check_game_over(self):
        # Tigers win if they eat 5 goats
        if self.eaten_goats >= 5:
            return "Tiger"

        tiger_positions = self.board.get_all_tiger_positions()
        # print('Tigers pos are : ', tiger_positions)

        for tiger_pos in tiger_positions:
            surrounding_nodes = self.board.get_surrounding_nodes(tiger_pos)
            for neighbor in surrounding_nodes:
                # print(f'Tiger pos sending in function: {tiger_pos}')
                # print(f'Neighbour pos sending in function: {neighbor}')
                if self.board.is_valid_tiger_move(tiger_pos, neighbor):
                    return None  # A tiger can still move, game is not over

        return "Goat"  # No tiger can move, goats win

    def get_trapped_tigers_count(self):
        tiger_positions = self.board.get_all_tiger_positions()
        trapped = 0
        for tiger_pos in tiger_positions:
            movable = False
            neighbors = self.board.get_surrounding_nodes(tiger_pos)
            for neighbor in neighbors:
                if self.board.is_valid_tiger_move(tiger_pos, neighbor):
                    movable = True
                    break
            if not movable:
                trapped += 1
        return trapped
