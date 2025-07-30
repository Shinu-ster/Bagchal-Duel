from menu.start_menu import main_menu, game_mode_menu, choose_side
from menu.review_menu import review_menu
from game.game import Game
from constants import constant
import sys
import pygame

# Initialize pygame
pygame.init()


# Game Constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont(constant.FONT_PATH, 70)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baghchal Duel")


def main():

    choice = main_menu(screen)


    # game = Game(screen)
    # game.run()


    if choice == "play":
        mode = game_mode_menu(screen)

        
        # side = choose_side(screen)
        if mode == '1v1':
            print('Starting Game..')
            game = Game(screen,mode)
            game.run()

        # if mode and side:
        #     print(f"Starting game: Mode={mode}, Side={side}")
        #     game = Game(screen)
        #     game.run()
        if mode == "ai":
            side = choose_side(screen)
            print('Side ',side)
            game = Game(screen,mode = "ai",player_side = side)
            game.run()

        # Call your game logic here based on mode and side

    elif choice == "rules":
        print("Displaying Rules...")
        # Implement your rules screen here
    elif choice == "review":
        print("Opening Review Menu...")
        review_result = review_menu(screen)
        if review_result == "back":
            main()  # Return to main menu


if __name__ == "__main__":
    main()
