"""Tests for the T078 exact lattice task."""

import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import pytest

from tasks.t078 import baseline, check, evolution, human, init_program, reference


TASK = Path(__file__).resolve().parent
CONFIG = json.loads((TASK / "task.json").read_text())["configurations"][0]


def _quadratic(gram, vector):
    return sum(vector[i] * gram[i][j] * vector[j] for i in range(10) for j in range(10))


def test_all_five_entries_and_frozen_lattice_witnesses():
    initial = init_program.run_code()
    search = baseline.run_code()
    human_solution = human.run_code()
    reference_solution = reference.run_code()
    evolution_solution = evolution.run_code()
    results = [
        check.validate(item, CONFIG)
        for item in (initial, search, human_solution, reference_solution, evolution_solution)
    ]
    assert results[0]["objective"] == 4**10
    assert results[1]["objective"] == 3072
    assert results[2]["objective"] == results[3]["objective"] == 768
    assert results[4]["objective"] == 3072
    assert human_solution["gram"] == reference_solution["gram"]
    assert search["search_metadata"]["trials_completed"] == 32
    assert search["search_metadata"]["reference_data_read"] is False
    saved = json.loads((TASK / "best/seed-0.json").read_text())
    assert check.validate(saved, CONFIG)["objective"] == 3072
    assert saved["gram"] == search["gram"]
    raw_source = (TASK / "data/source/lambda10.html").read_bytes()
    assert hashlib.sha256(raw_source).hexdigest() == (
        "10a1fa86d38c92c30d4df0f95169d0fee64e3584bc7316e35b19d0c325229c1a"
    )
    for path in (TASK / "data/human/lambda10_gram.json",):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == (
            "b515415581cb5044212b611d12ef3cf7cdc396b0f07d1c8cd7c605ae3750e886"
        )


def test_lattice_short_vector_certificate_matches_catalogue():
    gram = human.build_lambda10()["gram"]
    certificate = json.loads((TASK / "data/human/lambda10_minimal_vectors.json").read_text())["vectors"]
    assert len(certificate) == 336
    assert len({tuple(vector) for vector in certificate}) == 336
    assert all(any(vector) and _quadratic(gram, vector) == 4 for vector in certificate)
    vectors, _ = check._enumerate_vectors(
        [[check.Fraction(value) for value in row] for row in gram],
        check.Fraction(4),
        inclusive=True,
    )
    assert {tuple(vector) for vector in vectors} == {tuple(vector) for vector in certificate}


def test_claimed_objective_fields_do_not_change_validation():
    solution = reference.run_code()
    expected = check.validate(solution, CONFIG, strict=True)
    for key in ("objective", "score", "claimed_score"):
        changed = copy.deepcopy(solution)
        changed[key] = "1/999999"
        assert check.validate(changed, CONFIG, strict=True) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


@pytest.mark.parametrize(
    "gram, message",
    [
        ([[4] * 9] * 10, "10 entries"),
        ([[4 if i == j else 0 for j in range(10)] for i in range(10 - 1)], "10x10"),
    ],
)
def test_invalid_shapes_or_singular_forms_are_rejected(gram, message):
    with pytest.raises(ValueError, match=message):
        check.validate({"gram": gram}, CONFIG)


def test_rejects_nonsymmetric_and_short_vector_gram_matrices():
    nonsymmetric = [[4 if i == j else 0 for j in range(10)] for i in range(10)]
    nonsymmetric[0][1] = 1
    with pytest.raises(ValueError, match="symmetric"):
        check.validate({"gram": nonsymmetric}, CONFIG)
    too_short = [[3 if i == j == 0 else 4 if i == j else 0 for j in range(10)] for i in range(10)]
    with pytest.raises(ValueError, match="below 4"):
        check.validate({"gram": too_short}, CONFIG)


def test_rejects_singular_gram_matrix_with_duplicate_basis_rows():
    singular = [[4 if i == j else 0 for j in range(10)] for i in range(10)]
    singular[0][1] = singular[1][0] = 4
    with pytest.raises(ValueError, match="positive definite"):
        check.validate({"gram": singular}, CONFIG)


@pytest.mark.parametrize("entry", [True, 4.0, float("nan"), "NaN", "4/0", "1/-2"])
def test_rejects_boolean_float_nan_and_malformed_rationals(entry):
    gram = [[4 if i == j else 0 for j in range(10)] for i in range(10)]
    gram[0][0] = entry
    with pytest.raises(ValueError):
        check.validate({"gram": gram}, CONFIG)


def test_exact_rational_and_very_large_integer_entries_have_no_cap():
    rational_identity = [["4/1" if i == j else "0" for j in range(10)] for i in range(10)]
    assert check.validate({"gram": rational_identity}, CONFIG)["objective"] == 4**10
    rational_diagonal = [[4 if i == j else 0 for j in range(10)] for i in range(10)]
    rational_diagonal[0][0] = "17/4"
    assert check.validate({"gram": rational_diagonal}, CONFIG)["objective"] == 4**8 * 17
    rational_diagonal[0][0] = "21/5"
    assert check.validate({"gram": rational_diagonal}, CONFIG)["objective"] == str(check.Fraction(4**9 * 21, 5))
    gram = [[4 if i == j else 0 for j in range(10)] for i in range(10)]
    gram[1][1] = str(10**5000)
    result = check.validate({"gram": gram}, CONFIG)
    assert result["objective"] == 4**9 * 10**5000


def test_config_and_seed_are_fixed_and_repeatable(monkeypatch):
    with pytest.raises(ValueError):
        check.validate(init_program.run_code(), {**CONFIG, "id": "T078-C02"})
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T078-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "42")
    assert baseline.run_code() == baseline.run_code()
    monkeypatch.setenv("MATHBENCH_SEED", "not-an-integer")
    with pytest.raises(ValueError, match="MATHBENCH_SEED"):
        baseline.run_code()


def test_runner_errors_and_timeouts_are_checked_without_task_registration():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="T078 deliberate error"):
        _run([sys.executable, "-c", "raise RuntimeError('T078 deliberate error')"], env, 5)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
    assert time.monotonic() - start < 3
