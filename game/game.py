import pygame
from .board import Board
from constants import constant
from .move import Move
import sys
# from ai.ai_engine import *
# from ai.ai_engine import get_best_ai_move
from ai.helpers import handle_ai_move
from utils.move_recorder import MoveRecorder
import os


def render_text_with_border(font, message, text_color, border_color, border_width=2):
    base = font.render(message, True, text_color)
    size = base.get_width() + border_width * 2, base.get_height() + border_width * 2
    border_surface = pygame.Surface(size, pygame.SRCALPHA)

    # Draw the border
    for dx in [-border_width, 0, border_width]:
        for dy in [-border_width, 0, border_width]:
            if dx != 0 or dy != 0:
                border_surface.blit(font.render(
                    message, True, border_color), (dx + border_width, dy + border_width))

    # Draw the main text
    border_surface.blit(base, (border_width, border_width))
    return border_surface


class Game:
    def __init__(self, screen, mode, player_side=None):
        self.screen = screen
        self.board = Board()
        self.running = True
        self.nodes = self.board.return_nodes()
        self.selected_piece = None
        self.move = Move(self.board)
        self.mode = mode

        self.player_side = player_side
        # self.turn = False if (
        #     self.mode == 'ai' and self.player_side == 'tiger') else True
        self.turn = True
        # (self.mode == 'ai' and self.player_side=='tiger')? self.turn = False : self.turn == True
        # self.turn = True
        self.handle_ai_move = handle_ai_move

        # Initialize move recorder
        self.move_recorder = MoveRecorder(clear_file=True)

        self.turn_font = pygame.font.Font(
            'assets/fonts/WinkyRough-Black.ttf', 40)
        self.end_game_font = pygame.font.Font(
            'assets/fonts/WinkyRough-Black.ttf', 60)
        self.end_game_font2 = pygame.font.Font(
            'assets/fonts/WinkyRough-Black.ttf', 40)
        game_font = pygame.font.Font(constant.FONT_PATH, 70)
        self.game_name = render_text_with_border(
            game_font, "Baghchal Duel", constant.WHITE, (26, 26, 25), border_width=3)
        self.game_name_rect = self.game_name.get_rect(center=(400, 100))

    def display_info(self):
        self.goat_info_rect = pygame.draw.rect(
            self.screen, (constant.BLACK), (100, 100), 2)

    def record_move(self, from_pos, to_pos):
        """Record a move for the review system"""
        self.move_recorder.record_move(from_pos, to_pos)

    def run(self):
        winner = None
        reviewed = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    threshold = 25
                    clicked_node = None
                    # print(f"Existing Nodes are : {self.nodes}")

                    min_dist = float('inf')
                    clicked_node = None

                    for node_x, node_y in self.nodes:
                        dist = ((node_x - mouse_x)**2 +
                                (node_y - mouse_y)**2)**0.5
                        if dist < threshold and dist < min_dist:
                            clicked_node = (node_x, node_y)
                            min_dist = dist

                    if clicked_node:
                        index = self.nodes.index(clicked_node)
                        # print(f"Index of clicked node: {index}")

                    if self.mode == "1v1":

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
                                                from_pixel = self.selected_piece if self.selected_piece in self.nodes else self.selected_piece
                                                self.record_move(
                                                    from_pixel, clicked_node)
                                                self.board.update_board(
                                                    ((sx, sy), (tx, ty)))
                                                self.move.eaten_goats += 1

                                                self.turn = not self.turn

                                                winner = self.move.check_game_over()
                                                if winner:

                                                    self.running = False
                                                self.selected_piece = None

                                if self.move.is_valid_move(self.selected_piece, (node_x, node_y), self.turn):
                                    print(
                                        '-----------Runningg is valid move--------')
                                    self.turn = not self.turn
                                    winner = self.move.check_game_over()
                                    if winner:
                                        self.running = False
                                    print("Turn Changed. Now it's goat's turn")

                                    from_pixel = self.selected_piece if self.selected_piece in self.nodes else self.selected_piece
                                    print(f'From pixel is {from_pixel}')
                                    self.record_move(from_pixel, clicked_node)
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
                                        if not self.board.is_goat_at_node(node_x, node_y):
                                            # Valid empty node to drop goat
                                            if self.move.drop_goat(clicked_node):
                                                self.record_move(
                                                    (0, 0), clicked_node)
                                                self.selected_piece = None
                                                self.turn = not self.turn
                                                winner = self.move.check_game_over()
                                                if winner:
                                                    self.running = False
                                    else:
                                        print(
                                            'Piece exists in the board click another node')
                                else:
                                    # Now we have to allow moving goats
                                    print('Reached Else')
                                    print(
                                        f'printing is goat at node {self.board.is_goat_at_node(node_x, node_y)}')
                                    print(
                                        f'Selected Piece for goat setted to {self.selected_piece}')
                                    if self.board.is_goat_at_node(node_x, node_y):
                                        self.selected_piece = (node_x, node_y)
                                        print(
                                            f'Selected Piece for goat is {self.selected_piece}')
                                    elif self.selected_piece:
                                        print(
                                            f'Selected piece is availablee for goat')
                                        # Try to move selected goat to this empty node
                                        # Is empty
                                        if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                            if self.move.is_valid_move(self.selected_piece, (node_x, node_y), self.turn):
                                                self.turn = not self.turn
                                                winner = self.move.check_game_over()
                                                if winner:
                                                    self.running = False
                                                from_pixel = self.selected_piece if self.selected_piece in self.nodes else self.selected_piece
                                                self.record_move(
                                                    from_pixel, clicked_node)
                                                self.selected_piece = None

                            else:
                                print("Not valid node")

                    else:
                        print('Side Ai')
                        print(f'Mode {self.mode}')
                        print(f'Player side is {self.player_side}')
                        print(f'Printing self.turn {self.turn}')

                        if  self.player_side == 'goat':  # Goat's turn
                            if self.turn == True:
                                # Player is goat
                                if clicked_node:
                                    node_x, node_y = clicked_node
                                    print(f'Player is goat')
                                    # print(
                                    #     f'goats remaining {self.move.goats_remaining}')
                                    if self.move.goats_remaining > 0:
                                        print('This is running for more than 20')
                                        if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                            if not self.board.is_goat_at_node(node_x, node_y):
                                                print(
                                                    f'Is goat at {self.board.is_goat_at_node(node_x, node_y)}')
                                                if self.move.drop_goat(clicked_node):
                                                    # print(f'Droppedgoat at {clicked_node}')
                                                    self.record_move(
                                                        (0, 0), clicked_node)
                                                    self.turn = not self.turn
                                                    self.selected_piece = None

                                                    # pygame.time.delay(1000)
                                                    # Trigger AI immediately if it's now AI's turn
                                                    if self.player_side != 'tiger':

                                                        # print('Sent board is ', self.board)
                                                        goats_remaining = self.move.goats_remaining
                                                        eaten_goats = self.move.eaten_goats

                                                        move, self.turn, updated_goats_remaining, updated_eaten_goats = self.handle_ai_move(
                                                            self.board, self.turn, goats_remaining, eaten_goats)
                                                        # The move has already been applied in-place to self.board
                                                        self.move = Move(
                                                            self.board)
                                                        self.move.goats_remaining = updated_goats_remaining
                                                        self.move.eaten_goats = updated_eaten_goats
                                                        # print(f'Returns board is {self.board}')
                                                        winner = self.move.check_game_over()
                                                        if winner:
                                                            self.running = False
                                    else:
                                        print('This is running for less than 20')
                                        if self.board.is_goat_at_node(node_x, node_y):
                                            self.selected_piece = (
                                                node_x, node_y)
                                        elif self.selected_piece:
                                            if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                                if self.move.is_valid_move(self.selected_piece, (node_x, node_y), self.turn):
                                                    self.turn = not self.turn
                                                    self.selected_piece = None
                                                    from_pixel = self.selected_piece if self.selected_piece in self.nodes else self.selected_piece
                                                    self.record_move(
                                                        from_pixel, clicked_node)

                                                    # Trigger AI if it's now AI's turn
                                                    if self.player_side != 'tiger':

                                                        print(
                                                            f'Passing turn {self.turn}')
                                                        goats_remaining = self.move.goats_remaining
                                                        eaten_goats = self.move.eaten_goats

                                                        move, self.turn, updated_goats_remaining, updated_eaten_goats = self.handle_ai_move(
                                                            self.board, self.turn, goats_remaining, eaten_goats)
                                                        # The move has already been applied in-place to self.board
                                                        self.move = Move(
                                                            self.board)
                                                        self.move.goats_remaining = updated_goats_remaining
                                                        self.move.eaten_goats = updated_eaten_goats
                                                        print(
                                                            f'Returns board is {self.board}')
                                                        winner = self.move.check_game_over()
                                                        if winner:
                                                            self.running = False

                        elif self.player_side == 'tiger':  # Tiger's turn

                            if self.turn == True: # Goat AIs turn
                                print("Goat AIs turn")
                                goats_remaining = self.move.goats_remaining
                                eaten_goats = self.move.eaten_goats
                                move, self.turn, updated_goats_remaining, updated_eaten_goats = self.handle_ai_move(
                                    self.board, self.turn, goats_remaining, eaten_goats)
                                print(f'Turn of Tiger is False {self.turn}')
                                self.move = Move(self.board)
                                self.move.goats_remaining = updated_goats_remaining
                                self.move.eaten_goats = updated_eaten_goats

                            if self.turn == False:
                                print('This is running')
                                print(f'Turn of Tiger is False {self.turn}')
                                print(f'Returns board is {self.board}')
                                winner = self.move.check_game_over()
                                if winner:
                                    self.running = False

                                if clicked_node:
                                    node_x, node_y = clicked_node
                                    print(f'Clicked Node {clicked_node}')

                                    if self.board.piece_exists_in_node(node_x, node_y, self.turn):
                                        self.selected_piece = (node_x, node_y)
                                        print(f'Gotten Selected Node {self.selected_piece}')
                                        print(f'self.turn {self.turn}')
                                    elif self.selected_piece:
                                        print(f'Selected Node {self.selected_piece}')
                                        sx, sy = self.board.single_node_to_index(
                                            self.selected_piece)
                                        tx, ty = self.board.single_node_to_index(
                                            (node_x, node_y))

                                        is_eat_move, goat_to_remove = self.move.is_valid_tiger_eat_move(
                                            (sx, sy), (tx, ty))
                                        if is_eat_move:
                                            self.move.eaten_goats += 1
                                            gx, gy = goat_to_remove
                                            print('Reached here')
                                            self.board.update_board(
                                                ((gx, gy), (gx, gy)))
                                            print('Reached here')
                                            self.board.update_board(
                                                ((sx, sy), (tx, ty)))
                                            self.record_move(
                                                (sx, sy), (tx, ty))
                                            print(
                                                f'Before Swtiching Turn of Tiger is False {self.turn}')
                                            self.turn = not self.turn
                                            print(
                                                f' After Switching Turn of Tiger is False {self.turn}')
                                            self.selected_piece = None

                                        elif self.move.is_valid_move(self.selected_piece, (node_x, node_y), self.turn):
                                            print('Calling update board')
                                            print('After Calling update board')
                                            self.record_move(
                                                (sx, sy), (tx, ty))
                                            print(
                                                f'Before Swtiching Turn of Tiger is False {self.turn}')
                                            self.turn = not self.turn
                                            print(
                                                f' After Switching Turn of Tiger is False {self.turn}')
                                            self.selected_piece = None

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                print('Resstarting Game')
                self.restart_game()

            self.screen.fill(constant.BG_COLOR)
            self.board.draw_board(self.screen, self.selected_piece)

            # 🟦 Draw Turn Indicator Box
            # 🟦 Draw Turn Indicator Box
            turn_box_rect = pygame.Rect(
                20, 20, 100, 120)  # (x, y, width, height)
            pygame.draw.rect(self.screen, (255, 255, 255),
                             turn_box_rect, border_radius=10)  # White background
            pygame.draw.rect(self.screen, (0, 0, 0), turn_box_rect,
                             2, border_radius=10)      # Border

            # 🏷️ Draw the "Turn" label
            turn_label = self.turn_font.render("Turn", True, (0, 0, 0))
            label_rect = turn_label.get_rect(
                center=(turn_box_rect.centerx, turn_box_rect.y + 25))
            self.screen.blit(turn_label, label_rect)

            # 🖼️ Load and scale icons only once
            if not hasattr(self, 'tiger_icon'):
                self.tiger_icon = pygame.image.load(
                    "assets/image/tigericon2.png")
                self.goat_icon = pygame.image.load(
                    "assets/image/goaticon3.png")
                self.tiger_icon = pygame.transform.scale(
                    self.tiger_icon, (64, 64))
                self.goat_icon = pygame.transform.scale(
                    self.goat_icon, (64, 64))

            # ⬇️ Display the icon slightly below the label
            icon = self.goat_icon if self.turn else self.tiger_icon
            icon_rect = icon.get_rect(
                center=(turn_box_rect.centerx, label_rect.bottom + 25))
            self.screen.blit(icon, icon_rect)

            # 🟦 Goats Remaining Box
            screen_width = self.screen.get_width()
            goat_box_rect = pygame.Rect(screen_width - 220, 25, 210, 80)

            pygame.draw.rect(self.screen, (255, 255, 255),
                             goat_box_rect, border_radius=10)  # White background
            pygame.draw.rect(self.screen, (0, 0, 0), goat_box_rect,
                             2, border_radius=10)      # Border

            # 🏷️ Label: "Goats"
            goats_label = self.turn_font.render("Remaining", True, (0, 0, 0))
            goats_label_rect = goats_label.get_rect(
                center=(goat_box_rect.centerx+10, goat_box_rect.y + 20))
            self.screen.blit(goats_label, goats_label_rect)

            # 🐐 Small Goat Icon (scaled smaller)
            small_goat_icon = pygame.transform.scale(self.goat_icon, (40, 40))
            icon_x = goat_box_rect.x + 20
            icon_y = goats_label_rect.bottom + 10
            self.screen.blit(small_goat_icon, (icon_x, icon_y - 23))

            # 🔢 Remaining Goat Count
            goat_count_text = self.turn_font.render(
                str(self.move.goats_remaining), True, (0, 0, 0))
            count_rect = goat_count_text.get_rect(
                midleft=(icon_x + 55, icon_y))
            self.screen.blit(goat_count_text, count_rect)
            # 🟦 Goats Eaten Box - Top Center
            screen_width = self.screen.get_width()
            eaten_box_width = 160
            eaten_box_height = 100
            eaten_box_rect = pygame.Rect(
                (screen_width - eaten_box_width) // 2, 20, eaten_box_width, eaten_box_height)

            pygame.draw.rect(self.screen, (255, 255, 255),
                             eaten_box_rect, border_radius=10)  # White background
            pygame.draw.rect(self.screen, (0, 0, 0), eaten_box_rect,
                             2, border_radius=10)      # Border

            # 🏷️ Label: "Eaten"
            eaten_label = self.turn_font.render("Eaten", True, (0, 0, 0))
            eaten_label_rect = eaten_label.get_rect(
                center=(eaten_box_rect.centerx, eaten_box_rect.y + 20))
            self.screen.blit(eaten_label, eaten_label_rect)

            # 🐐 Small Goat Icon (reuse scaled one from earlier)
            small_goat_icon = pygame.transform.scale(
                self.goat_icon, (40, 40))  # Only do this once
            icon_x = eaten_box_rect.x + 20
            icon_y = eaten_label_rect.bottom + 5
            self.screen.blit(small_goat_icon, (icon_x, icon_y - 5))

            # 🔢 Eaten Goat Count
            eaten_count_text = self.turn_font.render(
                str(self.move.eaten_goats), True, (0, 0, 0))
            eaten_count_rect = eaten_count_text.get_rect(
                midleft=(icon_x + 55, icon_y + 10))
            self.screen.blit(eaten_count_text, eaten_count_rect)

            # 🟦 Trapped Tigers Box - Below Eaten Box
            trapped_box_width = 270
            trapped_box_height = 100
            trapped_box_rect = pygame.Rect(
                (screen_width - trapped_box_width) -
                20, eaten_box_rect.bottom + 550,
                trapped_box_width, trapped_box_height
            )

            pygame.draw.rect(self.screen, (255, 255, 255),
                             trapped_box_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), trapped_box_rect,
                             2, border_radius=10)

            # 🏷️ Label: "Trapped Tigers"
            trapped_label = self.turn_font.render(
                "Trapped Tigers", True, (0, 0, 0))
            trapped_label_rect = trapped_label.get_rect(
                center=(trapped_box_rect.centerx, trapped_box_rect.y + 20))
            self.screen.blit(trapped_label, trapped_label_rect)

            # 🐯 Small Tiger Icon (scaled)
            small_tiger_icon = pygame.transform.scale(
                self.tiger_icon, (40, 40))
            tiger_icon_x = trapped_box_rect.x + 20
            tiger_icon_y = trapped_label_rect.bottom + 10
            self.screen.blit(small_tiger_icon,
                             (tiger_icon_x, tiger_icon_y - 10))

            # 🔢 Trapped Tiger Count
            trapped_count = self.move.get_trapped_tigers_count()
            trapped_count_text = self.turn_font.render(
                str(trapped_count), True, (0, 0, 0))
            trapped_count_rect = trapped_count_text.get_rect(
                midleft=(tiger_icon_x + 55, tiger_icon_y))
            self.screen.blit(trapped_count_text, trapped_count_rect)

            pygame.display.flip()

            if winner:
                pygame.time.wait(500)
                # Background color for winner
                self.screen.fill(constant.MAIN_MENU_BG)
                self.screen.blit(self.game_name, self.game_name_rect)

                # Show winner screen
                winner_text = self.end_game_font.render(
                    f'{winner} Wins!', True, constant.WHITE)
                winner_rect = winner_text.get_rect(center=(400, 350))
                self.screen.blit(winner_text, winner_rect)

                restart_text = self.end_game_font2.render(
                    'Press R to restart', True, constant.WHITE
                )
                restart_rect = restart_text.get_rect(center=(400, 500))
                self.screen.blit(restart_text, restart_rect)

                review_text = self.end_game_font2.render(
                    'Press V to review game', True, constant.WHITE
                )
                review_rect = review_text.get_rect(center=(400, 550))
                self.screen.blit(review_text, review_rect)

                main_menu_text = self.end_game_font2.render(
                    'Press Space to go to main menu', True, constant.WHITE
                )
                main_menu_rect = main_menu_text.get_rect(center=(400, 600))
                self.screen.blit(main_menu_text, main_menu_rect)

                pygame.display.flip()  # Make sure the final screen is shown

                # Wait for a moment to show the winner screen
                # pygame.time.wait(2000)

                # After game ends, handle review or delete
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            waiting_for_input = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.go_to_main_menu()
                                waiting_for_input = False
                            elif event.key == pygame.K_r:
                                new_game = Game(self.screen, self.mode)
                                new_game.run()
                                waiting_for_input = False
                            elif event.key == pygame.K_v and self.mode == "1v1":
                                from menu.review_menu import review_menu
                                review_menu(self.screen)
                                reviewed = True
                                waiting_for_input = False
                # Only delete file if user didn't review
                if not reviewed:
                    self.move_recorder.delete_file()
        pygame.quit()
        sys.exit()

    def go_to_main_menu(self):
        print("Going back to main menu")
        self.winner = None
        self.restart_game()
        self.show_main_menu()

    def show_main_menu(self):
        from menu.start_menu import main_menu, game_mode_menu, choose_side
        self.screen.fill((0, 0, 0))
        choice = main_menu(self.screen)

        if choice == "play":
            mode = game_mode_menu(self.screen)

            if mode == "1v1":
                print('Starging Game...')
                game = Game(self.screen, mode)
                game.run()

            if mode == "ai":
                side = choose_side(self.screen)
                game = Game(self.screen, mode="ai", player_side=side)
                game.run()

        elif choice == "rules":
            print("Displaying Rules...")

    def restart_game(self):
        print("Restarting the game")
        self.board.reset()
        self.turn = True
        self.winner = None
        print('Winner set to none')
        self.move.eaten_goats = 0
        self.move.goats_remaining = 20

        pygame.display.flip()

    def save_moves_pixel_format(self):
        # Save moves in the required pixel format for review
        # Only for 1v1 mode
        if self.mode != "1v1":
            return
        moves = self.move_recorder.moves
        lines = []
        for move in moves:
            from_pos = move["from_pos"] if move["from_pos"] else (0, 0)
            to_pos = move["to_pos"]
            lines.append(f"{from_pos} {to_pos}")
        filename = f"reviews/game_{self.move_recorder.game_id}_pixel.txt"
        with open(filename, "w") as f:
            for line in lines:
                f.write(line + "\n")
        # Here you can call your algorithm to analyze the moves and rewrite the file
        # For example:
        # analyze_moves(filename)
