"""Rebuild a traditional base-3 Horner expression; no witness file is read."""

TARGET = 2**61 - 1


def _ones(count):
    return "+".join(["1"] * count)


def build_expression(target=TARGET):
    digits = []
    while target:
        target, digit = divmod(target, 3)
        digits.append(digit)
    digits.reverse()
    expression = _ones(digits[0])
    for digit in digits[1:]:
        expression = f"({expression}*(1+1+1))"
        if digit:
            expression = f"({expression}+{_ones(digit)})"
    return expression


def run_code():
    return {"expression": build_expression()}
