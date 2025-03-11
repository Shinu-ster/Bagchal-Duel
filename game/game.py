import pygame
from .board import Board
from constants import constant

class Game:

    pygame.init()
    screen = pygame.display.set_mode((constant.CELL_SIZE * 5, constant.CELL_SIZE * 5))
    pygame.display.set_caption("Baghchal Duel")

    board = Board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(constant.BG_COLOR)
        board.draw_board(screen)
        pygame.display.flip()

    pygame.quit()
