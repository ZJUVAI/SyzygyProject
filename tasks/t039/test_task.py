from pathlib import Path

import pytest

from tasks.t039.baseline import run_code as baseline_run_code
from tasks.t039.check import validate
from tasks.t039.human import run_code as human_run_code
from tasks.t039.init_program import run_code as init_run_code
from tasks.t039.reference import run_code as reference_run_code
from tasks.t039.evolution import run_code as evolution_run_code


CONFIG = {
    "id": "T039-C01",
    "parameters": {"rows": 7, "marks_per_row": 6},
    "direction": "minimize",
    "human_reference": 112,
}


def _example_rows():
    return [
        [0, 1, 3, 8, 14, 18],
        [0, 10, 21, 33, 46, 60],
        [0, 20, 42, 66, 92, 120],
        [0, 30, 63, 99, 138, 180],
        [0, 40, 84, 132, 184, 240],
        [0, 50, 105, 165, 230, 300],
        [0, 60, 126, 198, 276, 360],
    ]


def test_published_human_and_reference_witnesses():
    for program in (human_run_code, reference_run_code):
        result = validate(program(), CONFIG)
        assert result["objective"] == 112
        assert result["verification_status"] == "exact"
        assert result["details"]["within_row_differences_checked"] == 105
        assert result["details"]["distinct_differences"] == 105


def test_valid_simple_seed_and_search_entries():
    for program in (init_run_code, baseline_run_code, evolution_run_code):
        result = validate(program(), CONFIG)
        assert result["verification_status"] == "exact"
        assert isinstance(result["objective"], int)


def test_valid_example_allows_shared_marks_across_rows():
    rows = init_run_code()["rows"]
    assert rows[0][0] == rows[1][0] == 0
    result = validate({"rows": rows, "claimed_score": -999}, CONFIG)
    assert result["objective"] == max(row[-1] for row in rows)


def test_translation_is_score_invariant():
    rows = [[mark + 17 for mark in row] for row in human_run_code()["rows"]]
    assert validate(rows, CONFIG)["objective"] == 112


@pytest.mark.parametrize("rows", [
    [[0, 1, 3, 8, 14, 18]] * 7,  # repeated differences across rows
    [[0, 1, 3, 8, 14, 14]] + _example_rows()[1:],
    [[False, 1, 3, 8, 14, 18]] + _example_rows()[1:],
    [[0, 1.0, 3, 8, 14, 18]] + _example_rows()[1:],
    [[0, -1, 3, 8, 14, 18]] + _example_rows()[1:],
    _example_rows()[:6],
    _example_rows() + [[0, 1, 3, 8, 14, 18]],
    [[0, 1, 3, 8, 14]] + _example_rows()[1:],
])
def test_invalid_constructions_rejected(rows):
    with pytest.raises(ValueError):
        validate({"rows": rows, "claimed_score": 0}, CONFIG)


@pytest.mark.parametrize("bad_mark", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_marks_rejected(bad_mark):
    rows = _example_rows()
    rows[0][1] = bad_mark
    with pytest.raises(ValueError):
        validate(rows, CONFIG)


def test_configuration_validation_rejects_bool_and_invalid_counts():
    for parameters in ({"rows": True, "marks_per_row": 6},
                       {"rows": 7, "marks_per_row": False},
                       {"rows": 0, "marks_per_row": 6}):
        with pytest.raises(ValueError):
            validate(_example_rows(), {"parameters": parameters})


def test_search_is_seeded_and_keeps_claimed_scores_out_of_evaluation(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T039-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "19")
    first = baseline_run_code()
    second = baseline_run_code()
    assert first == second
    before = validate(first, CONFIG)["objective"]
    first["claimed_score"] = -10**100
    assert validate(first, CONFIG)["objective"] == before


def test_program_error_and_generation_timeout_are_categorized(tmp_path, monkeypatch):
    import mathbench.evaluate as shared_evaluator

    monkeypatch.setattr(shared_evaluator, "load_config", lambda *_: CONFIG)
    monkeypatch.setattr(shared_evaluator, "task_path", lambda *_: Path(__file__).parent)
    invalid_program = tmp_path / "invalid.py"
    invalid_program.write_text("def run_code():\n    raise RuntimeError('broken program')\n", encoding="utf-8")
    failed = shared_evaluator.evaluate_candidate("T039", invalid_program, "T039-C01")
    assert failed["error_category"] == "program_error"

    slow_program = tmp_path / "slow.py"
    slow_program.write_text("import time\ndef run_code():\n    time.sleep(2)\n", encoding="utf-8")
    timed_out = shared_evaluator.evaluate_candidate(
        "T039", slow_program, "T039-C01", generation_timeout=0.1)
    assert timed_out["error_category"] == "generation_timeout"
