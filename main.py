from menu.start_menu import main_menu, game_mode_menu, choose_side
from game.game import Game
from constants import constant
import sys
import pygame

# Initialize pygame
pygame.init()


# Game Constants
WIDTH, HEIGHT = 800,800
WHITE = (255,255,255)
BLACK = (0,0,0)
FONT = pygame.font.Font(constant.FONT_PATH,50)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Baghchal Duel")







def main():

    game = Game(screen)
    game.run()

    # choice = main_menu(screen)
    
    # if choice == "play":
    #     mode = game_mode_menu(screen)
    #     side = choose_side(screen)
    #     if mode and side:
    #         print(f"Starting game: Mode={mode}, Side={side}")
    #         game = Game(screen)   
    #         game.run()

        
    #     # Call your game logic here based on mode and side
    
    # elif choice == "rules":
    #     print("Displaying Rules...")
    #     # Implement your rules screen here

if __name__ == "__main__":
    main()
