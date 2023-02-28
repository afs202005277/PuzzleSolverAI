class Piece:
    def __init__(self, height, width, x, y, isObjective=False):
        self.id = -1
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.isObjective = isObjective

    def get_occupied_positions(self):
        return [(self.x + x, self.y + y) for y in range(self.height) for x in range(self.width)]

    def show_tui(self, representation):
        positions = self.get_occupied_positions()
        for (x, y) in positions:
            representation[x][y] = self.id

    def show_gui(self):
        print("TO BE DONE")


class Puzzle:
    def __init__(self, numRows, numCols, pieces=None):
        if pieces is None:
            pieces = []
        self.numRows = numRows
        self.numCols = numCols
        self.pieces = pieces
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
        representation = [[[] for _ in range(self.numCols)] for _ in range(self.numRows)]
        for piece in self.pieces:
            piece.show_tui(representation)
        print(representation)

    def show_gui(self):
        print("TO BE DONE")


def first_map():
    pieces = [Piece(2, 1, 0, 0), Piece(2, 1, 1, 0), Piece(2, 1, 3, 0), Piece(2, 1, 0, 2), Piece(2, 1, 1, 2),
              Piece(2, 2, 2, 2, True), Piece(1, 1, 0, 4), Piece(1, 1, 1, 4), Piece(1, 1, 2, 4), Piece(1, 1, 3, 4)]

    puzzle = Puzzle(4, 5, pieces)

    puzzle.show_tui()

    puzzle.move_piece(2, 2, 0)

    puzzle.show_tui()


first_map()
