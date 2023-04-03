import pygame
from copy import deepcopy

HIGHLIGHT = 70
ANIMATION_TIME = 10

BLUE = "./assets/blue.png"
BLUE_H = "./assets/blue_h.png"
RED = "./assets/objective_cube.png"
RED_H = "./assets/objective_cube_h.png"
YELLOW = "./assets/yellow.png"
YELLOW_H = "./assets/yellow_h.png"
GREEN = "./assets/green.png"
GREEN_H = "./assets/green_h.png"

exit_image = pygame.image.load("./assets/exit.png")

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 840

GAME_WIDTH_START = 80
GAME_HEIGHT_START = 80
GAME_WIDTH_SIZE = 450
GAME_HEIGHT_SIZE = 640
OFFSET = 10

BG_COLOR = (0, 51, 68)
GAME_BACKGROUND_COLOR = (20, 58, 75)

"""
The Piece class represents a puzzle piece and stores information about its dimensions, position, 
texture, and whether or not it is the objective piece.
"""


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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            statement = self.row_idx == other.row_idx and self.col_idx == other.col_idx \
                        and self.width == other.width and self.height == other.height
            return statement
        return False

    def __hash__(self):
        return hash((self.row_idx, self.col_idx, self.width, self.height))

    # Toggles the highlight state of a grid cell. The force parameter forces the cell to highlight
    # even if it was already
    def toggle_highlight(self, force=False):
        if force:
            if self.texture == BLUE:
                self.texture = BLUE_H
            elif self.texture == YELLOW:
                self.texture = YELLOW_H
            elif self.texture == RED:
                self.texture = RED_H
            elif self.texture == GREEN:
                self.texture = GREEN_H

        elif self.isHighlighted:

            if self.texture == BLUE_H:
                self.texture = BLUE
            elif self.texture == YELLOW_H:
                self.texture = YELLOW
            elif self.texture == RED_H:
                self.texture = RED
            elif self.texture == GREEN_H:
                self.texture = GREEN

            self.isHighlighted = False
        else:

            if self.texture == BLUE:
                self.texture = BLUE_H
            elif self.texture == YELLOW:
                self.texture = YELLOW_H
            elif self.texture == RED:
                self.texture = RED_H
            elif self.texture == GREEN:
                self.texture = GREEN_H

            self.isHighlighted = True

    # Returns a list of all the positions occupied by the grid cell.
    def get_occupied_positions(self):
        pos = []
        for delta_row in range(self.row_idx, self.row_idx + self.height):
            for delta_col in range(self.col_idx, self.col_idx + self.width):
                pos.append((delta_col, delta_row))
        return pos

    # Updates a text-based representation of the grid cell in a terminal user interface
    def show_tui(self, representation):
        positions = self.get_occupied_positions()
        for (x, y) in positions:
            representation[y][x] = self.id


"""
The Puzzle class represents the game board and manages the state of the game. 
It contains a list of Piece objects and methods to move them around the board, check if a move is valid, 
and check if the game is over.
"""


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
            min_pos = GAME_WIDTH_START + self.wSize * col
            self.pos_x_to_index[f'{min_pos}'] = col
        self.pos_x_to_index[f'{GAME_WIDTH_START + GAME_WIDTH_SIZE}'] = numCols

        for row in range(numRows):
            min_pos = GAME_HEIGHT_START + self.hSize * row
            self.pos_y_to_index[f'{min_pos}'] = row
        self.pos_y_to_index[f'{GAME_HEIGHT_START + GAME_HEIGHT_SIZE}'] = numRows

    def __eq__(self, other):
        if isinstance(other, self.__class__) and len(self.pieces) == len(other.pieces):
            for i in range(len(self.pieces)):
                if self.pieces[i] != other.pieces[i]:
                    return False
            return True
        return False

    def __hash__(self):
        return hash(self.pieces.__hash__)

    # Returns the number of moves made so far.
    def getMoves(self):
        return self.moves

    # Given a horizontal position posX, returns the index of the column it belongs to.
    def getColIndex(self, posX):
        for x in self.pos_x_to_index:
            if float(x) > posX:
                return self.pos_x_to_index[x] - 1
        return -1

    # Given a vertical position posY, returns the index of the row it belongs to.
    def getRowIndex(self, posY):
        for y in self.pos_y_to_index:
            if float(y) > posY:
                return self.pos_y_to_index[y] - 1
        return -1

    # Returns the objective piece of the puzzle.
    def get_objective_piece(self):
        for piece in self.pieces:
            if piece.isObjective:
                return piece

    # Returns the piece at the given index.
    def getPiece(self, index):
        return self.pieces[index]

    # Tries to move the piece at the given index to the given position.
    def move_piece(self, index, newX, newY):
        if self.is_valid_move(index, newX, newY):
            self.pieces[index].col_idx = newX
            self.pieces[index].row_idx = newY

    # Tries to move the piece at the given index by the given deltas in the column and row directions.
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

        self.pieces[index].col_idx = new_col_idx
        self.pieces[index].row_idx = new_row_idx

    # Checks whether moving the piece at the given index to the given position is valid.
    def is_valid_move(self, index, newX, newY):
        if index < 0 or index >= len(self.pieces):
            return False
        elif newX + self.pieces[index].width > self.numCols or newX < 0 or newY + self.pieces[
            index].height > self.numRows or newY < 0:
            return False
        else:
            tmp_piece = deepcopy(self.pieces[index])
            tmp_piece.col_idx = newX
            tmp_piece.row_idx = newY
            occupied_positions = tmp_piece.get_occupied_positions()
            for piece in self.pieces:
                if piece.id != tmp_piece.id and any(
                        map(lambda x: x in occupied_positions, piece.get_occupied_positions())):
                    return False
            return True

    # Generates a text-based representation of the current state of the puzzle.
    def show_tui(self):
        representation = [[[] for _ in range(self.numCols)] for _ in range(self.numRows + 1)]
        for piece in self.pieces:
            piece.show_tui(representation)
        for i in range(self.exit_x):
            representation[self.exit_y][i] = '-'
        for i in range(self.exit_x + self.exit_width, self.numCols):
            representation[self.exit_y][i] = '-'
        return representation

    # Draws the current state of the puzzle on the given screen.
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


# Creates the easy map
def easy_map():
    pieces = [Piece(2, 1, 0, 0, BLUE), Piece(2, 1, 0, 1, BLUE), Piece(2, 1, 0, 3, BLUE), Piece(2, 1, 2, 0, BLUE),
              Piece(2, 1, 2, 1, BLUE), Piece(2, 2, 2, 2, RED, True), Piece(1, 1, 4, 0, YELLOW),
              Piece(1, 1, 4, 1, YELLOW), Piece(1, 1, 4, 2, YELLOW), Piece(1, 1, 4, 3, YELLOW)]

    puzzle = Puzzle(5, 4, pieces)

    return puzzle


# Creates the medium map
def medium_map():
    pieces = [Piece(2, 1, 0, 0, BLUE), Piece(2, 1, 0, 1, BLUE), Piece(1, 1, 0, 3, YELLOW), Piece(1, 1, 0, 2, YELLOW),
              Piece(2, 2, 2, 0, RED, True), Piece(2, 1, 1, 2, BLUE), Piece(2, 1, 1, 3, BLUE),
              Piece(2, 1, 3, 2, BLUE), Piece(1, 1, 3, 3, YELLOW), Piece(1, 1, 4, 1, YELLOW)]

    puzzle = Puzzle(5, 4, pieces)

    return puzzle


# Creates the hard map
def hard_map():
    pieces = [Piece(1, 2, 0, 0, GREEN), Piece(1, 1, 0, 2, YELLOW), Piece(2, 1, 0, 3, BLUE),
              Piece(1, 1, 1, 0, YELLOW), Piece(2, 2, 1, 1, RED, True), Piece(2, 1, 2, 3, BLUE),
              Piece(2, 1, 3, 0, BLUE), Piece(1, 1, 3, 1, YELLOW), Piece(2, 1, 3, 2, BLUE), Piece(1, 1, 2, 0, YELLOW)]

    puzzle = Puzzle(5, 4, pieces)

    return puzzle


# Move a piece
def movedPiece(puzzle1, puzzle2):
    for i in range(len(puzzle1.pieces)):
        if puzzle1.pieces[i] != puzzle2.pieces[i]:
            return puzzle1.pieces[i]
    return None


# Move a piece (Computer)
def move_piece_ai(puzzle, index, newX, newY):
    if puzzle.is_valid_move(index, newX, newY):
        res = deepcopy(puzzle)
        res.pieces[index].col_idx = newX
        res.pieces[index].row_idx = newY
        res.moves += 1
        return res
    return None

# Gets the next puzzle states
def get_child_states(puzzle):
    vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    res = []
    for i, piece in enumerate(puzzle.pieces):
        for (x, y) in vectors:
            new_puzzle = move_piece_ai(puzzle, i, piece.col_idx + x, piece.row_idx + y)
            if new_puzzle:
                res.append(new_puzzle)
    return res


# Checks whether the game has ended or not
def gameOver(puzzle):
    heightRule = puzzle.objectivePiece.row_idx == puzzle.numRows - puzzle.objectivePiece.height
    widthRule = puzzle.objectivePiece.col_idx >= puzzle.exit_x and puzzle.objectivePiece.col_idx + puzzle.objectivePiece.width <= puzzle.exit_x + puzzle.exit_width
    puzzle.isGameOver = puzzle.objectivePiece is not None and heightRule and widthRule
    return puzzle.isGameOver
