"""Self-contained schoolbook bilinear algorithm (27 scalar products)."""


# EVOLVE-BLOCK-START
def run_code():
    terms = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                alpha = [0] * 9
                beta = [0] * 9
                gamma = [0] * 9
                alpha[3 * i + j] = 1
                beta[3 * j + k] = 1
                gamma[3 * i + k] = 1
                terms.append({"alpha": alpha, "beta": beta, "gamma": gamma})
    return {"terms": terms}

# EVOLVE-BLOCK-END
