import pygame
from constants import constant
from game.move import Move
import numpy as np

class Board:
    def __init__(self):
        self.grid_size = constant.BOARD_SIZE
        self.cell_size = constant.CELL_SIZE
        self.board = self.create_board()
        self.start_x = 200 # position of first node x 
        self.start_y = 200 # position of first node y

        # Load images for tiger and goat
        self.tiger_image = pygame.image.load('assets/image/tiger-icon.png')
        self.goat_image = pygame.image.load('assets/image/goat-icon.png')

        # Scale the images to be smaller
        self.tiger_image = pygame.transform.scale(self.tiger_image, (constant.CELL_SIZE/2, constant.CELL_SIZE/2))
        self.goat_image = pygame.transform.scale(self.goat_image, (constant.CELL_SIZE, constant.CELL_SIZE))

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
            [1,0,0,0,1], # initialize tigers at spot 1
            [0,0,0,0,0],
            [0,0,2,0,0],
            [0,0,0,0,0],
            [1,0,0,0,1],
        ])

        # Place 4 tigers at the corners
        # board[0][0] = board[0][4] = board[4][0] = board[4][4] = "T"
        print('Board; ',board)

        # All other spaces are empty initially (goats will be placed during gameplay)
        return board

    def calculate_nodes(self):
        """Calculate the coordinates of the intersection nodes."""
        nodes = []
        cell_size = constant.CELL_SIZE

        # Calculate top-left position to center the board
        offset_x = (pygame.display.get_surface().get_width() - 5 * cell_size) // 2
        offset_y = (pygame.display.get_surface().get_height() - 5 * cell_size) // 2

        for i in range(5):  # 5 intersections in each direction
            for j in range(5):  # 5 intersections in each direction
                x = j * cell_size + offset_x + cell_size // 2
                y = i * cell_size + offset_y + cell_size // 2
                nodes.append((x, y))

        return nodes

    def draw_board(self, screen):
        """Draw the board grid and pieces on the screen."""
        screen.fill(constant.BG_COLOR)
        cell_size = constant.CELL_SIZE
        line_width = 2  # Thickness of the diagonal lines

        # Calculate top-left position to center the board
        offset_x = (screen.get_width() - constant.BOARD_ROW * cell_size) // 2
        offset_y = (screen.get_height() - constant.BOARD_COL * cell_size) // 2

        # Draw grid
        for i in range(constant.BOARD_ROW):  # Corrected to draw for a 5x5 grid
            for j in range(constant.BOARD_COL):  # Corrected to draw for a 5x5 grid
                x, y = j * cell_size + offset_x, i * cell_size + offset_y

                # Draw grid lines (rectangle borders)
                pygame.draw.rect(screen, constant.GRID_COLOR, (x, y, cell_size, cell_size), line_width)

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

        # Draw the pieces at the nodes (intersections)
        self.place_pieces_on_nodes(screen)

    def draw_nodes(self, screen):
        """Draw the nodes at intersections to show their positions."""
        node_color = (255, 0, 0)  # Red color for nodes (change this as needed)
        node_radius = 5  # Radius of the node circle
        node_pos = []

        for x, y in self.nodes:
            pygame.draw.circle(screen, node_color, (x, y), node_radius)
            node_pos.append((x,y))
        
        # print('Node Positions; ',node_pos)
        return node_pos

    def place_pieces_on_nodes(self, screen):
        """Place the tiger and goat pieces on their respective nodes."""
        cell_size = constant.CELL_SIZE
        for i, (x, y) in enumerate(self.nodes):
            row, col = i // 5, i % 5  # Get the row and column index from the node index

            # Draw the tiger icon at the corners (nodes)
            if self.board[row][col] == 1:
                # Center the tiger icon on the node position
                screen.blit(self.tiger_image, (x - self.tiger_image.get_width() // 2, y - self.tiger_image.get_height() // 2))

            # If you add goats later, you can place them like this
            elif self.board[row][col] == 2:
                # Center the goat icon on the node position
                screen.blit(self.goat_image, (x - self.goat_image.get_width() // 2, y - self.goat_image.get_height() // 2))

    def update_board(self, move):
        """Update board after a move (for both player and AI)."""
        from_pos, to_pos = move
        x1, y1 = from_pos
        x2, y2 = to_pos

        # Move piece
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = "."  # Clear old position

    def print_board(self):
        """Prints the board state in console (for debugging)."""
        for row in self.board:
            print(" ".join(row))
        print("\n")

    def return_nodes(self):
        return self.nodes
    
    def piece_exists_in_node(self,pos_x,pos_y,turn):
        row = (pos_y - self.start_y) // self.cell_size
        col = (pos_x - self.start_x) // self.cell_size

        if 0 <= row < 5 and 0 <= col < 5:
            print(f"Checking board[{row}][{col}]")

            if turn == False and self.board[row][col] == 1:
                print("Tiger Present at the node")
                return True
            elif turn == True and self.board[row][col] == 2:
                print("Goat present at the node")
                return True
                

            # if self.board[row][col] == 1:
            #     print('Tiger present')
            #     # if turn == False # Tigers turn
                    
            #     return True
            # elif self.board[row][col] == 2:
            #     print('Goat present')
            #     return False
           
        else:
            print("Clicked outside the board")
            return False
        
    def get_piece_at(self,pos_x,pos_y):
        row = (pos_y - self.start_y) // self.cell_size
        col = (pos_x - self.start_x) // self.cell_size
        if 0 <= row < 5 and 0 <= col < 5:
            return self.board[row][col]  # 1 = Tiger, 2 = Goat, 0 = Empty
        return None
        
        
