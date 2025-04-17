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

                    threshold = 25
                    clicked_node = None
                    # print(f"Existing Nodes are : {self.nodes}")

                    for node_x, node_y in self.nodes:
                        if abs(node_x - mouse_x) < threshold and abs(node_y - mouse_y) < threshold:
                            clicked_node = (node_x, node_y)
                            index = self.nodes.index(clicked_node)
                            print(f"Index of elements are as follows {index}")
                            break  # Stop searching once we find the nearest node

                    if self.turn == False:  # Tigers turn
                        if clicked_node:
                            node_x, node_y = clicked_node
                            print('-----Tigers Turn-----')
                            print(f"Clocked on node: {clicked_node}")
                            print(
                                f"Surrounding nodes are as follows: {self.board.get_surrounding_nodes(clicked_node)}")
                            surrounding_node = self.board.get_surrounding_nodes(
                                clicked_node)
                            print(
                                f'Gettin piece of surroundin node: {surrounding_node}')

                            pieces = self.board.get_surrounding_node_piece(
                                surrounding_node)
                            print('Printing pieces in the node')

                            for (row, col), piece in pieces:
                                print(f'pieces at ({row},{col}):{piece}')

                        if self.selected_piece:
                            # 💡 If user clicks on another valid tiger, re-select it instead of moving
                            if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                print("Switched selection to another tiger")
                                self.selected_piece = (node_x, node_y)

                            else:
                                # result = self.move.is_valid_tiger_jump(self.selected_piece,(node_x,node_y))
                                t1, t2 = self.selected_piece
                                sx, sy = self.board.single_node_to_index(
                                    self.selected_piece)
                                print('----------Moving piece -----------')
                                surrounding_nodes = self.board.get_surrounding_nodes(
                                    self.selected_piece)
                                is_valid = False
                                for s_node in surrounding_nodes:
                                    s_x, s_y = s_node
                                    piece_val = self.board.get_piece_at(
                                        s_x, s_y)
                                    if piece_val == 1:
                                        print(
                                            f'🐐 Goat exists at pixel: ({s_x}, {s_y})')
                                    elif piece_val == 2:
                                        print(
                                            f'🐅 Tiger exists at pixel: ({s_x}, {s_y})')
                                        is_valid = self.move.is_valid_tiger_jump(
                                            (t1, t2), (s_x, s_y), (node_x, node_y))
                                        print(f'Tiger can jump {is_valid}')
                                    else:
                                        print(
                                            f'⭕ Empty at pixel: ({s_x}, {s_y})')

                                    if is_valid:
                                        tx, ty = self.board.single_node_to_index(
                                            (node_x, node_y))
                                        is_eat_move, goat_to_romove = self.move.is_valid_tiger_eat_move(
                                            (sx, sy), (tx, ty))

                                        if is_eat_move:
                                            # sx, sy = self.selected_piece
                                            gx, gy = goat_to_romove
                                            # tx, ty = node_x, node_y

                                            print(
                                                f'Tiger at {self.selected_piece} eats goat at ({gx},{gy} and jumps to ({tx},{ty}))')
                                            sx, sy = self.board.single_node_to_index(
                                                self.selected_piece)
                                            tx, ty = self.board.single_node_to_index(
                                                (node_x, node_y))

                                            # self.board[gx][gy] = 0
                                            # self.board[sx][sy] = 0
                                            # self.board[tx][ty] = 1

                                            self.board.update_board(
                                                ((gx, gy), (gx, gy)))

                                            self.board.update_board(
                                                ((sx, sy), (tx, ty)))

                                            self.turn = not self.turn
                                            self.selected_piece = None

                            if self.move.is_valid_move(self.selected_piece, (node_x, node_y), self.turn):
                                print('-----------Runningg is valid move--------')
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

                                if self.goats_remaining > 0:
                                    if clicked_node is None:
                                        break
                                    if self.move.drop_goat(clicked_node):
                                        self.selected_piece = None
                                        self.turn = not self.turn
                            else:
                                isempty = self.board.piece_exists_in_node(node_x,node_y,self.turn)
                                if isempty == False:
                                    self.selected_piece = (node_x,node_y)

                                if self.selected_piece:
                                    if self.board.piece_exists_in_node(node_x,node_y,self.turn):
                                        self.move.is_valid_move(self.selected_piece,(node_x,node_y),self.turn)
                                        self.turn = not self.turn
                                        


                        else:
                            print("Not valid node")

            self.screen.fill(constant.BG_COLOR)
            self.board.draw_board(self.screen, self.selected_piece)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
