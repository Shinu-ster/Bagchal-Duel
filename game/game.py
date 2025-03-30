import pygame
from .board import Board
from constants import constant
import sys

class Game:
    def __init__(self,screen):
        self.screen = screen
        self.board = Board()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill(constant.BG_COLOR)
            self.board.draw_board(self.screen)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    # screen = pygame.display.set_mode((constant.CELL_SIZE * 8, constant.CELL_SIZE * 8))
    # pygame.display.set_caption("Baghchal Duel")
   

    # board = Board()
    # running = True

    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False

    #     screen.fill(constant.BG_COLOR)
    #     board.draw_board(screen)
    #     pygame.display.flip()

    # pygame.quit()
