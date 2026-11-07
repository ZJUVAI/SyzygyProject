import json
from fractions import Fraction
from pathlib import Path

import pytest

from tasks.t041.baseline import run_code as baseline
from tasks.t041.check import validate
from tasks.t041.evolution import run_code as evolution
from tasks.t041.human import run_code as human
from tasks.t041.init_program import run_code as initial
from tasks.t041.reference import run_code as reference

ROOT = Path(__file__).parent
CONFIG = {
    "id": "T041-C01",
    "parameters": {
        "square_count": 17,
        "container": "closed unit square [0,1]^2",
        "orientation": "arbitrary",
        "interior_disjoint": True,
        "objective": "sum of the 17 side lengths",
    },
}


def test_initial_human_and_search_are_valid():
    assert validate(initial(), CONFIG, strict=True)["objective"] == "1"
    assert validate(human(), CONFIG, strict=True)["objective"] == "4"
    search = baseline()
    checked = validate(search, CONFIG, strict=True)
    assert checked["objective"] == "4"
    assert search["search_metadata"]["iterations_attempted"] == 32
    assert search["search_metadata"]["seed"] == 6


def test_evolution_runner_entry_and_fixed_reference():
    assert validate(evolution(), CONFIG, strict=True)["objective"] == "4"
    expected = json.loads((ROOT / "data" / "public_witness.json").read_text())
    assert reference() == expected
    result = validate(reference(), CONFIG, strict=True)
    assert result["objective"] == "2190452873/547596200"
    assert result["details"]["pairs_checked"] == 136


def test_human_archive_is_exact_and_fully_checked():
    witness = json.loads((ROOT / "data" / "human_grid_witness.json").read_text())
    assert human()["squares"] == witness["squares"]
    result = validate(witness, CONFIG, strict=True)
    assert Fraction(result["objective"]) == 15*Fraction(1, 4) + 2*Fraction(1, 8) == 4
    assert result["details"]["corners_checked"] == 68


def test_claimed_score_is_ignored():
    item = reference()
    item["claimed_score"] = "999999999999999999"
    item["objective"] = "999999999999999999"
    checked = validate(item, CONFIG, strict=True)
    assert checked["objective"] == "2190452873/547596200"
    assert checked["details"]["claimed_objective_ignored"] is True


def test_touching_is_valid_and_exact_orientation_is_checked():
    witness = human()
    assert validate(witness, CONFIG, strict=True)["objective"] == "4"
    tilted = reference()
    assert tilted["squares"][-1]["cos"] == "255/257"
    assert tilted["squares"][-1]["sin"] == "32/257"
    assert validate(tilted, CONFIG, strict=True)["verification_status"] == "exact"


@pytest.mark.parametrize("mutate", [
    lambda s: s["squares"].pop(),
    lambda s: s["squares"][0].update(x="-1/10"),
    lambda s: s["squares"][1].update(side="0"),
    lambda s: s["squares"][1].update(x=s["squares"][0]["x"], y=s["squares"][0]["y"], side=s["squares"][0]["side"]),
    lambda s: s["squares"][0].update(side=True),
    lambda s: s["squares"][0].update(x=float("nan")),
    lambda s: s["squares"][0].update(y=float("inf")),
    lambda s: s["squares"][0].update(y=float("-inf")),
    lambda s: s["squares"][0].update(cos="1/2", sin="1/2"),
])
def test_invalid_witnesses_are_rejected(mutate):
    item = human()
    mutate(item)
    with pytest.raises(ValueError):
        validate(item, CONFIG, strict=True)


def test_candidate_runtime_error_and_timeout_are_reported(tmp_path, monkeypatch):
    import mathbench.registry as registry
    from tasks.t041.evaluator import evaluate

    # The main reviewer registers new IDs only after admission. Make this
    # task-local test exercise the worker without changing the shared registry.
    monkeypatch.setattr(registry, "INITIAL_TASKS", registry.INITIAL_TASKS + ("T041",))

    valid_solution = initial()
    valid_solution["objective"] = "999999999999"
    valid_program = tmp_path / "valid_program.py"
    valid_program.write_text(
        "import json\n"
        f"SOLUTION = {json.dumps(valid_solution)!r}\n"
        "def run_code():\n    return json.loads(SOLUTION)\n"
    )
    valid = evaluate(valid_program, "T041-C01", strict=True,
                     generation_timeout=300, verification_timeout=60)
    assert valid["validity"] == 1.0
    assert valid["objective"] == "1"
    assert valid["combined_score"] == 0.25
    assert valid["details"]["claimed_objective_ignored"] is True

    error_program = tmp_path / "error_program.py"
    error_program.write_text("def run_code():\n    raise RuntimeError('deliberate')\n")
    error = evaluate(error_program, "T041-C01",
                     generation_timeout=300, verification_timeout=60)
    assert error["validity"] == 0.0
    assert error["objective"] is None
    assert error["error_category"] == "program_error"

    timeout_program = tmp_path / "timeout_program.py"
    timeout_program.write_text("import time\ndef run_code():\n    time.sleep(3)\n    return {}\n")
    timeout = evaluate(timeout_program, "T041-C01", generation_timeout=0.25)
    assert timeout["validity"] == 0.0
    assert timeout["objective"] is None
    assert timeout["error_category"] == "generation_timeout"
