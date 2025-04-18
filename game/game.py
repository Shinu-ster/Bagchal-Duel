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
        self.turn = False
        self.turn_font = pygame.font.Font('assets/fonts/WinkyRough-Black.ttf', 40)

    def display_info(self):
        self.goat_info_rect = pygame.draw.rect(self.screen,(constant.BLACK),(100,100),2)


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

                            print(f'clicking goat {node_x}{node_y}')
                            print(
                                f'Piece exists at board for goat {self.board.piece_exists_in_node(node_x, node_y, self.turn)} ')

                            if self.move.goats_remaining > 0:
                                    if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                        # Valid empty node to drop goat
                                        if self.move.drop_goat(clicked_node):
                                            self.selected_piece = None
                                            self.turn = not self.turn
                            else:
                                    # Now we have to allow moving goats
                                    print('Reached Else')
                                    print(f'printing is goat at node {self.board.is_goat_at_node(node_x,node_y)}')
                                    print(f'Selected Piece for goat setted to {self.selected_piece}')
                                    if self.board.is_goat_at_node(node_x, node_y):
                                        self.selected_piece = (node_x, node_y)
                                        print(f'Selected Piece for goat is {self.selected_piece}') 
                                    elif self.selected_piece:
                                        print(f'Selected piece is availablee for goat')
                                        # Try to move selected goat to this empty node
                                        if self.board.piece_exists_in_node(node_x, node_y, self.turn):  # Is empty
                                            if self.move.is_valid_move(self.selected_piece, (node_x, node_y), self.turn):
                                                self.turn = not self.turn
                                                self.selected_piece = None


                        else:
                            print("Not valid node")

            self.screen.fill(constant.BG_COLOR)
            self.board.draw_board(self.screen, self.selected_piece)

            # 🟦 Draw Turn Indicator Box
            # 🟦 Draw Turn Indicator Box
            turn_box_rect = pygame.Rect(20, 20, 100, 120)  # (x, y, width, height)
            pygame.draw.rect(self.screen, (255, 255, 255), turn_box_rect, border_radius=10)  # White background
            pygame.draw.rect(self.screen, (0, 0, 0), turn_box_rect, 2, border_radius=10)      # Border

            # 🏷️ Draw the "Turn" label
            turn_label = self.turn_font.render("Turn", True, (0, 0, 0))
            label_rect = turn_label.get_rect(center=(turn_box_rect.centerx, turn_box_rect.y + 25))
            self.screen.blit(turn_label, label_rect)

            # 🖼️ Load and scale icons only once
            if not hasattr(self, 'tiger_icon'):
                self.tiger_icon = pygame.image.load("assets/image/tiger-icon.png")
                self.goat_icon = pygame.image.load("assets/image/goat-icon.png")
                self.tiger_icon = pygame.transform.scale(self.tiger_icon, (64, 64))
                self.goat_icon = pygame.transform.scale(self.goat_icon, (64, 64))

            # ⬇️ Display the icon slightly below the label
            icon = self.goat_icon if self.turn else self.tiger_icon
            icon_rect = icon.get_rect(center=(turn_box_rect.centerx, label_rect.bottom + 25))
            self.screen.blit(icon, icon_rect)


                        # 🟦 Goats Remaining Box
            screen_width = self.screen.get_width()
            goat_box_rect = pygame.Rect(screen_width - 180, 20, 160, 80)  # Right side

            pygame.draw.rect(self.screen, (255, 255, 255), goat_box_rect, border_radius=10)  # White background
            pygame.draw.rect(self.screen, (0, 0, 0), goat_box_rect, 2, border_radius=10)      # Border

            # 🏷️ Label: "Goats"
            goats_label = self.turn_font.render("Goats", True, (0, 0, 0))
            goats_label_rect = goats_label.get_rect(center=(goat_box_rect.centerx, goat_box_rect.y + 20))
            self.screen.blit(goats_label, goats_label_rect)

            # 🐐 Small Goat Icon (scaled smaller)
            small_goat_icon = pygame.transform.scale(self.goat_icon, (40, 40))
            icon_x = goat_box_rect.x + 20
            icon_y = goats_label_rect.bottom + 10
            self.screen.blit(small_goat_icon, (icon_x, icon_y - 23))

            # 🔢 Remaining Goat Count
            goat_count_text = self.turn_font.render(str(self.move.goats_remaining), True, (0, 0, 0))
            count_rect = goat_count_text.get_rect(midleft=(icon_x + 55, icon_y))
            self.screen.blit(goat_count_text, count_rect)



            pygame.display.flip()

        pygame.quit()
        sys.exit()
