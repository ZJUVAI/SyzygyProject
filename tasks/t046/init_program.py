"""Cold start: the monomial x^146."""


# EVOLVE-BLOCK-START
def run_code():
    import math
    import os

    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T046-C01")
    if config_id != "T046-C01":
        raise ValueError(f"unsupported configuration: {config_id}")

    coefficients = [0] * 147
    coefficients[146] = 1
    return {"coefficients": coefficients}
# EVOLVE-BLOCK-END
