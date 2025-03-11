import pygame
from constants import constant

class Board:
    def __init__(self):
        self.grid_size = constant.BOARD_SIZE
        self.board = self.create_board()
    
    def create_board(self):
        """Initialize the board with tigers and empty spaces."""
        board = [["." for _ in range(5)] for _ in range(5)]

        # Place 4 tigers at the corners
        board[0][0] = board[0][4] = board[4][0] = board[4][4] = "T"

        # All other spaces are empty initially (goats will be placed during gameplay)
        return board

    def draw_board(self, screen):
        """Draw the board grid and pieces on the screen."""
        screen.fill(constant.BG_COLOR)
        cell_size = constant.CELL_SIZE
        line_width = 2 # Thickness of the diagonal lines

        # Calculate top-left position to center the board
        offset_x = (screen.get_width() - 4 * cell_size) // 2
        offset_y = (screen.get_height() - 4 * cell_size) // 2

        # Draw grid
        for i in range(4):
            for j in range(4):
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
