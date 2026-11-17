"""A simple 91-point collinear seed with exact rational coordinates."""


def run_code():
    # EVOLVE-BLOCK-START
    return {
        "minimal_polynomial": [0, 1],
        "isolating_interval": ["-1", "1"],
        "points": [
            {"x": [str(i)], "y": ["0"]}
            for i in range(91)
        ],
    }
    # EVOLVE-BLOCK-END
