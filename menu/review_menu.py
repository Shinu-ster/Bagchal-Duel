import pygame
import sys
from utils.move_recorder import MoveRecorder
from utils.game_analyzer import GameAnalyzer
from constants import constant
from game.board import Board


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


def review_menu(screen):
    """Main review menu showing available games to analyze"""
    FONT = pygame.font.Font(constant.FONT_PATH, 50)
    SMALL_FONT = pygame.font.Font(constant.FONT_PATH, 30)
    # Get the latest move file
    recorder = MoveRecorder()
    move_file = recorder.filename
    analyzer = GameAnalyzer(move_file)
    analysis = analyzer.analyze_moves()
    moves = analyzer.moves
    current_move = 0
    board = Board()
    # For replay, we need to reset and apply moves up to current_move

    def replay_to(move_idx):
        board.reset()
        for i in range(move_idx + 1):
            line = moves[i]
            from_str, to_str = line.split(') (')
            from_str = from_str.replace('(', '')
            to_str = to_str.replace(')', '')
            from_pos = tuple(map(int, from_str.split(',')))
            to_pos = tuple(map(int, to_str.split(',')))
            if from_pos == (0, 0):
                board.update_goat(to_pos)
            else:
                board.update_board((from_pos, to_pos))
    while True:
        screen.fill(constant.MAIN_MENU_BG)
        # Title
        title = render_text_with_border(
            FONT, "Game Review", constant.WHITE, (26, 26, 25), border_width=3)
        screen.blit(title, (constant.WIDTH//2 - title.get_width()//2, 50))
        # Back button
        back_text = SMALL_FONT.render("Back to Menu", True, constant.WHITE)
        screen.blit(back_text, (50, 50))
        # Draw board state for current move
        replay_to(current_move)
        board.draw_board(screen)
        # Move info
        if analysis:
            move = moves[current_move]
            quality = analysis[current_move]['quality']
            move_text = SMALL_FONT.render(
                f"Move: {move}", True, constant.WHITE)
            quality_text = SMALL_FONT.render(f"Quality: {quality}", True, (0, 255, 0) if quality == "brilliant" else (
                255, 0, 0) if quality == "blunder" else (255, 255, 0) if quality == "bad" else (100, 255, 100))
            screen.blit(move_text, (100, 700))
            screen.blit(quality_text, (100, 740))
        # Navigation
        nav_text = SMALL_FONT.render(
            "Use ← → to navigate moves, ESC to go back", True, (150, 150, 150))
        screen.blit(nav_text, (constant.WIDTH//2 -
                    nav_text.get_width()//2, 800))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_move > 0:
                    current_move -= 1
                elif event.key == pygame.K_RIGHT and current_move < len(moves) - 1:
                    current_move += 1
                elif event.key == pygame.K_ESCAPE:
                    return "back"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 50 <= x <= 250 and 50 <= y <= 80:
                    return "back"
