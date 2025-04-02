import pygame
from .board import Board
from constants import constant
from .move import Move
import sys
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board()
        self.running = True
        self.nodes = self.board.return_nodes()
        self.selected_piece = None
        self.move_checker = Move(self.board)
        self.turn = False

        # self.is_piece_at = self.board.piece_exists_in_node()
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # print(f"Mouse clicked at {event.button} pressed at {event.pos}")
                    # print("Nodes at mouse click are: ", self.nodes)

                   

                    threshold = 25
                    clicked_node = None

                    for node_x, node_y in self.nodes:
                        if abs(node_x - mouse_x) < threshold and abs(node_y - mouse_y) < threshold:
                            clicked_node = (node_x, node_y)
                            break  # Stop searching once we find the nearest node

                        
                        # if clicked_node:
                          


                    if clicked_node:
                        node_x , node_y = clicked_node
                        print(f"Clicked on node: {clicked_node}")

                        if self.selected_piece:
                            print('Move Selected piece ', self.selected_piece , ' to node ', node_x, node_y)
                            if self.move_checker.is_valid_move(self.selected_piece,(node_x,node_y),self.turn):
                                self.turn = not self.turn
                                print("Turn Changed. Now its," "goats turn" if self.turn else "Tigers turn")
                                self.selected_piece = None

                        else:
                            if self.board.piece_exists_in_node(node_x,node_y,self.turn):
                                # Another mouse click pos 
                                self.selected_piece = (node_x,node_y)
                            

                        
                    else:
                        print("No valid node")

                # Check for mouse clicks
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     # Get the mouse position
                #     mouse_x, mouse_y = pygame.mouse.get_pos()
                #     # Call handle_click and pass the mouse position
                #     self.handle_click(mouse_x, mouse_y)

            self.screen.fill(constant.BG_COLOR)
            self.board.draw_board(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # def handle_click(self, mouse_x, mouse_y): 
    #     """Handle the logic for placing a goat or tiger based on the mouse click position."""
    #     # Calculate the grid coordinates based on the cell size (no offsets)
    #     node_x = mouse_x // constant.CELL_SIZE
    #     node_y = mouse_y // constant.CELL_SIZE

    #     # Check if the click is within the valid bounds of the board
    #     if 0 <= node_x < 5 and 0 <= node_y < 5:
    #         # Call the function to handle the move based on turn (Tiger's turn or Goat's turn)
    #         self.board.place_piece(node_x, node_y)

   