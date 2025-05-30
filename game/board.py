import pygame
from constants import constant
from game.move import Move
import numpy as np
import copy


class Board:
    def __init__(self, skip_init=False):
        if skip_init:
            return  # Don’t call create_board or load anything

        self.grid_size = constant.BOARD_SIZE
        self.cell_size = constant.CELL_SIZE
        self.board = self.create_board()
        self.start_x = 200  # position of first node x
        self.start_y = 200  # position of first node y

        # Load images for tiger and goat
        self.tiger_image = pygame.image.load('assets/image/tigericon2.png')
        self.goat_image = pygame.image.load('assets/image/goaticon3.png')

        # Scale the images to be smaller
        self.tiger_image = pygame.transform.scale(
            self.tiger_image, (constant.CELL_SIZE/2, constant.CELL_SIZE/2))
        self.goat_image = pygame.transform.scale(
            self.goat_image, (constant.CELL_SIZE/2, constant.CELL_SIZE/2))

        # Define nodes (intersection points)
        self.nodes = self.calculate_nodes()

        # Track whose turn it is (True means Tiger's turn, False means Goat's turn)
        self.is_tigers_turn = True

        # List of goats placed on the board
        self.goats = []

    def create_board(self):
        """Initialize the board with tigers and empty spaces."""
        # Tigers = 1
        # Goat = 2
        board = np.array([
            [1, 0, 0, 0, 1],  # initialize tigers at spot 1
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
        ])

        # Place 4 tigers at the corners
        # board[0][0] = board[0][4] = board[4][0] = board[4][4] = "T"
        print('Board; ', board)

        # All other spaces are empty initially (goats will be placed during gameplay)
        return board

    def __str__(self):
        return str(self.board)

    def reset(self):
        self.board = self.create_board()

    def calculate_nodes(self):
        """Calculate the coordinates of the intersection nodes."""
        nodes = []
        cell_size = constant.CELL_SIZE

        # Calculate top-left position to center the board
        offset_x = (pygame.display.get_surface(
        ).get_width() - 5 * cell_size) // 2
        offset_y = (pygame.display.get_surface(
        ).get_height() - 5 * cell_size) // 2

        for i in range(5):  # 5 intersections in each direction
            for j in range(5):  # 5 intersections in each direction
                x = j * cell_size + offset_x + cell_size // 2
                y = i * cell_size + offset_y + cell_size // 2
                nodes.append((x, y))

        return nodes

    def draw_board(self, screen, selected_piece=None):
        """Draw the board grid and pieces on the screen."""
        screen.fill(constant.BG_COLOR)
        cell_size = constant.CELL_SIZE
        line_width = 4  # Thickness of the diagonal lines

        # Calculate top-left position to center the board
        offset_x = (screen.get_width() - constant.BOARD_ROW * cell_size) // 2
        offset_y = (screen.get_height() - constant.BOARD_COL * cell_size) // 2
        # Draw thick outer border around the whole board
        board_width = constant.BOARD_COL * cell_size
        board_height = constant.BOARD_ROW * cell_size
        outer_rect = pygame.Rect(offset_x, offset_y, board_width, board_height)

        pygame.draw.rect(screen, constant.GRID_COLOR,
                         outer_rect, line_width + 2)

        # Draw grid
        for i in range(constant.BOARD_ROW):  # Corrected to draw for a 5x5 grid
            for j in range(constant.BOARD_COL):  # Corrected to draw for a 5x5 grid
                x, y = j * cell_size + offset_x, i * cell_size + offset_y

                # Draw grid lines (rectangle borders)
                pygame.draw.rect(screen, constant.GRID_COLOR,
                                 (x, y, cell_size, cell_size), line_width)

                # Adjust diagonal lines to prevent overflow
                offset = line_width // 2  # Reduce overflow by half of the line width

                if (i + j) % 2 == 0:
                    pygame.draw.line(screen, constant.GRID_COLOR,
                                     (x + offset, y + offset), (x + cell_size - offset, y + cell_size - offset), line_width + 2)
                else:
                    pygame.draw.line(screen, constant.GRID_COLOR,
                                     (x + cell_size - offset, y + offset), (x + offset, y + cell_size - offset), line_width + 2)

        # Draw the nodes (intersection points) with a color
        self.draw_nodes(screen)

        if selected_piece:
            self.highlight_selected(screen, selected_piece)

        # Draw the pieces at the nodes (intersections)
        self.place_pieces_on_nodes(screen)

    def draw_nodes(self, screen):
        """Draw the nodes at intersections to show their positions."""
        node_color = (255, 0, 0)  # Red color for nodes (change this as needed)
        node_radius = 5  # Radius of the node circle
        node_pos = []

        for x, y in self.nodes:
            pygame.draw.circle(screen, node_color, (x, y), node_radius)
            node_pos.append((x, y))

        # print('Node Positions; ',node_pos)
        return node_pos

    def highlight_selected(self, screen, selected_node):
        if selected_node:
            row, col = self.single_node_to_index(selected_node)
            x = self.start_x + col * self.cell_size
            y = self.start_y + row * self.cell_size
            pygame.draw.circle(screen, (255, 215, 0),
                               (x, y), self.cell_size // 2.5)

    def place_pieces_on_nodes(self, screen):
        """Place the tiger and goat pieces on their respective nodes."""
        cell_size = constant.CELL_SIZE
        for i, (x, y) in enumerate(self.nodes):
            row, col = i // 5, i % 5  # Get the row and column index from the node index

            # Draw the tiger icon at the corners (nodes)
            if self.board[row][col] == 1:
                # Center the tiger icon on the node position
                screen.blit(self.tiger_image, (x - self.tiger_image.get_width() //
                            2, y - self.tiger_image.get_height() // 2))

            # If you add goats later, you can place them like this
            elif self.board[row][col] == 2:
                # Center the goat icon on the node position
                screen.blit(self.goat_image, (x - self.goat_image.get_width() //
                            2, y - self.goat_image.get_height() // 2))

    def update_board(self, move):
        """Update board after a move (for both player and AI)."""
        from_pos, to_pos = move
        x1, y1 = from_pos
        x2, y2 = to_pos

        # Move piece
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = 0  # Clear old position

    def update_goat(self, pos):
        x1, y1 = pos
        self.board[x1][y1] = 2

    def print_board(self):
        """Prints the board state in console (for debugging)."""
        for row in self.board:
            print(" ".join(row))
        print("\n")

    def return_nodes(self):
        return self.nodes

    def piece_exists_in_node(self, pos_x, pos_y, turn):
        row = (pos_y - self.start_y) // self.cell_size
        col = (pos_x - self.start_x) // self.cell_size

        if 0 <= row < 5 and 0 <= col < 5:
            # print(f"Checking board[{row}][{col}]")

            if turn == False:
                if self.board[row][col] == 1:
                    return True
                elif self.board[row][col] == 2:
                    return False
            elif turn == True:
                if self.board[row][col] == 0:
                    return True
                if self.board[row][col] == 1:
                    return False
                if self.board[row][col] == 2:
                    return True
            # if turn == False and self.board[row][col] == 1 or self.board[row][col] == 2:
            #     print("Either Tiger or Goat is present at that node")
            #     return True
            # elif turn == True and self.board[row][col] == 2 or self.board[row][col] == 1:
            #     print("Either Goat or tiger is present at that node")
            #     return True

        else:
            print("Clicked outside the board")
            return False

    def node_to_index(self, from_pos, to_pos):
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        initialRow = (from_y - self.start_y) // self.cell_size
        initialCol = (from_x - self.start_x) // self.cell_size

        finalRow = (to_y - self.start_y) // self.cell_size
        finalCol = (to_x - self.start_x) // self.cell_size

        if 0 <= initialRow < 5 and 0 <= initialCol < 5:
            # print(f"Index at initial Pos [{initialRow}][{initialCol}]")
            pass

        if 0 <= finalRow < 5 and 0 <= finalCol < 5:
            # print(f"Index at final Pos [{finalRow}][{finalCol}]")
            pass

        return (initialRow, initialCol), (finalRow, finalCol)

    def get_piece_at(self, pos_x, pos_y):
        row = (pos_y - self.start_y) // self.cell_size
        col = (pos_x - self.start_x) // self.cell_size
        if 0 <= row < 5 and 0 <= col < 5:
            return self.board[row][col]  # 1 = Tiger, 2 = Goat, 0 = Empty
        return None

    def get_surrounding_nodes(self, selected_node):
        if selected_node not in self.nodes:
            return "Node not found"

        pos_x, pos_y = selected_node
        # print(f'posx {pos_x} posy {pos_y}')

        index = self.nodes.index(selected_node)
        num_columns = 5
        num_rows = 5

        row = index // num_columns
        col = index % num_columns

        # Define offsets
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
        elif row == num_rows - 1:
            # print(f'Printing col for bottom edge {col}')
            if col == 2:
                offsets = bottom_edge_with_diagonal_offsets
            else:
                offsets = bottom_edge_offsets
        elif col == 0:
            # print(f'Printing col for left edge {row}')
            if row == 2:
                offsets = left_edge_with_diagonal_offsets
            else:
                offsets = left_edge_offsets
        elif col == num_columns - 1:
            # print(f'Printing col for right edge {row}')
            if row == 2:
                offsets = right_edge_with_diagonal_offsets
            else:
                offsets = right_edge_offsets
        else:
            # Middle node - choose diagonal or no-diagonal based on pattern
            if ((pos_x + pos_y) // 100) % 2 == 0:
                offsets = middle_offsets
                # print('Offset middle offset')
            else:
                # print('offset is middle with no diagonal')
                offsets = middle_offsets_no_diagonal

        # Find valid surrounding nodes
        surrounding_nodes = []
        for offset in offsets:
            new_index = index + offset
            if 0 <= new_index < len(self.nodes):
                surrounding_nodes.append(self.nodes[new_index])

        return surrounding_nodes

    def get_surrounding_node_piece(self, surrounding_nodes):
        pieces = []

        for node in surrounding_nodes:
            index = self.single_node_to_index(
                node)  # convert (x, y) to (row, col)

            if index:  # Ensure it's not None
                row, col = index
                piece = self.board[row][col]
                pieces.append((index, piece))
            else:
                print(f"Invalid node position: {node} -> outside board")

        return pieces

    def get_all_tiger_positions(self):

        tiger_positions = []

        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row][col] == 1:  # 1 = Tiger
                    # Convert grid coordinates to screen coordinates
                    pos_x = self.start_x + col * self.cell_size
                    pos_y = self.start_y + row * self.cell_size
                    tiger_positions.append((pos_x, pos_y))

        return tiger_positions

    def is_valid_tiger_move(self, start, end):
        # print('Start pos: ', start)
        start_idx = self.single_node_to_index(start)
        end_idx = self.single_node_to_index(end)

        if start_idx is None or end_idx is None:
            return False

        start_row, start_col = start_idx
        end_row, end_col = end_idx

        if self.board[start_row][start_col] != 1:
            return False
        if self.board[end_row][end_col] != 0:
            return False

        return True

    def get_piece_at_index(self, x, y):
        return self.board[x][y]

    def is_goat_at_node(self, pos_x, pos_y):
        row = (pos_y - self.start_y) // self.cell_size
        col = (pos_x - self.start_x) // self.cell_size
        return self.board[row][col] == 2

    def get_all_pieces(self, player_turn):

        piece_value = 2 if player_turn else 1
        positions = []

        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row, col] == piece_value:
                    positions.append((row, col))

        return positions

    def single_node_to_index(self, pos):
        # print(f'Receiving pos {pos}')
        pos_x, pos_y = pos
        row = (pos_y - self.start_y) // self.cell_size
        col = (pos_x - self.start_y) // self.cell_size

        if 0 <= row < 5 and 0 <= col < 5:
            return (row, col)

    def index_to_single_node(self, row, col):
        return self.nodes[row * 5 + col]  # for 5x5 board

    def clone(self):
        new_board = Board(skip_init=True)
        new_board.board = np.copy(self.board)
        new_board.goats = copy.deepcopy(self.goats)
        new_board.is_tigers_turn = self.is_tigers_turn
        new_board.eaten_goats = getattr(self, 'eaten_goats', 0)

        # Copy all essential visual/positioning attributes
        new_board.nodes = self.nodes
        new_board.cell_size = self.cell_size
        new_board.grid_size = self.grid_size
        new_board.start_x = self.start_x
        new_board.start_y = self.start_y
        new_board.tiger_image = self.tiger_image
        new_board.goat_image = self.goat_image
        return new_board


    def is_tiger_jump(self, src, dest):
        # This method assumes a valid jump is 2 steps away from src,
        # and there must be a goat in between
        middle = self.get_middle_position(src, dest)
        if middle is None:
            return False
        return self.get_piece_at(*middle) == 2  # 2 = Goat

    def get_middle_position(self, src, dest):
        src_x, src_y = src
        dest_x, dest_y = dest

        mid_x = (src_x + dest_x) // 2
        mid_y = (src_y + dest_y) // 2

        if (mid_x, mid_y) in self.nodes:
            return (mid_x, mid_y)
        return None
