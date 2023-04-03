from time import sleep

import pygame
import analysis


'''
Initializes pygame and creates the game window.

Returns the game window surface.
'''
def pygame_init():
    pygame.init()
    screen = pygame.display.set_mode((analysis.SCREEN_WIDTH, analysis.SCREEN_HEIGHT))
    pygame.display.set_caption("Block Escape")
    return screen


'''
Determines whether a point is colliding with a given piece.

Arguments:
piece: The piece to check collision with.
pos: The position to check collision at.

Returns true if the point collides with the piece, False otherwise.
'''
def is_colliding(piece, pos):
    return piece.collidepoint(pos[0], pos[1])


'''
Draws the start menu on the game.

Arguments:
screen: The game screen to draw on.
'''
def draw_start_menu(screen):
    screen.fill(tuple(map(lambda x: x * 1.7, analysis.BG_COLOR)))
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    gl = pygame.image.load("./assets/logo.png").convert_alpha()
    game_logo = pygame.transform.scale(gl, (analysis.SCREEN_WIDTH * 0.8, analysis.SCREEN_WIDTH * 0.2792862684 * 0.8))
    screen.blit(game_logo, (analysis.SCREEN_WIDTH / 2 * 0.2, analysis.SCREEN_HEIGHT * 0.1))
    start_button = font.render('PRESS SPACE TO PLAY (HUMAN)', True, (255, 255, 255))
    screen.blit(start_button,
                (analysis.SCREEN_WIDTH / 2 - start_button.get_width() / 2, analysis.SCREEN_HEIGHT * 0.45 + start_button.get_height() / 2))
    start_button = font.render('PRESS C TO PLAY (COMPUTER)', True, (255, 255, 255))
    screen.blit(start_button,
                (analysis.SCREEN_WIDTH / 2 - start_button.get_width() / 2, analysis.SCREEN_HEIGHT * 0.60 + start_button.get_height() / 2))
    quit_button = font.render('PRESS ESCAPE TO QUIT', True, (255, 255, 255))
    screen.blit(quit_button,
                (analysis.SCREEN_WIDTH / 2 - quit_button.get_width() / 2, analysis.SCREEN_HEIGHT * 0.75 + quit_button.get_height() / 2))
    pygame.display.update()


'''
Draws the difficulties selection menu.

Arguments:
screen: The game screen to draw on.
'''
def draw_difficulties(screen):
    screen.fill(analysis.BG_COLOR)
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    title = font.render('CHOOSE AN OPTION', True, (255, 255, 255))
    easy = font.render('1: EASY', True, (255, 255, 255))
    medium = font.render('2: MEDIUM', True, (255, 255, 255))
    hard = font.render('3: HARD', True, (255, 255, 255))

    screen.blit(title,
                (analysis.SCREEN_WIDTH / 2 - title.get_width() / 2, analysis.SCREEN_HEIGHT * 0.15 + title.get_height() / 2))
    screen.blit(easy,
                (analysis.SCREEN_WIDTH / 2 - easy.get_width() / 2, analysis.SCREEN_HEIGHT * 0.25 + easy.get_height() / 2))
    screen.blit(medium,
                (analysis.SCREEN_WIDTH / 2 - medium.get_width() / 2, analysis.SCREEN_HEIGHT * 0.35 + medium.get_height() / 2))
    screen.blit(hard,
                (analysis.SCREEN_WIDTH / 2 - hard.get_width() / 2, analysis.SCREEN_HEIGHT * 0.45 + hard.get_height() / 2))

    pygame.display.update()


'''
Draws the algorithms selection menu.

Arguments:
screen: The game screen to draw on.
'''
def draw_algos(screen):
    screen.fill(analysis.BG_COLOR)
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    title = font.render('CHOOSE AN OPTION', True, (255, 255, 255))
    bfs = font.render('1: BFS', True, (255, 255, 255))
    dfs = font.render('2: DFS', True, (255, 255, 255))
    ids = font.render('3: IDS', True, (255, 255, 255))
    greedy = font.render('4: GREEDY', True, (255, 255, 255))
    a_star = font.render('5: A*', True, (255, 255, 255))
    w_a_star = font.render('6: WEIGHTED A*', True, (255, 255, 255))

    screen.blit(title,
                (analysis.SCREEN_WIDTH / 2 - title.get_width() / 2, analysis.SCREEN_HEIGHT * 0.15 + title.get_height() / 2))
    screen.blit(bfs,
                (analysis.SCREEN_WIDTH / 2 - bfs.get_width() / 2, analysis.SCREEN_HEIGHT * 0.25 + bfs.get_height() / 2))
    screen.blit(dfs,
                (analysis.SCREEN_WIDTH / 2 - dfs.get_width() / 2, analysis.SCREEN_HEIGHT * 0.35 + dfs.get_height() / 2))
    screen.blit(ids,
                (analysis.SCREEN_WIDTH / 2 - ids.get_width() / 2, analysis.SCREEN_HEIGHT * 0.45 + ids.get_height() / 2))
    screen.blit(greedy,
                (analysis.SCREEN_WIDTH / 2 - greedy.get_width() / 2, analysis.SCREEN_HEIGHT * 0.55 + greedy.get_height() / 2))
    screen.blit(a_star,
                (analysis.SCREEN_WIDTH / 2 - a_star.get_width() / 2, analysis.SCREEN_HEIGHT * 0.65 + a_star.get_height() / 2))
    screen.blit(w_a_star,
                (analysis.SCREEN_WIDTH / 2 - w_a_star.get_width() / 2, analysis.SCREEN_HEIGHT * 0.75 + w_a_star.get_height() / 2))
    pygame.display.update()


"""
Draw the heuristics menu.

Arguments:
screen: The game screen to draw on.
"""
def draw_heuristics(screen):
    screen.fill(analysis.BG_COLOR)
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    title = font.render('CHOOSE AN OPTION', True, (255, 255, 255))
    h1 = font.render('1: HEURISTIC 1', True, (255, 255, 255))
    h2 = font.render('2: HEURISTIC 2', True, (255, 255, 255))
    h3 = font.render('3: HEURISTIC 3', True, (255, 255, 255))
    h4 = font.render('4: HEURISTIC 4', True, (255, 255, 255))
    h5 = font.render('5: HEURISTIC 5', True, (255, 255, 255))
    h6 = font.render('6: HEURISTIC 6', True, (255, 255, 255))
    h7 = font.render('7: HEURISTIC 7', True, (255, 255, 255))
    h8 = font.render('8: HEURISTIC 8', True, (255, 255, 255))

    screen.blit(title,
                (analysis.SCREEN_WIDTH / 2 - title.get_width() / 2, analysis.SCREEN_HEIGHT * 0.05 + title.get_height() / 2))
    screen.blit(h1,
                (analysis.SCREEN_WIDTH / 2 - h1.get_width() / 2, analysis.SCREEN_HEIGHT * 0.15 + h1.get_height() / 2))
    screen.blit(h2,
                (analysis.SCREEN_WIDTH / 2 - h2.get_width() / 2, analysis.SCREEN_HEIGHT * 0.25 + h2.get_height() / 2))
    screen.blit(h3,
                (analysis.SCREEN_WIDTH / 2 - h3.get_width() / 2, analysis.SCREEN_HEIGHT * 0.35 + h3.get_height() / 2))
    screen.blit(h4,
                (analysis.SCREEN_WIDTH / 2 - h4.get_width() / 2, analysis.SCREEN_HEIGHT * 0.45 + h4.get_height() / 2))
    screen.blit(h5,
                (analysis.SCREEN_WIDTH / 2 - h5.get_width() / 2, analysis.SCREEN_HEIGHT * 0.55 + h5.get_height() / 2))
    screen.blit(h6,
                (analysis.SCREEN_WIDTH / 2 - h6.get_width() / 2, analysis.SCREEN_HEIGHT * 0.65 + h6.get_height() / 2))
    screen.blit(h7,
                (analysis.SCREEN_WIDTH / 2 - h7.get_width() / 2, analysis.SCREEN_HEIGHT * 0.75 + h7.get_height() / 2))
    screen.blit(h8,
                (analysis.SCREEN_WIDTH / 2 - h8.get_width() / 2, analysis.SCREEN_HEIGHT * 0.85 + h8.get_height() / 2))
    pygame.display.update()


"""
Draw the end game screen.

Arguments:
screen: The game screen to draw on.
puzzle: The instance of the Puzzle class representing the puzzle that was just completed.
"""
def draw_end_screen(screen, puzzle):
    screen.fill(analysis.BG_COLOR)
    hint_button(screen)
    pygame.draw.rect(screen, analysis.GAME_BACKGROUND_COLOR,
                     pygame.Rect(analysis.GAME_WIDTH_START, analysis.GAME_HEIGHT_START, analysis.GAME_WIDTH_SIZE, analysis.GAME_HEIGHT_SIZE),
                     border_radius=5)
    puzzle.drawPieces(screen)

    end_screen = pygame.Surface((analysis.SCREEN_WIDTH - 20, analysis.SCREEN_HEIGHT - 20), pygame.SRCALPHA)
    end_screen.fill((0, 0, 0, 150))
    screen.blit(end_screen, (10, 10))
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(True)
    game_over_info = font.render('YOU WIN!', True, (255, 255, 255))
    screen.blit(game_over_info,
                (analysis.SCREEN_WIDTH / 2 - game_over_info.get_width() / 2,
                 50))
    score = font.render(f'MOVES MADE: {puzzle.getMoves()}', True, (255, 255, 255))
    screen.blit(score,
                (analysis.SCREEN_WIDTH / 2 - score.get_width() / 2,
                 100))
    main_menu_button = font.render('PRESS "M" TO RETURN TO THE MENU', True, (255, 255, 255))
    screen.blit(main_menu_button,
                (analysis.SCREEN_WIDTH / 2 - main_menu_button.get_width() / 2,
                 analysis.SCREEN_HEIGHT * 0.4 + main_menu_button.get_height() / 2))
    quit_button = font.render('PRESS ESCAPE TO QUIT', True, (255, 255, 255))
    screen.blit(quit_button,
                (analysis.SCREEN_WIDTH / 2 - quit_button.get_width() / 2,
                 analysis.SCREEN_HEIGHT * 0.70 + quit_button.get_height() / 2))
    pygame.display.flip()
    pygame.display.update()


"""
Draw the number of moves made on the screen.

Arguments:
screen: The game screen to draw on.
moves: The number of moves made.
"""
def draw_moves(screen, moves):
    font = pygame.font.SysFont('poppins', 40)
    moves = font.render(F'MOVES: {moves}', True, (255, 255, 255))
    screen.blit(moves,
                (analysis.SCREEN_WIDTH / 2 - moves.get_width() / 2, 20))


"""
Draw the hint button on the screen.

Arguments:
screen: The game screen to draw on.
"""
def hint_button(screen):
    hint_image = pygame.image.load('assets/hint.png')
    image_position = (analysis.SCREEN_WIDTH / 2 - hint_image.get_width() / 2, 770)
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


"""
Displays the path to get to the solution.

Arguments:
path: States path to the solution.
"""
def show_ai_path(path):
    screen = pygame_init()
    moves = 0
    for step in path:
        screen.fill(analysis.BG_COLOR)
        pygame.draw.rect(screen, analysis.GAME_BACKGROUND_COLOR,
                         pygame.Rect(analysis.GAME_WIDTH_START, analysis.GAME_HEIGHT_START, analysis.GAME_WIDTH_SIZE, analysis.GAME_HEIGHT_SIZE),
                         border_radius=5)
        step.drawPieces(screen)
        draw_moves(screen, moves)
        pygame.display.flip()
        pygame.display.update()
        moves += 1
        sleep(1)

