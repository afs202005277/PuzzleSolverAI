from time import sleep

import pygame
import main

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 840

GAME_WIDTH_START = 80
GAME_HEIGHT_START = 80
GAME_WIDTH_SIZE = 450
GAME_HEIGHT_SIZE = 640
OFFSET = 10

BG_COLOR = (0, 51, 68)
GAME_BACKGROUND_COLOR = (20, 58, 75)


def pygame_init():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Block Escape")
    return screen


def is_colliding(piece, pos):
    return piece.collidepoint(pos[0], pos[1])


def draw_start_menu(screen):
    screen.fill(tuple(map(lambda x: x * 1.7, BG_COLOR)))
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    gl = pygame.image.load("./assets/logo.png").convert_alpha()
    game_logo = pygame.transform.scale(gl, (SCREEN_WIDTH * 0.8, SCREEN_WIDTH * 0.2792862684 * 0.8))
    screen.blit(game_logo, (SCREEN_WIDTH / 2 * 0.2, SCREEN_HEIGHT * 0.1))
    start_button = font.render('PRESS SPACE TO START', True, (255, 255, 255))
    screen.blit(start_button,
                (SCREEN_WIDTH / 2 - start_button.get_width() / 2, SCREEN_HEIGHT * 0.55 + start_button.get_height() / 2))
    quit_button = font.render('PRESS ESCAPE TO QUIT', True, (255, 255, 255))
    screen.blit(quit_button,
                (SCREEN_WIDTH / 2 - quit_button.get_width() / 2, SCREEN_HEIGHT * 0.70 + quit_button.get_height() / 2))
    pygame.display.update()


def draw_difficulties(screen):
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    title = font.render('CHOOSE AN OPTION', True, (255, 255, 255))
    easy = font.render('1: EASY', True, (255, 255, 255))
    medium = font.render('2: MEDIUM', True, (255, 255, 255))
    hard = font.render('3: HARD', True, (255, 255, 255))

    screen.blit(title,
                (SCREEN_WIDTH / 2 - title.get_width() / 2, SCREEN_HEIGHT * 0.15 + title.get_height() / 2))
    screen.blit(easy,
                (SCREEN_WIDTH / 2 - easy.get_width() / 2, SCREEN_HEIGHT * 0.25 + easy.get_height() / 2))
    screen.blit(medium,
                (SCREEN_WIDTH / 2 - medium.get_width() / 2, SCREEN_HEIGHT * 0.35 + medium.get_height() / 2))
    screen.blit(hard,
                (SCREEN_WIDTH / 2 - hard.get_width() / 2, SCREEN_HEIGHT * 0.45 + hard.get_height() / 2))

    pygame.display.update()


def draw_end_screen(screen, puzzle):
    screen.fill(BG_COLOR)
    hint_button(screen)
    pygame.draw.rect(screen, GAME_BACKGROUND_COLOR,
                     pygame.Rect(GAME_WIDTH_START, GAME_HEIGHT_START, GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE),
                     border_radius=5)
    puzzle.drawPieces(screen)

    end_screen = pygame.Surface((SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), pygame.SRCALPHA)
    end_screen.fill((0, 0, 0, 150))
    screen.blit(end_screen, (10, 10))
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    game_over_info = font.render('YOU WIN!', True, (255, 255, 255))
    screen.blit(game_over_info,
                (SCREEN_WIDTH / 2 - game_over_info.get_width() / 2,
                 50))
    score = font.render(f'MOVES MADE: {puzzle.getMoves()}', True, (255, 255, 255))
    screen.blit(score,
                (SCREEN_WIDTH / 2 - score.get_width() / 2,
                 100))
    main_menu_button = font.render('PRESS "M" TO RETURN TO THE MENU', True, (255, 255, 255))
    screen.blit(main_menu_button,
                (SCREEN_WIDTH / 2 - main_menu_button.get_width() / 2,
                 SCREEN_HEIGHT * 0.4 + main_menu_button.get_height() / 2))
    quit_button = font.render('PRESS ESCAPE TO QUIT', True, (255, 255, 255))
    screen.blit(quit_button,
                (SCREEN_WIDTH / 2 - quit_button.get_width() / 2,
                 SCREEN_HEIGHT * 0.70 + quit_button.get_height() / 2))
    pygame.display.flip()
    pygame.display.update()


def draw_moves(screen, moves):
    font = pygame.font.SysFont('poppins', 40)
    moves = font.render(F'MOVES: {moves}', True, (255, 255, 255))
    screen.blit(moves,
                (SCREEN_WIDTH / 2 - moves.get_width() / 2, 20))

def hint_button(screen):
    hint_image = pygame.image.load('assets/hint.png')
    image_position = (SCREEN_WIDTH / 2 - hint_image.get_width() / 2, 770)
    scaled_image = pygame.transform.scale(hint_image,
                                          (hint_image.get_width() / 9, hint_image.get_height() / 9))
    border_surface = pygame.Surface((scaled_image.get_width() + 10, scaled_image.get_height() + 10), pygame.SRCALPHA)

    border_rect = pygame.draw.rect(border_surface, (255, 255, 255, 128),
                                   (0, 0, scaled_image.get_width() + 10, scaled_image.get_height() + 10),
                                   border_radius=10)

    pygame.draw.circle(border_surface, (255, 255, 255, 128), (border_rect.left + 10, border_rect.top + 10), 10)
    pygame.draw.circle(border_surface, (255, 255, 255, 128), (border_rect.right - 10, border_rect.top + 10), 10)
    pygame.draw.circle(border_surface, (255, 255, 255, 128), (border_rect.left + 10, border_rect.bottom - 10), 10)
    pygame.draw.circle(border_surface, (255, 255, 255, 128), (border_rect.right - 10, border_rect.bottom - 10), 10)

    screen.blit(border_surface, (image_position[0] - 5, image_position[1] - 5))
    screen.blit(scaled_image, image_position)

    image_rect = pygame.Rect(image_position[0] - 5, image_position[1] - 5, scaled_image.get_width() + 10,
                             scaled_image.get_height() + 10)
    return image_rect


def main_loop():
    screen = pygame_init()
    last_col = None
    last_row = None
    moving_piece_index = None
    hint_rect = None
    puzzle = main.medium_map()
    game_state = 'main_menu'
    first_click  = True
    path = None

    # Game Loop (temporary)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if game_state == 'main_menu':
                draw_start_menu(screen)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    game_state = 'choose_diff'
                    game_over = False

            if game_state == 'choose_diff':
                draw_difficulties(screen)

                keys = pygame.key.get_pressed()
                # Change when more levels are implemented
                if keys[pygame.K_1]:
                    game_state = 'playing'
                    puzzle = main.easy_map()
                elif keys[pygame.K_2]:
                    puzzle = main.medium_map()
                    game_state = 'playing'
                elif keys[pygame.K_3]:
                    puzzle = main.hard_map()
                    game_state = 'playing'

            elif game_state == 'playing':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        start_pos = pygame.mouse.get_pos()
                        if hint_rect.collidepoint(start_pos):
                            if first_click:
                                sol = main.a_star_search(puzzle, main.gameOver, main.get_child_states, main.h4)
                                path = main.get_solution_path(sol[0])
                                main.movedPiece(path[0], path[1]).toggle_highlight()
                                first_click = False

                            else:
                                if main.gameOver(path[1]):
                                    puzzle.move_piece_delta(puzzle.objectivePiece.id, 0, 3)
                                    game_state = "end_screen"
                                else:
                                    puzzle = path[1]
                                path = None
                                first_click = True

                        last_col = puzzle.getColIndex(start_pos[0])
                        last_row = puzzle.getRowIndex(start_pos[1])
                        tmp = [idx for idx, piece in enumerate(pieces) if is_colliding(piece, start_pos)]
                        if len(tmp) == 1:
                            moving_piece_index = tmp[0]
                            puzzle.getPiece(moving_piece_index).toggle_highlight(True)
                            path = None
                            first_click = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        if moving_piece_index is None:
                            continue
                        end_pos = pygame.mouse.get_pos()

                        new_col = puzzle.getColIndex(end_pos[0])
                        new_row = puzzle.getRowIndex(end_pos[1])
                        puzzle.move_piece_delta(moving_piece_index, new_col - last_col, new_row - last_row)
                        puzzle.getPiece(moving_piece_index).toggle_highlight()
                        start_pos = None
                        if main.gameOver(puzzle):
                            puzzle.move_piece_delta(moving_piece_index, 0, 3)
                            game_state = "end_screen"
                        moving_piece_index = None

                if moving_piece_index is not None:
                    current_pos = pygame.mouse.get_pos()

                    new_col = puzzle.getColIndex(current_pos[0])
                    new_row = puzzle.getRowIndex(current_pos[1])
                    delta_col = new_col - last_col
                    delta_row = new_row - last_row
                    puzzle.move_piece_delta(moving_piece_index, delta_col, delta_row)
                    last_col += delta_col
                    last_row += delta_row

                screen.fill(BG_COLOR)
                pygame.draw.rect(screen, GAME_BACKGROUND_COLOR,
                                 pygame.Rect(GAME_WIDTH_START, GAME_HEIGHT_START, GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE),
                                 border_radius=5)
                pieces = puzzle.drawPieces(screen)
                draw_moves(screen, puzzle.getMoves())
                hint_rect = hint_button(screen)
                pygame.display.flip()
                pygame.display.update()
            elif game_state == 'end_screen':
                draw_end_screen(screen, puzzle)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_m]:
                    game_state = 'main_menu'
                    last_col = None
                    last_row = None
                    moving_piece_index = None
                    puzzle = main.easy_map()
                    game_over = False


def show_ai_path(path):
    screen = pygame_init()
    for step in path:
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, GAME_BACKGROUND_COLOR,
                         pygame.Rect(GAME_WIDTH_START, GAME_HEIGHT_START, GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE),
                         border_radius=5)
        step.drawPieces(screen)
        pygame.display.flip()
        pygame.display.update()
        sleep(2)


if __name__ == '__main__':
    main_loop()
