# main.py
from game.game import Game  # Import Game class from game.py
import pygame

pygame.init()

game = Game()
game.run()  # Assuming game.py has a Game class with a run method
