"""A simple B_3 set from distinct base-4 digit positions."""


def run_code():
    # EVOLVE-BLOCK-START
    # Each three-term sum has base-4 digits in {0,1,2,3}; no carry occurs.
    elements = [0] + [4 ** exponent for exponent in range(30)]
    # EVOLVE-BLOCK-END
    return {"elements": elements}
