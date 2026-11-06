import random

def run_code():
    # EVOLVE-BLOCK-START
    rng=random.Random(0)
    coeff=[rng.randint(1, 1000) for _ in range(208)]
    # EVOLVE-BLOCK-END
    return {"coefficients":coeff}
