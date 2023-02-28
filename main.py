class Piece:
    def __init__(self, height, width, row_idx, col_idx, isObjective=False):
        self.id = -1
        self.height = height
        self.width = width
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.isObjective = isObjective

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
        for idx, piece in enumerate(pieces):
            piece.id = idx

    def add_piece(self, size, orientation, x, y):
        piece = Piece(size, orientation, x, y)
        self.pieces.append(piece)

    def move_piece(self, index, newX, newY):
        if self.is_valid_move(index, newX, newY):
            self.pieces[index].x = newX
            self.pieces[index].y = newY

    def is_valid_move(self, index, newX, newY):
        if index < 0 or index >= len(self.pieces):
            print("Invalid Piece")
            return False
        else:
            tmp_piece = self.pieces[index]
            tmp_piece.x = newX
            tmp_piece.y = newY
            occupied_positions = tmp_piece.get_occupied_positions()
            for piece in self.pieces:
                if piece.id != tmp_piece.id and any(
                        map(lambda x: x in occupied_positions, piece.get_occupied_positions())):
                    print("Invalid position")
                    return False
            return True

    def show_tui(self):
        representation = [[[] for _ in range(self.numCols)] for _ in range(self.numRows+1)]
        for piece in self.pieces:
            piece.show_tui(representation)
        for i in range(self.exit_x):
            representation[self.exit_y][i] = '-'
        for i in range(self.exit_x+self.exit_width, self.numCols):
            representation[self.exit_y][i] = '-'
        print(representation)

    def show_gui(self):
        print("TO BE DONE")


def first_map():
    pieces = [Piece(2, 1, 0, 0), Piece(2, 1, 0, 1), Piece(2, 1, 0, 3), Piece(2, 1, 2, 0), Piece(2, 1, 2, 1), Piece(2, 2, 2, 2, True), Piece(1, 1, 4, 0), Piece(1, 1, 4, 1), Piece(1, 1, 4, 2), Piece(1, 1, 4, 3)]

    puzzle = Puzzle(5, 4, pieces)

    puzzle.show_tui()


first_map()
