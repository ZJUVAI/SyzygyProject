"""Exact feasibility, source replay, and runner-control tests for T082."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t082.check import MAX_ARMY, PARAMETERS, validate


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T082-C01", "parameters": PARAMETERS}
WITNESS_HASH = "97350f71d71e4537ec694259c8b9c5805560bdfdb0198702887c2c4f158cd5a4"
SOURCE_HASH = "a5da2c9d852ecc24f8abcfcdc1b219d998e58d27ca6758cc4757041714fb4cfc"


def _line_attack(a, b):
    return a[0] == b[0] or a[1] == b[1] or abs(a[0] - b[0]) == abs(a[1] - b[1])


def test_public_layout_exactly_reconstructs_and_verifies_131():
    path = ROOT / "data/reference/peaceable_queens_n30_131.json"
    source = ROOT / "data/source/kamenetsky_2019.txt"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == WITNESS_HASH
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_HASH
    witness = json.loads(path.read_text(encoding="utf-8"))
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 131
    assert result["details"]["cross_color_pairs_checked"] == 131**2 == 17161
    assert result["details"]["cross_color_attacking_pairs"] == 0
    assert len(witness["white"]) == len(witness["black"]) == 131
    assert all(not _line_attack(w, b) for w in witness["white"] for b in witness["black"])


def test_human_parser_and_reference_program_replay_same_witness():
    from tasks.t082.human import run_code as human_run
    from tasks.t082.reference import run_code as reference_run

    human = human_run()
    reference = reference_run()
    assert human == reference
    assert validate(human, CONFIG)["objective"] == 131


def test_finite_row_column_upper_bound_is_225():
    n = PARAMETERS["board_size"]
    assert MAX_ARMY == n * n // 4 == 225
    # For four equal occupied row/column blocks, Cauchy-Schwarz is tight.
    assert 2 * (MAX_ARMY**0.5) == n
    witness = json.loads((ROOT / "data/reference/peaceable_queens_n30_131.json").read_text())
    rows_w = len({r for r, _ in witness["white"]})
    rows_b = len({r for r, _ in witness["black"]})
    cols_w = len({c for _, c in witness["white"]})
    cols_b = len({c for _, c in witness["black"]})
    assert rows_w + rows_b <= n
    assert cols_w + cols_b <= n


def test_checker_allows_same_color_attacks_but_rejects_cross_attack():
    valid_same_color_attack = {
        "white": [[0, 0], [0, 1]],
        "black": [[29, 15], [29, 16]],
    }
    assert validate(valid_same_color_attack, CONFIG)["objective"] == 2
    invalid_diagonal = {"white": [[0, 0]], "black": [[1, 1]]}
    with pytest.raises(ValueError, match="must not attack"):
        validate(invalid_diagonal, CONFIG)
    invalid_row = {"white": [[3, 1]], "black": [[3, 9]]}
    with pytest.raises(ValueError, match="must not attack"):
        validate(invalid_row, CONFIG)
    invalid_column = {"white": [[1, 3]], "black": [[9, 3]]}
    with pytest.raises(ValueError, match="must not attack"):
        validate(invalid_column, CONFIG)


def test_boundaries_empty_layout_and_malformed_coordinates():
    assert validate({"white": [], "black": []}, CONFIG)["objective"] == 0
    assert validate({"white": [[0, 0]], "black": [[29, 28]]}, CONFIG)["objective"] == 1
    bad_solutions = [
        {"white": [[0, 0]], "black": []},
        {"white": [[0, 0], [0, 0]], "black": [[29, 28], [28, 29]]},
        {"white": [[0, 0]], "black": [[0, 0]]},
        {"white": [[True, 0]], "black": [[29, 28]]},
        {"white": [[0, 1.0]], "black": [[29, 28]]},
        {"white": [[float("nan"), 0]], "black": [[29, 28]]},
        {"white": [[-1, 0]], "black": [[29, 28]]},
        {"white": [[30, 0]], "black": [[29, 28]]},
        {"white": [[0]], "black": [[29, 28]]},
        {"white": ["0,0"], "black": [[29, 28]]},
    ]
    for solution in bad_solutions:
        with pytest.raises(ValueError):
            validate(solution, CONFIG)


def test_claimed_score_cannot_change_validation_result():
    candidate = {"white": [[0, 0]], "black": [[1, 2]]}
    expected = validate(candidate, CONFIG)
    for key, value in (("objective", 999), ("score", float("nan")), ("claimed_score", {"fake": True})):
        assert validate({**candidate, key: value}, CONFIG) == expected


def test_all_five_run_code_entries_return_feasible_layouts(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T082-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    monkeypatch.setenv("MATHBENCH_BASELINE_ITERATIONS", "1")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "1")
    monkeypatch.setenv("MATHBENCH_POPULATION", "2")
    from tasks.t082.init_program import run_code as initial
    from tasks.t082.baseline import run_code as baseline
    from tasks.t082.evolution import run_code as evolution
    from tasks.t082.human import run_code as human
    from tasks.t082.reference import run_code as reference

    outputs = [initial(), baseline(), evolution(), human(), reference()]
    results = [validate(output, CONFIG, strict=True) for output in outputs]
    assert results[0]["objective"] == 1
    assert results[3]["objective"] == results[4]["objective"] == 131
    assert 0 <= results[1]["objective"] <= 225
    assert 0 <= results[2]["objective"] <= 225
    assert outputs[1]["search_metadata"]["restarts_run"] == 1
    assert outputs[2]["search_metadata"]["generations_run"] == 1


def test_records_and_sota_match_recomputed_witness():
    sota = json.loads((ROOT / "sota.json").read_text())
    records = json.loads((ROOT / "records.json").read_text())
    witness = json.loads((ROOT / "data/reference/peaceable_queens_n30_131.json").read_text())
    actual = validate(witness, CONFIG)["objective"]
    entry = sota["configurations"]["T082-C01"]
    record = records["configurations"]["T082-C01"]
    assert entry["reproduced_value"] == entry["public_value"] == actual
    assert entry["highest_reported"]["value"] == actual
    assert entry["best_reproduced"]["value"] == actual
    assert record["best_reproduced"]["value"] == actual
    assert entry["best_reproduced"]["witness_sha256"] == WITNESS_HASH


def test_runner_reports_worker_errors_and_timeouts():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T082 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T082 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
