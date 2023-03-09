from view import *
from copy import deepcopy
import math

"""BLUE = [0, 0, 120]
RED = [120, 0, 0]
YELLOW = [120, 120, 0]"""
HIGHLIGHT = 70
ANIMATION_TIME = 10

BLUE = "./assets/blue.png"
RED = "./assets/objective_cube.png"
YELLOW = "./assets/yellow.png"
GREEN = "./assets/green.png"

exit_image = pygame.image.load("./assets/exit.png")


class Piece:
    def __init__(self, height, width, row_idx, col_idx, texture, isObjective=False):
        self.id = -1
        self.height = height
        self.width = width
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.texture = texture
        self.color = (0, 0, 0, 0)
        self.isObjective = isObjective
        self.isHighlighted = False

    def toggleHighlight(self):
        if self.isHighlighted:
            self.color = (0, 0, 0, 0)
            self.isHighlighted = False
        else:
            self.color = (255, 255, 255, 255)
            self.isHighlighted = True

    def get_occupied_positions(self):
        pos = []
        for delta_row in range(self.row_idx, self.row_idx + self.height):
            for delta_col in range(self.col_idx, self.col_idx + self.width):
                pos.append((delta_col, delta_row))
        return pos

    def show_tui(self, representation):
        positions = self.get_occupied_positions()
        for (x, y) in positions:
            representation[y][x] = self.id

    def show_gui(self):
        print("TO BE DONE")


class Puzzle:
    def __init__(self, numRows, numCols, pieces=None, exit_x=1, exit_width=2):
        if pieces is None:
            pieces = []
        self.numRows = numRows
        self.numCols = numCols
        self.pieces = pieces
        self.exit_x = exit_x
        self.exit_y = numRows
        self.exit_width = exit_width
        self.wSize = GAME_WIDTH_SIZE / self.numCols
        self.hSize = GAME_HEIGHT_SIZE / self.numRows
        self.pos_x_to_index = {}
        self.pos_y_to_index = {}
        self.animation = 0
        self.movedPiece = None
        self.objectivePiece = None
        self.isGameOver = False
        self.moves = 0

        for idx, piece in enumerate(pieces):
            piece.id = idx
            if piece.isObjective:
                self.objectivePiece = piece

        for col in range(numCols):
            minPos = GAME_WIDTH_START + self.wSize * col
            self.pos_x_to_index[f'{minPos}'] = col
        self.pos_x_to_index[f'{GAME_WIDTH_START + GAME_WIDTH_SIZE}'] = numCols

        for row in range(numRows):
            minPos = GAME_HEIGHT_START + self.hSize * row
            self.pos_y_to_index[f'{minPos}'] = row
        self.pos_y_to_index[f'{GAME_HEIGHT_START + GAME_HEIGHT_SIZE}'] = numRows

    def getMoves(self):
        return self.moves

    def gameOver(self):
        heightRule = self.objectivePiece.row_idx == self.numRows - self.objectivePiece.height
        widthRule = self.objectivePiece.col_idx >= self.exit_x and self.objectivePiece.col_idx + self.objectivePiece.width <= self.exit_x + self.exit_width
        self.isGameOver = self.objectivePiece is not None and heightRule and widthRule
        return self.isGameOver

    def getColIndex(self, posX):
        for x in self.pos_x_to_index:
            if float(x) > posX:
                return self.pos_x_to_index[x] - 1
        return -1

    def getRowIndex(self, posY):
        for y in self.pos_y_to_index:
            if float(y) > posY:
                return self.pos_y_to_index[y] - 1
        return -1

    def get_objective_piece(self):
        for piece in self.pieces:
            if piece.isObjective:
                return piece

    def getPiece(self, index):
        return self.pieces[index]

    def add_piece(self, size, orientation, x, y):
        piece = Piece(size, orientation, x, y)
        self.pieces.append(piece)

    def move_piece(self, index, newX, newY):
        if self.is_valid_move(index, newX, newY):
            self.pieces[index].col_idx = newX
            self.pieces[index].row_idx = newY

    def move_piece_delta(self, index, delta_col, delta_row):
        new_col_idx = min((self.pieces[index]).col_idx + delta_col, self.numCols - self.pieces[index].width)
        new_row_idx = min((self.pieces[index]).row_idx + delta_row, self.numRows - self.pieces[index].height)

        if not self.isGameOver and not self.is_valid_move(index, new_col_idx, new_row_idx):
            return

        if self.isGameOver:
            new_row_idx = (self.pieces[index]).row_idx + delta_row

        if delta_col != 0 or delta_row != 0:
            self.animation = ANIMATION_TIME
            incrementX = (new_col_idx * self.wSize - self.pieces[index].col_idx * self.wSize) / ANIMATION_TIME
            incrementY = (new_row_idx * self.hSize - self.pieces[index].row_idx * self.hSize) / ANIMATION_TIME
            self.movedPiece = [index, self.pieces[index].col_idx * self.wSize, self.pieces[index].row_idx * self.hSize,
                               incrementX, incrementY]

        if not self.isGameOver and (
                self.pieces[index].col_idx != new_col_idx or self.pieces[index].row_idx != new_row_idx):
            self.moves += 1
        print(h1(self))
        self.pieces[index].col_idx = new_col_idx
        self.pieces[index].row_idx = new_row_idx

    def is_valid_move(self, index, newX, newY):
        if index < 0 or index >= len(self.pieces):
            print("Invalid Piece")
            return False
        elif newX + self.pieces[index].width > self.numCols or newX < 0 or newY + self.pieces[index].height > self.numRows or newY < 0:
            print("Out of bounds")
            return False
        else:
            tmp_piece = deepcopy(self.pieces[index])
            tmp_piece.col_idx = newX
            tmp_piece.row_idx = newY
            occupied_positions = tmp_piece.get_occupied_positions()
            for piece in self.pieces:
                if piece.id != tmp_piece.id and any(
                        map(lambda x: x in occupied_positions, piece.get_occupied_positions())):
                    print("Invalid position")
                    return False
            return True

    def show_tui(self):
        representation = [[[] for _ in range(self.numCols)] for _ in range(self.numRows + 1)]
        for piece in self.pieces:
            piece.show_tui(representation)
        for i in range(self.exit_x):
            representation[self.exit_y][i] = '-'
        for i in range(self.exit_x + self.exit_width, self.numCols):
            representation[self.exit_y][i] = '-'
        return representation

    def show_gui(self):
        print("TO BE DONE")

    def drawPieces(self, screen):
        pieces = []

        piece_objective = ""
        for piece in self.pieces:
            if piece.isObjective:
                piece_objective = piece
                break

        exit = pygame.draw.rect(screen, GAME_BACKGROUND_COLOR, pygame.Rect(GAME_WIDTH_START + self.wSize * self.exit_x,
                                                                           GAME_HEIGHT_START + self.hSize * self.exit_y,
                                                                           piece_objective.width * self.wSize,
                                                                           piece_objective.width * self.wSize * 0.438547486),
                                0)
        exit_image_prepared = pygame.transform.scale(exit_image, (
            piece_objective.width * self.wSize, piece_objective.width * self.wSize * 0.438547486))
        screen.blit(exit_image_prepared, exit)

        pygame.draw.rect(screen, (255, 255, 255, 255), pygame.Rect(0,
                                                                   GAME_HEIGHT_START + self.hSize * self.exit_y + piece_objective.width * self.wSize * 0.10355866,
                                                                   GAME_WIDTH_START + self.wSize * self.exit_x,
                                                                   piece_objective.width * self.wSize * 0.08379888), 0)

        pygame.draw.rect(screen, (255, 255, 255, 255),
                         pygame.Rect(GAME_WIDTH_START + self.wSize * self.exit_x + piece_objective.width * self.wSize,
                                     GAME_HEIGHT_START + self.hSize * self.exit_y + piece_objective.width * self.wSize * 0.10355866,
                                     GAME_WIDTH_SIZE - GAME_WIDTH_START + self.wSize * self.exit_x - piece_objective.width * self.wSize,
                                     piece_objective.width * self.wSize * 0.08379888), 0)

        for piece in self.pieces:
            pygame.draw.rect(screen, GAME_BACKGROUND_COLOR, pygame.Rect(GAME_WIDTH_START + self.wSize * piece.col_idx,
                                                                        GAME_HEIGHT_START + self.hSize * piece.row_idx,
                                                                        self.wSize * piece.width,
                                                                        self.hSize * piece.height), border_radius=5)
            texture_load = pygame.image.load(piece.texture)
            texture_tmp = pygame.transform.scale(texture_load, (
                self.wSize * piece.width - OFFSET * 2, self.hSize * piece.height - OFFSET * 2))
            if self.animation != 0 and piece.id == self.movedPiece[0]:
                tmpCol = self.movedPiece[1]
                tmpRow = self.movedPiece[2]

                pieceDraw = pygame.draw.rect(screen, piece.color,
                                             pygame.Rect(GAME_WIDTH_START + tmpCol + OFFSET,
                                                         GAME_HEIGHT_START + tmpRow + OFFSET,
                                                         self.wSize * piece.width - OFFSET * 2,
                                                         self.hSize * piece.height - OFFSET * 2), 0)

                screen.blit(texture_tmp, pieceDraw)
                self.movedPiece[1] += self.movedPiece[3]
                self.movedPiece[2] += self.movedPiece[4]
                self.animation -= 1

            else:
                pieceDraw = pygame.draw.rect(screen, piece.color,
                                             pygame.Rect(GAME_WIDTH_START + self.wSize * piece.col_idx + OFFSET,
                                                         GAME_HEIGHT_START + self.hSize * piece.row_idx + OFFSET,
                                                         self.wSize * piece.width - OFFSET * 2,
                                                         self.hSize * piece.height - OFFSET * 2), border_radius=5)
                screen.blit(texture_tmp, pieceDraw)
            pieces.append(pieceDraw)
        return pieces


def easy_map():
    pieces = [Piece(2, 1, 0, 0, BLUE), Piece(2, 1, 0, 1, BLUE), Piece(2, 1, 0, 3, BLUE), Piece(2, 1, 2, 0, BLUE),
              Piece(2, 1, 2, 1, BLUE), Piece(2, 2, 2, 2, RED, True), Piece(1, 1, 4, 0, YELLOW),
              Piece(1, 1, 4, 1, YELLOW), Piece(1, 1, 4, 2, YELLOW), Piece(1, 1, 4, 3, YELLOW)]

    puzzle = Puzzle(5, 4, pieces)

    return puzzle


def hard_map():
    pieces = [Piece(2, 1, 0, 0, BLUE), Piece(2, 2, 0, 1, RED, True), Piece(2, 1, 0, 3, BLUE), Piece(2, 1, 2, 0, BLUE),
              Piece(1, 1, 2, 1, YELLOW), Piece(1, 1, 3, 1, YELLOW), Piece(1, 1, 3, 2, YELLOW),
              Piece(1, 1, 2, 2, YELLOW), Piece(2, 1, 2, 3, BLUE), Piece(1, 2, 4, 1, GREEN)]

    puzzle = Puzzle(5, 4, pieces)

    return puzzle


def medium_map():
    pieces = [Piece(2, 1, 0, 0, BLUE), Piece(2, 1, 0, 1, BLUE), Piece(1, 1, 0, 3, YELLOW), Piece(1, 1, 0, 2, YELLOW),
              Piece(2, 2, 2, 0, RED, True), Piece(2, 1, 1, 2, BLUE), Piece(2, 1, 1, 3, BLUE),
              Piece(2, 1, 3, 2, BLUE), Piece(1, 1, 3, 3, YELLOW), Piece(1, 1, 4, 1, YELLOW)]

    puzzle = Puzzle(5, 4, pieces)

    return puzzle


if __name__ == '__main__':
    easy_map()


# distance red block to exit
def h1(puzzle):
    vector = (puzzle.get_objective_piece().col_idx - puzzle.exit_x,
              puzzle.get_objective_piece().row_idx - (puzzle.exit_x + puzzle.exit_width))
    return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])


def h3(puzzle):
    matrix = puzzle.show_tui()
    rows, cols = len(matrix), len(matrix[0])

    def dfs(row, col):
        if row < 0 or row >= rows-1 or col < 0 or col >= cols-1:
            return 0

        if matrix[row][col]:
            return 0

        size = 1 + dfs(row+1, col) + dfs(row, col+1)

        return size

    max = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            tmp = dfs(i, j)
            if max < tmp:
                max = tmp

    return max

def h2(puzzle):
    # weighted sum of the number of obstacles between the red block and the exit
    path = []

    weight = 0
    for piece in puzzle.pieces:
        if piece.isObjective:
            for i in range(piece.width):
                for j in range(puzzle.numRows - piece.row_idx):
                    path.append((piece.col_idx + i, piece.row_idx + j))
            break

    for piece in puzzle.pieces:
        if not piece.isObjective:
            if (piece.col_idx, piece.row_idx) in path:
                weight += (piece.width ** 2) * piece.height

    return weight


def h4(puzzle):
    return max(puzzle.get_objective_piece().col_idx,
               puzzle.numCols - puzzle.get_objective_piece().width - puzzle.get_objective_piece().col_idx) * 100


def h5(puzzle):
    index = 0
    for i, piece in enumerate(puzzle.pieces):
        if piece.isObjective:
            index = i
            break
    vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    weight = 0
    for (x, y) in vectors:
        if puzzle.is_valid_move(index, puzzle.pieces[index].col_idx + x, puzzle.pieces[index].row_idx + y):
            print(index, puzzle.pieces[index].col_idx + x, puzzle.pieces[index].row_idx + y)
            print((x, y))
            weight += 1
    return weight
