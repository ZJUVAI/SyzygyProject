"""Exact peaceable-queens feasibility checker for T082."""

from collections.abc import Mapping


CONFIG_ID = "T082-C01"
BOARD_SIZE = 30
MAX_ARMY = BOARD_SIZE * BOARD_SIZE // 4
PARAMETERS = {
    "board_size": 30,
    "queen_movement": "standard row, column, and diagonal",
    "equal_armies": True,
    "same_color_attacks_allowed": True,
}


def _check_config(config):
    if not isinstance(config, Mapping) or config.get("id") != CONFIG_ID:
        raise ValueError(f"unsupported configuration; expected {CONFIG_ID}")
    if config.get("parameters") != PARAMETERS:
        raise ValueError("configuration must fix the 30x30 peaceable-queens model")


def _read_army(solution, name):
    raw = solution.get(name)
    if not isinstance(raw, (list, tuple)):
        raise ValueError(f"{name} must be a list of [row,column] pairs")
    army = []
    seen = set()
    for index, square in enumerate(raw):
        if not isinstance(square, (list, tuple)) or len(square) != 2:
            raise ValueError(f"{name}[{index}] must contain exactly two coordinates")
        row, column = square
        if type(row) is not int or type(column) is not int:
            raise ValueError(f"{name}[{index}] coordinates must be integers; bool is invalid")
        if not (0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE):
            raise ValueError(f"{name}[{index}] lies outside the 30x30 board")
        if (row, column) in seen:
            raise ValueError(f"{name} contains a duplicate square")
        seen.add((row, column))
        army.append((row, column))
    return army


def validate(solution, config, strict=False):
    _check_config(config)
    if not isinstance(solution, Mapping):
        raise ValueError("solution must be an object")
    white = _read_army(solution, "white")
    black = _read_army(solution, "black")
    if len(white) != len(black):
        raise ValueError("white and black armies must have equal sizes")
    army_size = len(white)
    if army_size > MAX_ARMY:
        raise ValueError("army size exceeds the proven 225 upper bound")
    white_squares = set(white)
    black_squares = set(black)
    if white_squares & black_squares:
        raise ValueError("opposite colors cannot occupy the same square")

    attacks = 0
    for wr, wc in white:
        for br, bc in black:
            if wr == br or wc == bc or abs(wr - br) == abs(wc - bc):
                attacks += 1
    if attacks:
        raise ValueError("white and black queens must not attack each other")

    occupied_white_rows = len({row for row, _ in white})
    occupied_black_rows = len({row for row, _ in black})
    occupied_white_columns = len({column for _, column in white})
    occupied_black_columns = len({column for _, column in black})
    return {
        "objective": army_size,
        "verification_status": "exact",
        "details": {
            "board_size": BOARD_SIZE,
            "army_size_each_color": army_size,
            "total_queens": 2 * army_size,
            "cross_color_pairs_checked": army_size * army_size,
            "cross_color_attacking_pairs": 0,
            "cross_color_square_overlap": False,
            "occupied_rows": {
                "white": occupied_white_rows,
                "black": occupied_black_rows,
                "disjoint": occupied_white_rows + occupied_black_rows <= BOARD_SIZE,
            },
            "occupied_columns": {
                "white": occupied_white_columns,
                "black": occupied_black_columns,
                "disjoint": occupied_white_columns + occupied_black_columns <= BOARD_SIZE,
            },
            "proven_upper_bound": MAX_ARMY,
            "claimed_objective_ignored": True,
            "strict": bool(strict),
        },
    }
