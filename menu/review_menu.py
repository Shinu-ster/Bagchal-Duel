import pygame
import sys
from utils.move_recorder import MoveRecorder
from utils.game_analyzer import GameAnalyzer
from constants import constant
from game.board import Board
from game.move import Move


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
    FONT = pygame.font.Font(constant.FONT_PATH, 50)
    SMALL_FONT = pygame.font.Font(constant.FONT_PATH, 30)
    TINY_FONT = pygame.font.Font(constant.FONT_PATH, 20)

    recorder = MoveRecorder()
    move_file = recorder.filename
    analyzer = GameAnalyzer(move_file)
    analysis = analyzer.analyze_moves()
    moves = analyzer.moves

    if not moves:
        screen.fill(constant.MAIN_MENU_BG)
        no_moves_text = FONT.render("No moves to review", True, constant.WHITE)
        screen.blit(no_moves_text, (constant.WIDTH//2 - no_moves_text.get_width()//2, 400))
        back_text = SMALL_FONT.render("Press ESC to go back", True, constant.WHITE)
        screen.blit(back_text, (constant.WIDTH//2 - back_text.get_width()//2, 500))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
        return "back"

    current_move = -1  # Start before the first move (empty board)

    def replay_to(move_idx):
        board = Board()
        move_obj = Move(board)
        goats_remaining = 20
        eaten_goats = 0
        turn = True  # True = Goat, False = Tiger
        for i in range(min(move_idx + 1, len(moves))):
            line = moves[i]
            from_str, to_str = line.split(') (')
            from_str = from_str.replace('(', '')
            to_str = to_str.replace(')', '')
            from_pos = tuple(map(int, from_str.split(',')))
            to_pos = tuple(map(int, to_str.split(',')))
            if from_pos == (0, 0):
                move_obj.drop_goat(to_pos)
                goats_remaining -= 1
            else:
                from_idx = board.single_node_to_index(from_pos)
                to_idx = board.single_node_to_index(to_pos)
                if from_idx is not None and to_idx is not None:
                    if not turn and board.is_tiger_jump(from_pos, to_pos):
                        middle_pos = board.get_middle_position(from_pos, to_pos)
                        if middle_pos:
                            middle_idx = board.single_node_to_index(middle_pos)
                            if middle_idx:
                                board.board[middle_idx[0]][middle_idx[1]] = 0
                        eaten_goats += 1
                    move_obj.board.update_board((from_idx, to_idx))
            turn = not turn
        return board, goats_remaining, turn

    while True:
        screen.fill(constant.MAIN_MENU_BG)

        # Title
        title = render_text_with_border(
            FONT, "Game Review", constant.WHITE, (26, 26, 25), border_width=3)
        screen.blit(title, (constant.WIDTH//2 - title.get_width()//2, 30))

        # Instructions
        instructions = SMALL_FONT.render(
            "Use ← → to navigate moves. Press ESC to exit.", True, (200, 200, 200))
        screen.blit(instructions, (constant.WIDTH//2 - instructions.get_width()//2, 100))

        # Subtitle
        subtitle = SMALL_FONT.render(
            "Review your game moves and AI suggestions", True, constant.WHITE)
        screen.blit(subtitle, (constant.WIDTH//2 - subtitle.get_width()//2, 140))

        # Back button
        back_text = SMALL_FONT.render("Back to Menu", True, constant.WHITE)
        screen.blit(back_text, (50, 50))

        # Draw board for current move
        if current_move >= 0:
            board, goats_remaining, turn = replay_to(current_move)
            board.draw_board(screen)
        else:
            # Show empty board initially
            Board().draw_board(screen)

        # Display move info
        if moves and 0 <= current_move < len(moves):
            move = moves[current_move]
            analysis_item = analysis[current_move]
            quality = analysis_item.get('quality', 'unknown')
            best_move_str = analysis_item.get('best_move', 'None')
            blunder_reason = analysis_item.get('blunder_reason', None)

            # Quality colors
            if quality == "excellent":
                q_color = (0, 255, 0)
            elif quality == "good":
                q_color = (255, 255, 0)
            elif quality in ("bad", "blunder"):
                q_color = (255, 0, 0)
            else:
                q_color = (100, 255, 100)

            move_text = SMALL_FONT.render(f"Move {current_move + 1}/{len(moves)}: {move}", True, constant.WHITE)
            quality_text = SMALL_FONT.render(f"Quality: {quality}", True, q_color)
            best_move_text = TINY_FONT.render(f"Best: {best_move_str}", True, (0, 255, 255))

            screen.blit(move_text, (100, 60))
            screen.blit(quality_text, (100, 80))
            screen.blit(best_move_text, (100, 100))

            if blunder_reason:
                blunder_text = TINY_FONT.render(f"Reason: {blunder_reason}", True, (255, 100, 100))
                screen.blit(blunder_text, (100, 120))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_move > -1:
                    current_move -= 1
                elif event.key == pygame.K_RIGHT and current_move < len(moves) - 1:
                    current_move += 1
                elif event.key == pygame.K_ESCAPE:
                    return "back"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 50 <= x <= 250 and 50 <= y <= 80:
                    return "back"
