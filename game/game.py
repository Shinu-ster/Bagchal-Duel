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
        self.move = Move(self.board)
        self.goats_remaining = self.move.goats_remaining
        self.turn = False
        self.turn_font = pygame.font.Font('assets/fonts/BaghchalFont.ttf', 50)
        # self.goats_remaining = 20

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
                    # print(f"Existing Nodes are : {self.nodes}")

                    for node_x, node_y in self.nodes:
                        if abs(node_x - mouse_x) < threshold and abs(node_y - mouse_y) < threshold:
                            clicked_node = (node_x, node_y)
                            index = self.nodes.index(clicked_node)
                            print(f"Index of elements are as follows {index}")
                            break  # Stop searching once we find the nearest node

                        # if clicked_node:

                    if self.turn == False:  # Tigers turn
                        if clicked_node:
                            node_x, node_y = clicked_node
                            print('-----Tigers Turn-----')
                            print(f"Clocked on node: {clicked_node}")
                            print(
                                f"Surrounding nodes are as follows: {self.board.get_surrounding_nodes(clicked_node)}")
                            surrounding_node = self.board.get_surrounding_nodes(clicked_node)
                            print(f'Gettin piece of surroundin node: {surrounding_node}')
                            pieces = self.board.get_surrounding_node_piece(surrounding_node)
                            for (row,col),piece in pieces:
                                print(f'pieces at ({row},{col}):{piece}')

                        if self.selected_piece:
                            # 💡 If user clicks on another valid tiger, re-select it instead of moving
                            if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                print("Switched selection to another tiger")
                                self.selected_piece = (node_x, node_y)

                            elif self.move.is_valid_move(self.selected_piece, (node_x, node_y), self.turn):
                                self.turn = not self.turn
                                print("Turn Changed. Now it's goat's turn")
                                self.selected_piece = None

                        else:
                            if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                self.selected_piece = (node_x, node_y)

                    elif self.turn == True:  # Goats Turn

                        if clicked_node:
                            node_x, node_y = clicked_node
                            print('-----Goats Turn-----')
                            print(f"Clocked on node: {clicked_node}")
                            print(
                                f"Surrounding nodes are as follows: {self.board.get_surrounding_nodes(clicked_node)}")

                        if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                            print("Piece Doesn't exist at that node")
                            if self.goats_remaining >= 0:
                                if self.move.drop_goat(clicked_node):
                                    self.selected_piece = None
                                    self.turn = not self.turn

                        else:
                            print("Piece exists at that node")


            self.screen.fill(constant.BG_COLOR)
            self.board.draw_board(self.screen,self.selected_piece)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
