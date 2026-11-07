"""Rebuild the 32-element initial segment of the Odlyzko-Stanley S(1) sequence."""


def run_code():
    elements = [
        1 + sum(digit * (3**place) for place, digit in enumerate(bits))
        for bits in _binary_digit_vectors(5)
    ]
    return {"elements": elements}


def _binary_digit_vectors(width):
    if width == 0:
        yield ()
        return
    for prefix in _binary_digit_vectors(width - 1):
        yield prefix + (0,)
        yield prefix + (1,)
