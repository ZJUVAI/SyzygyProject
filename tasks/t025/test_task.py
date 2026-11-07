import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t025.baseline import run_code as search_run
from tasks.t025.check import validate
from tasks.t025.human import run_code as human_run
from tasks.t025.init_program import run_code as seed_run
from tasks.t025.reference import run_code as reference_run


CONFIG = {
    "id": "T025-C01",
    "parameters": {"dimension": 7, "field_order": 3, "max_points": 288},
    "direction": "maximize",
    "human_reference": 236,
}


def test_human_cap_is_rebuilt_from_author_matrix_and_recomputed():
    solution = human_run()
    result = validate({**solution, "claimed_objective": -1}, CONFIG, strict=True)
    assert solution == reference_run()
    assert len(solution["points"]) == 236
    assert result["objective"] == 236
    assert result["verification_status"] == "exact"
    assert result["details"]["all_distinct_pairs_checked"] is True
    assert result["details"]["claimed_objective_ignored"] is True
    matrix_path = Path(__file__).parent / "data" / "edel_bierbrauer_248_projective_matrix.txt"
    assert hashlib.sha256(matrix_path.read_bytes()).hexdigest() == (
        "0e3ad612ca8ee9259290f4748af505cf6184c2107e77859d3ae6117fe24545eb"
    )


def test_binary_seed_is_a_valid_cap():
    solution = seed_run()
    assert len(solution["points"]) == 128
    assert validate(solution, CONFIG)["objective"] == 128


def test_three_collinear_points_are_rejected():
    points = [[0] * 7, [1] + [0] * 6, [2] + [0] * 6]
    with pytest.raises(ValueError, match="affine line"):
        validate({"points": points}, CONFIG)


def test_duplicate_point_rejected():
    point = [0] * 7
    with pytest.raises(ValueError, match="duplicate"):
        validate({"points": [point, point]}, CONFIG)


@pytest.mark.parametrize("bad", [True, 1.0, "1", -1, 3, float("nan"), float("inf")])
def test_bad_coordinates_rejected(bad):
    point = [0] * 7
    point[0] = bad
    with pytest.raises(ValueError):
        validate({"points": [point]}, CONFIG)


def test_bad_shape_and_configuration_rejected():
    with pytest.raises(ValueError, match="points"):
        validate({"points": None}, CONFIG)
    with pytest.raises(ValueError, match="seven coordinates"):
        validate({"points": [[0] * 6]}, CONFIG)
    with pytest.raises(ValueError, match="configuration"):
        validate({"points": []}, {**CONFIG, "parameters": {"dimension": 6}})


def test_empty_cap_boundary_and_safe_upper_bound():
    assert validate({"points": []}, CONFIG)["objective"] == 0
    too_large = [[(i >> bit) & 1 for bit in range(7)] for i in range(289)]
    # Duplicates would also make this invalid, but the theorem cutoff applies first.
    with pytest.raises(ValueError, match="upper bound"):
        validate({"points": too_large}, CONFIG)


def test_seeded_greedy_search_is_reproducible_and_does_not_read_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    first = search_run()
    second = search_run()
    assert first == second
    assert first["search_metadata"]["seed"] == 17
    assert first["search_metadata"]["iteration_limit"] == 100_000
    assert first["search_metadata"]["budget"]["iteration_limit"] == 100_000
    assert first["search_metadata"]["reference_data_read"] is False
    assert first["search_metadata"]["iterations"] <= 100_000
    assert validate(first, CONFIG)["objective"] == len(first["points"])


def test_zero_second_search_budget_returns_valid_seed(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    solution = search_run()
    assert solution["search_metadata"]["iterations"] == 0
    assert len(solution["points"]) == 128
    assert validate(solution, CONFIG)["objective"] == 128


def test_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
