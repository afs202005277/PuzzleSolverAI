import math

# distance red block to exit
def h1(puzzle, _):
    # Distance from the red block to the exit.

    vector = (puzzle.objectivePiece.col_idx - puzzle.exit_x,
              puzzle.objectivePiece.row_idx - (puzzle.exit_x + puzzle.exit_width))
    return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])


def h3(puzzle, _):
    # The largest contiguous empty space near the red block.
    matrix = puzzle.show_tui()
    rows, cols = len(matrix), len(matrix[0])

    def dfs(row, col):
        if row < 0 or row >= rows - 1 or col < 0 or col >= cols - 1:
            return 0

        if matrix[row][col]:
            return 0

        size = 1 + dfs(row + 1, col) + dfs(row, col + 1)

        return size

    max = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            tmp = dfs(i, j)
            if max < tmp:
                max = tmp

    return -max


def h2(puzzle, _):
    # weighted sum of the number of obstacles between the red block and the exit
    path = []

    weight = 0
    piece = puzzle.objectivePiece
    for i in range(piece.width):
        for j in range(puzzle.numRows - piece.row_idx):
            path.append((piece.col_idx + i, piece.row_idx + j))
    for piece in puzzle.pieces:
        if not piece.isObjective:
            if (piece.col_idx, piece.row_idx) in path:
                weight += (piece.width ** 2) * piece.height

    return weight


def h4(puzzle, _):
    # H4: Prioritize moves that keep the red block close to the edges of the game board.
    return max(puzzle.objectivePiece.col_idx,
               puzzle.numCols - puzzle.objectivePiece.width - puzzle.objectivePiece.col_idx) * 100


def h5(puzzle, _):
    # Always ensure that the red block has at least one valid move option available.
    index = 0
    for i, piece in enumerate(puzzle.pieces):
        if piece.isObjective:
            index = i
            break
    vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    weight = 0
    for (x, y) in vectors:
        if puzzle.is_valid_move(index, puzzle.pieces[index].col_idx + x, puzzle.pieces[index].row_idx + y):
            weight += 1
    return -weight


def h6(puzzle, _):
    # prioritize fitting pieces along the edges of the game board from largest to smallest
    score = 0
    for piece in puzzle.pieces:
        if not piece.isObjective:
            score += max(piece.col_idx, puzzle.numCols - piece.width - piece.col_idx) * piece.width * piece.height
    return -score


def h7(puzzle, index):
    # prioritize moving the largest pieces first
    if index is not None:
        return puzzle.pieces[index].width * puzzle.pieces[index].height
    return 0


def h8(puzzle, index):
    # prioritize moving the smallest pieces first
    return -h7(puzzle, index)