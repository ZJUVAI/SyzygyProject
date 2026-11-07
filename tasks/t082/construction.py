"""Small search helpers for valid cross-color queen placements."""

import random


N = 30


def attacks(a, b):
    return a[0] == b[0] or a[1] == b[1] or abs(a[0] - b[0]) == abs(a[1] - b[1])


def _free_against(square, opposite):
    row, column = square
    return all(not attacks(square, other) for other in opposite)


def try_add_pair(white, black, rng):
    white_set = set(map(tuple, white))
    black_set = set(map(tuple, black))
    squares = [(row, col) for row in range(N) for col in range(N)]
    rng.shuffle(squares)
    for new_white in squares:
        if new_white in white_set or not _free_against(new_white, black):
            continue
        updated_white = white + [new_white]
        black_candidates = [
            square for square in squares
            if square not in black_set and _free_against(square, updated_white)
        ]
        if black_candidates:
            new_black = rng.choice(black_candidates)
            return updated_white, black + [new_black]
    return None


def greedy_layout(rng, max_army=45, tries_per_extension=1):
    white, black = [(0, 0)], [(1, 2)]
    while len(white) < max_army:
        result = None
        for _ in range(tries_per_extension):
            result = try_add_pair(white, black, rng)
            if result is not None:
                break
        if result is None:
            break
        white, black = result
    return {"white": [list(x) for x in white], "black": [list(x) for x in black]}


def mutate_layout(layout, rng):
    white = [tuple(x) for x in layout["white"]]
    black = [tuple(x) for x in layout["black"]]
    if len(white) > 1 and rng.random() < 0.35:
        index = rng.randrange(len(white))
        white.pop(index)
        black.pop(index)
    result = try_add_pair(white, black, rng)
    if result is not None:
        white, black = result
    return {"white": [list(x) for x in white], "black": [list(x) for x in black]}
