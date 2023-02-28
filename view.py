import pygame
import main

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

GAME_WIDTH_START = 80
GAME_HEIGHT_START = 40
GAME_WIDTH_SIZE = 450
GAME_HEIGHT_SIZE = 640
OFFSET = 10

BG_COLOR = (2, 2, 20)
GAME_PART_COLOR = (200, 200, 200)


def pygameInit():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Let the RED pass")
    return screen

def isColliding(piece, pos):
    return piece.collidepoint(pos[0], pos[1])


if __name__ == '__main__':
    screen = pygameInit()

    # Game Loop (temporary)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    pos = pygame.mouse.get_pos()
                    print([piece for piece in pieces if isColliding(piece, pos)])

        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, GAME_PART_COLOR, pygame.Rect(GAME_WIDTH_START, GAME_HEIGHT_START, GAME_WIDTH_SIZE, GAME_HEIGHT_SIZE), border_radius=5)

        puzzle = main.first_map()

        pieces = puzzle.drawPieces(screen)
        pygame.display.flip()
        pygame.display.update()

