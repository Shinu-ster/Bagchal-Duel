import numpy as np


class Move:
    def __init__(self, board):
        self.board = board
        self.goats_remaining = 20

    def is_valid_move(self, from_pos, to_pos, player_turn):

        from_x, from_y = from_pos
        to_x, to_y = to_pos

        # print("move is valid from ", from_x, from_y, "to ",
            #   to_x, to_y, "Player turn ", player_turn)
        piece_at_destination = self.board.get_piece_at(to_x, to_y)
        if player_turn == False:  # Turn of Tiger
            if piece_at_destination is not None and piece_at_destination == 1 or piece_at_destination == 2:
                print("Invalid tiger move piece exists in t{he node")
                return False
            else:
                surrounding_node = self.board.get_surrounding_nodes(from_pos)
                # print(f'Gettin piece of surroundin node: {surrounding_node}')
                # pieces = self.board.get_surrounding_node_piece(surrounding_node)
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
                initial_pos, final_pos = self.board.node_to_index(
                    from_pos, to_pos)
                self.move_piece(initial_pos, final_pos, player_turn)
                return True

    def move_piece(self, from_pos, to_pos, player_turn):
        from_x, from_y = from_pos
        to_x, to_y = to_pos

        if player_turn:
            print(
                f'Moving Goat from pos x {from_x} y {from_y} to pos x {to_x} y {to_y}')
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
            return False

        else:
            print("Pece doesn't' exsts in the board")
            index = self.board.single_node_to_index(to_pos)
            print('index of board is ', index)
            self.board.update_goat(index)
            self.goats_remaining -= 1
            print(f'Goats remaining are {self.goats_remaining}')
            return True

    
    