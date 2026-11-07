"""Search-space helpers for positive diagonal complex PSD matrices."""


def matrices_from_diagonals(diagonals):
    matrices = []
    for diagonal in diagonals:
        matrix = []
        for row in range(3):
            matrix.append([[int(diagonal[row]) if row == col else 0, 0] for col in range(3)])
        matrices.append(matrix)
    return {"matrices": matrices}


def initial_diagonals():
    return [[1, 1, 1] for _ in range(4)]
