from view import *
from copy import deepcopy
import math

BLUE = [0, 0, 120]
RED = [120, 0, 0]
YELLOW = [120, 120, 0]
HIGHLIGHT = 70


class Piece:
    def __init__(self, height, width, row_idx, col_idx, color, isObjective=False):
        self.id = -1
        self.height = height
        self.width = width
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.color = color
        self.isObjective = isObjective
        self.isHighlighted = False


    def toggleHighlight(self):
        if self.isHighlighted:
            self.color = [c - HIGHLIGHT for c in self.color]
            self.isHighlighted = False
        else:
            self.color = [c + HIGHLIGHT for c in self.color]
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

        for idx, piece in enumerate(pieces):
            piece.id = idx

        for col in range(numCols):
            minPos = GAME_WIDTH_START + self.wSize * col
            self.pos_x_to_index[f'{minPos}'] = col
        self.pos_x_to_index[f'{GAME_WIDTH_START + GAME_WIDTH_SIZE}'] = numCols

        for row in range(numRows):
            minPos = GAME_HEIGHT_START + self.hSize * row
            self.pos_y_to_index[f'{minPos}'] = row
        self.pos_y_to_index[f'{GAME_HEIGHT_START + GAME_HEIGHT_SIZE}'] = numRows



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
        new_col_idx = (self.pieces[index]).col_idx + delta_col
        new_row_idx = (self.pieces[index]).row_idx + delta_row
        return self.move_piece(index, min(new_col_idx, self.numCols - self.pieces[index].width),
                               min(new_row_idx, self.numRows - self.pieces[index].height))

    def is_valid_move(self, index, newX, newY):
        if index < 0 or index >= len(self.pieces):
            print("Invalid Piece")
            return False
        elif newX >= self.numCols or newX < 0 or newY >= self.numRows or newY < 0:
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
        print(representation)

    def show_gui(self):
        print("TO BE DONE")

    def drawPieces(self, screen):
        pieces = []

        for piece in self.pieces:
            pygame.draw.rect(screen, GAME_PART_COLOR, pygame.Rect(GAME_WIDTH_START + self.wSize * piece.col_idx,
                                                                  GAME_HEIGHT_START + self.hSize * piece.row_idx,
                                                                  self.wSize * piece.width,
                                                                  self.hSize * piece.height), border_radius=5)
            pieceDraw = pygame.draw.rect(screen, piece.color,
                                         pygame.Rect(GAME_WIDTH_START + self.wSize * piece.col_idx + OFFSET,
                                                     GAME_HEIGHT_START + self.hSize * piece.row_idx + OFFSET,
                                                     self.wSize * piece.width - OFFSET * 2,
                                                     self.hSize * piece.height - OFFSET * 2), border_radius=5)
            pieces.append(pieceDraw)
        return pieces


def first_map():
    pieces = [Piece(2, 1, 0, 0, BLUE), Piece(2, 1, 0, 1, BLUE), Piece(2, 1, 0, 3, BLUE), Piece(2, 1, 2, 0, BLUE),
              Piece(2, 1, 2, 1, BLUE), Piece(2, 2, 2, 2, RED, True), Piece(1, 1, 4, 0, YELLOW),
              Piece(1, 1, 4, 1, YELLOW), Piece(1, 1, 4, 2, YELLOW), Piece(1, 1, 4, 3, YELLOW)]

    puzzle = Puzzle(5, 4, pieces)

    return puzzle


if __name__ == '__main__':
    first_map()
