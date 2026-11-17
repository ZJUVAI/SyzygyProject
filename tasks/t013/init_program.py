def run_code():
    # EVOLVE-BLOCK-START
    length = 100
    sequence = [1 if i % 2 == 0 else -1 for i in range(length)]
    # EVOLVE-BLOCK-END
    return {"sequence": sequence}
