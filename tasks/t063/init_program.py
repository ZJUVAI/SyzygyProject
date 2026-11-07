"""Standalone simple seed: x^100 - 2 with proposed rational root disks."""
import math
import os


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T063-C01") != "T063-C01":
        raise ValueError("unsupported configuration")
    int(os.environ.get("MATHBENCH_SEED", "0"))
    # EVOLVE-BLOCK-START
    degree = 100
    scale = 10**16
    radius = "1/100000000000000"
    root_radius = 2.0 ** (1.0 / degree)
    disks = []
    for k in range(degree):
        angle = 2.0 * math.pi * k / degree
        real = round(root_radius * math.cos(angle) * scale)
        imag = round(root_radius * math.sin(angle) * scale)
        disks.append({"center_real": f"{real}/{scale}",
                      "center_imag": f"{imag}/{scale}",
                      "radius": radius})
    coefficients = [-2] + [0] * (degree - 1) + [1]
    # EVOLVE-BLOCK-END
    return {"coefficients_ascending": coefficients, "root_disks": disks}


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
