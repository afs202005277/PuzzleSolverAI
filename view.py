import pygame
import main

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

GAME_WIDTH_START = 80
GAME_HEIGHT_START = 40
GAME_WIDTH_SIZE = 450
GAME_HEIGHT_SIZE = 640
OFFSET = 10

BG_COLOR = (0, 51, 68)
GAME_BACKGROUND_COLOR = (20, 58, 75)


def pygameInit():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Let the RED pass")
    return screen

def isColliding(piece, pos):
    return piece.collidepoint(pos[0], pos[1])

def draw_start_menu(screen):
    screen.fill(tuple(map(lambda x: x*1.7, BG_COLOR)))
    font = pygame.font.SysFont('poppins', 40)
    font.set_bold(600)
    gl = pygame.image.load("./assets/logo.png").convert_alpha()
    game_logo = pygame.transform.scale(gl, (SCREEN_WIDTH*0.8, SCREEN_WIDTH*0.2792862684*0.8))
    screen.blit(game_logo, (SCREEN_WIDTH/2*0.2, SCREEN_HEIGHT*0.1))
    start_button = font.render('PRESS SPACE TO START', True, (255, 255, 255))
    screen.blit(start_button,
                (SCREEN_WIDTH/2 - start_button.get_width()/2, SCREEN_HEIGHT*0.55 + start_button.get_height()/2))
    quit_button = font.render('PRESS ESCAPE TO QUIT', True, (255, 255, 255))
    screen.blit(quit_button,
                (SCREEN_WIDTH / 2 - quit_button.get_width() / 2, SCREEN_HEIGHT*0.70 + quit_button.get_height() / 2))
    pygame.display.update()


if __name__ == '__main__':
    screen = pygameInit()
    lastCol = None
    lastRow = None
    moving_piece_index = None
    puzzle = main.first_map()
    game_state = 'main_menu'

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
                    game_state = 'playing' # mudar isto para 'choose_diff' quando feito
                    game_over = False

            if game_state == 'choose_diff': # parte do andre
                pass

            elif game_state == 'playing':
                print(main.h2(puzzle))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        start_pos = pygame.mouse.get_pos()
                        lastCol = puzzle.getColIndex(start_pos[0])
                        lastRow = puzzle.getRowIndex(start_pos[1])
                        tmp = [idx for idx, piece in enumerate(pieces) if isColliding(piece, start_pos)]
                        if len(tmp) == 1:
                            moving_piece_index = tmp[0]
                            puzzle.getPiece(moving_piece_index).toggleHighlight()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        if moving_piece_index is None:
                            continue
                        end_pos = pygame.mouse.get_pos()

                        newCol = puzzle.getColIndex(end_pos[0])
                        newRow = puzzle.getRowIndex(end_pos[1])
                        puzzle.move_piece_delta(moving_piece_index, newCol - lastCol, newRow - lastRow)
                        puzzle.getPiece(moving_piece_index).toggleHighlight()
                        #delta_col = (end_pos[0] - start_pos[0]) / puzzle.wSize
                        #delta_row = (end_pos[1] - start_pos[1]) / puzzle.hSize
                        #puzzle.move_piece_delta(moving_piece_index, delta_col, delta_row)
                        start_pos = None
                        moving_piece_index = None

                if moving_piece_index is not None:
                    current_pos = pygame.mouse.get_pos()

                    newCol = puzzle.getColIndex(current_pos[0])
                    newRow = puzzle.getRowIndex(current_pos[1])
                    deltaCol = newCol - lastCol
                    deltaRow = newRow - lastRow

                    puzzle.move_piece_delta(moving_piece_index, deltaCol, deltaRow)
                    lastCol += deltaCol
                    lastRow += deltaRow

                screen.fill(BG_COLOR)
                pygame.draw.rect(screen, GAME_BACKGROUND_COLOR, pygame.Rect(GAME_WIDTH_START, GAME_HEIGHT_START, GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE), border_radius=5)
                pieces = puzzle.drawPieces(screen)
                pygame.display.flip()
                pygame.display.update()

