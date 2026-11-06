"""Return the saved, independently verified Magma BKLC [68,15,24] witness."""
import json
from pathlib import Path


def run_code():
    obj = json.loads(
        (Path(__file__).parent / "data" / "sota_generator.json").read_text()
    )
    return {
        "generator_matrix": [
            [int(bit) for bit in row] for row in obj["matrix"]
        ]
    }
