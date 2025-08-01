import pygame
import sys
from game.board import Board  # Adjust import based on your structure
from constants import constant

# # Initialize pygame
# pygame.init()

# # Constants
# WIDTH, HEIGHT = 800, 800
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # Initialize screen
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Baghchal Duel")


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


def blur_surface(surface, amount=100):
    """Applies a blur effect to the given surface."""
    for _ in range(amount):
        surface = pygame.transform.smoothscale(
            surface, (surface.get_width()//2, surface.get_height()//2))
        surface = pygame.transform.smoothscale(
            surface, (surface.get_width(), surface.get_height()))
    return surface


def main_menu(screen):
    FONT = pygame.font.Font(constant.FONT_PATH, 70)

    # board = Board()
    # board_surface = pygame.Surface((WIDTH, HEIGHT))
    # board_surface.fill(BLACK)  # Make sure it has a visible background

    # board.draw_board(board_surface)
    # screen.blit(board_surface, (0, 0))  # Show board before blurring
    # pygame.display.flip()

    # blurred_board = blur_surface(board_surface.convert_alpha())  # Convert to compatible format

    # Starts main menu
    while True:
        # screen.blit(blurred_board, (0, 0))
        # title = FONT.render("Baghchal Duel", True, constant.WHITE)
        screen.fill(constant.MAIN_MENU_BG)
        title = render_text_with_border(
            FONT, "Baghchal Duel", constant.WHITE, (26, 26, 25), border_width=3)
        play_text = FONT.render("Play", True, constant.WHITE)
        # rules_text = FONT.render("Rules", True, constant.WHITE)
        # review_text = FONT.render("Review Games", True, constant.WHITE)
        quit_text = FONT.render("Quit", True, constant.WHITE)

        screen.blit(title, (constant.WIDTH//2 - title.get_width()//2, 100))
        screen.blit(play_text, (constant.WIDTH//2 -
                    play_text.get_width()//2, 350))
        # screen.blit(rules_text, (constant.WIDTH//2 -
        #             rules_text.get_width()//2, 350))
        # screen.blit(review_text, (constant.WIDTH//2 -
        #             review_text.get_width()//2, 450))
        screen.blit(quit_text, (constant.WIDTH//2 -
                    quit_text.get_width()//2, 550))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 250 <= y <= 400:
                    return "play"
                if 350 <= y <= 400:
                    return "rules"
                if 550 <= y <= 600:
                    pygame.quit()
                    sys.exit()


def game_mode_menu(screen):
    """Menu for choosing 1v1 or AI"""
    FONT = pygame.font.Font(constant.FONT_PATH, 70)

    while True:
        screen.fill(constant.MAIN_MENU_BG)
        title = FONT.render("Choose Game Mode", True, constant.WHITE)
        pvp_text = FONT.render(" 1 vs 1", True, constant.WHITE)
        ai_text = FONT.render("Play vs AI", True, constant.WHITE)

        screen.blit(title, (constant.WIDTH//2 - title.get_width()//2, 100))
        screen.blit(pvp_text, (constant.WIDTH//2 -
                    pvp_text.get_width()//2, 300))
        screen.blit(ai_text, (constant.WIDTH//2 - ai_text.get_width()//2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= y <= 350:
                    return "1v1"
                if 400 <= y <= 450:
                    return "ai"


def choose_side(screen):
    """Menu for choosing Goat or Tiger"""
    FONT = pygame.font.Font(constant.FONT_PATH, 70)
    while True:
        screen.fill(constant.MAIN_MENU_BG)
        title = FONT.render("Choose Your Side", True, constant.WHITE)
        goat_text = FONT.render("Goat", True, constant.WHITE)
        tiger_text = FONT.render("Tiger", True, constant.WHITE)

        screen.blit(title, (constant.WIDTH//2 - title.get_width()//2, 100))
        screen.blit(goat_text, (constant.WIDTH//2 -
                    goat_text.get_width()//2, 300))
        screen.blit(tiger_text, (constant.WIDTH//2 -
                    tiger_text.get_width()//2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= y <= 350:
                    return "goat"
                if 400 <= y <= 450:
                    return "tiger"
