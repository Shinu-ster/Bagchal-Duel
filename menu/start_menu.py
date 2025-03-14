import pygame
import sys
from game.board import Board  # Adjust import based on your structure
from constants import constant

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_PATH = "assets/fonts/BaghchalFont.ttf"
FONT = pygame.font.Font(constant.FONT_PATH, 50)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baghchal Duel")

def blur_surface(surface, amount=100):
    """Applies a blur effect to the given surface."""
    for _ in range(amount):
        surface = pygame.transform.smoothscale(surface, (surface.get_width()//2, surface.get_height()//2))
        surface = pygame.transform.smoothscale(surface, (surface.get_width(), surface.get_height()))
    return surface

def main_menu():
    board = Board()
    board_surface = pygame.Surface((WIDTH, HEIGHT))
    board_surface.fill(BLACK)  # Make sure it has a visible background

    board.draw_board(board_surface)  
    screen.blit(board_surface, (0, 0))  # Show board before blurring
    pygame.display.flip()

    blurred_board = blur_surface(board_surface.convert_alpha())  # Convert to compatible format

    while True:
        screen.blit(blurred_board, (0, 0))  
        title = FONT.render("Baghchal Duel", True, BLACK)
        play_text = FONT.render("Play", True, WHITE)
        rules_text = FONT.render("Rules", True, WHITE)
        quit_text = FONT.render("Quit", True, WHITE)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, 300))
        screen.blit(rules_text, (WIDTH//2 - rules_text.get_width()//2, 400))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= y <= 350:
                    return "play"
                if 400 <= y <= 450:
                    return "rules"
                if 500 <= y <= 550:
                    pygame.quit()
                    sys.exit()


def game_mode_menu():
    """Menu for choosing 1v1 or AI"""
    while True:
        screen.fill(BLACK)
        title = FONT.render("Choose Game Mode", True, WHITE)
        pvp_text = FONT.render("1v1", True, WHITE)
        ai_text = FONT.render("Play vs AI", True, WHITE)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(pvp_text, (WIDTH//2 - pvp_text.get_width()//2, 300))
        screen.blit(ai_text, (WIDTH//2 - ai_text.get_width()//2, 400))

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

def choose_side():
    """Menu for choosing Goat or Tiger"""
    while True:
        screen.fill(BLACK)
        title = FONT.render("Choose Your Side", True, WHITE)
        goat_text = FONT.render("Goat", True, WHITE)
        tiger_text = FONT.render("Tiger", True, WHITE)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(goat_text, (WIDTH//2 - goat_text.get_width()//2, 300))
        screen.blit(tiger_text, (WIDTH//2 - tiger_text.get_width()//2, 400))

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
