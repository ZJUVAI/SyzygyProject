"""Exact finite-set and interval tests for T080-C01."""

import hashlib
import json
import os
from math import comb
from pathlib import Path
import sys

import pytest

from tasks.t080.check import PARAMETERS, validate
from tasks.t080.construction import projected_simplex


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T080-C01", "parameters": PARAMETERS}
WITNESS_SHA256 = "39cb22a35e93fdd3a2431a121f3b8fa015c0b8ce5c84ca5304cfcb1c59777f39"
DISTINCTION_SHA256 = "3a063ce60ca94b3b45040f1e8b907282a2fc167eebc979120a18b18d4972eb53"


def _counts(values):
    sums = {a + b for a in values for b in values}
    differences = {a - b for a in values for b in values}
    return len(sums), len(differences)


def _mp_bounds(interval):
    import mpmath as mp
    return mp.mpf(interval[0]), mp.mpf(interval[1])


def _iv_bounds(value):
    def low(endpoint):
        return str(endpoint).strip().strip("[]").split(",", 1)[0].strip()
    def high(endpoint):
        return str(endpoint).strip().strip("[]").split(",")[-1].strip()
    return low(value.a), high(value.b)


def test_published_v65_formula_exact_counts_and_strict_lemma_condition():
    witness_path = ROOT / "data/reference/gyarmati_hennecart_ruzsa_m6_l5.json"
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == WITNESS_SHA256
    saved = json.loads(witness_path.read_text(encoding="utf-8"))
    values, weights = projected_simplex(6, 5)
    assert values == saved["set"]
    assert weights == [1, 11, 111, 1111, 11111, 111111]
    assert len(values) == comb(11, 6) == 462
    assert max(values) == 555555
    sum_size, difference_size = _counts(values)
    formula_difference_size = sum(comb(6, k) ** 2 * comb(11-k, 6) for k in range(7))
    assert sum_size == comb(16, 6) == 8008
    assert difference_size == formula_difference_size == 39733
    assert difference_size < 2 * max(values) + 1 == 1111111
    checked = validate({"set": values}, CONFIG)
    assert checked["details"]["strict_difference_bound_verified"] is True
    assert checked["details"]["q"] == 1111111


def test_human_and_reference_replay_exact_finite_witness():
    from tasks.t080.human import run_code as human_run
    from tasks.t080.reference import run_code as reference_run

    human = human_run()
    reference = reference_run()
    assert human == reference
    checked = validate(human, CONFIG, strict=True)
    assert (checked["details"]["cardinality"], checked["details"]["sumset_size"],
            checked["details"]["difference_set_size"], checked["details"]["q"]) == (462, 8008, 39733, 1111111)
    assert checked["details"]["objective_interval"][0] == checked["objective"]
    import mpmath as mp
    mp.mp.dps = 100
    low, high = _mp_bounds(checked["details"]["objective_interval"])
    exact_real_score = 1 + mp.log(mp.mpf(39733) / 8008) / mp.log(1111111)
    assert low <= exact_real_score <= high


def test_t080_is_not_order_equivalent_to_t012_or_t077():
    path = ROOT / "data/source/objective_distinction_examples.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == DISTINCTION_SHA256
    data = json.loads(path.read_text(encoding="utf-8"))["examples"]
    from mpmath import iv
    iv.dps = 70

    t012 = data["T012_vs_T080"]
    U_a, U_b = t012["A"], t012["B"]
    n_a, (s_a, d_a) = len(U_a), _counts(U_a)
    n_b, (s_b, d_b) = len(U_b), _counts(U_b)
    assert (n_a, s_a, d_a, max(U_a)) == (8, 26, 25, 14)
    assert (n_b, s_b, d_b, max(U_b)) == (16, 78, 75, 1014)
    assert d_a < 2 * max(U_a) + 1 and d_b < 2 * max(U_b) + 1
    assert s_a > d_a > n_a and s_b > d_b > n_b
    t012_a = iv.ln(iv.mpf(s_a) / n_a) / iv.ln(iv.mpf(d_a) / n_a)
    t012_b = iv.ln(iv.mpf(s_b) / n_b) / iv.ln(iv.mpf(d_b) / n_b)
    t080_a = validate({"set": U_a}, CONFIG)["details"]["objective_interval"]
    t080_b = validate({"set": U_b}, CONFIG)["details"]["objective_interval"]
    t012_a_bounds = tuple(map(__import__("mpmath").mpf, _iv_bounds(t012_a)))
    t012_b_bounds = tuple(map(__import__("mpmath").mpf, _iv_bounds(t012_b)))
    t080_a_bounds, t080_b_bounds = _mp_bounds(t080_a), _mp_bounds(t080_b)
    assert t012_a_bounds[0] > t012_b_bounds[1]
    assert t080_a_bounds[1] < t080_b_bounds[0]

    t077 = data["T077_vs_T080"]
    U_c, U_d = t077["C"], t077["D"]
    n_c, (s_c, d_c) = len(U_c), _counts(U_c)
    n_d, (s_d, d_d) = len(U_d), _counts(U_d)
    assert (n_c, s_c, d_c, max(U_c)) == (10, 28, 37, 21)
    assert (n_d, s_d, d_d, max(U_d)) == (19, 190, 343, 262143)
    assert d_c < 2 * max(U_c) + 1 and d_d < 2 * max(U_d) + 1
    t077_c = iv.ln(iv.mpf(d_c)) / iv.ln(iv.mpf(s_c))
    t077_d = iv.ln(iv.mpf(d_d)) / iv.ln(iv.mpf(s_d))
    t080_c = _mp_bounds(validate({"set": U_c}, CONFIG)["details"]["objective_interval"])
    t080_d = _mp_bounds(validate({"set": U_d}, CONFIG)["details"]["objective_interval"])
    t077_c_bounds = tuple(map(__import__("mpmath").mpf, _iv_bounds(t077_c)))
    t077_d_bounds = tuple(map(__import__("mpmath").mpf, _iv_bounds(t077_d)))
    assert t077_c_bounds[1] < t077_d_bounds[0]
    assert t080_c[0] > t080_d[1]


def test_all_five_programs_produce_valid_sets(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T080-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "9")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_BASELINE_ITERATIONS", "6")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_POPULATION", "2")
    from tasks.t080.init_program import run_code as initial
    from tasks.t080.baseline import run_code as baseline
    from tasks.t080.evolution import run_code as evolution
    from tasks.t080.human import run_code as human
    from tasks.t080.reference import run_code as reference

    outputs = [initial(), baseline(), evolution(), human(), reference()]
    results = [validate(output, CONFIG, strict=True) for output in outputs]
    assert results[0]["details"]["cardinality"] == 3
    assert 2 <= results[1]["details"]["cardinality"] <= 512
    assert 2 <= results[2]["details"]["cardinality"] <= 512
    assert results[3]["objective"] == results[4]["objective"]
    assert outputs[1]["search_metadata"]["iterations_run"] == 6
    assert outputs[2]["search_metadata"]["generations_run"] == 2


def test_cardinality_and_element_boundaries():
    assert validate({"set": [0, 2]}, CONFIG)["details"]["cardinality"] == 2
    max_element = validate({"set": [0, 1_000_000]}, CONFIG)
    assert max_element["details"]["q"] == 2_000_001
    boundary512 = [0, *range(1000, 1511)]
    result512 = validate({"set": boundary512}, CONFIG)
    assert result512["details"]["cardinality"] == 512
    assert result512["details"]["strict_difference_bound_verified"] is True


def test_checker_rejects_invalid_types_domain_and_strict_bound():
    for invalid in (True, 1.0, float("nan"), float("inf"), None, "3"):
        with pytest.raises(ValueError):
            validate({"set": [0, 1, invalid]}, CONFIG)
    with pytest.raises(ValueError, match="distinct"):
        validate({"set": [0, 1, 1]}, CONFIG)
    with pytest.raises(ValueError, match="2..512"):
        validate({"set": [0]}, CONFIG)
    with pytest.raises(ValueError, match="2..512"):
        validate({"set": [0, *range(1, 513)]}, CONFIG)
    with pytest.raises(ValueError, match="outside"):
        validate({"set": [0, -1]}, CONFIG)
    with pytest.raises(ValueError, match="outside"):
        validate({"set": [0, 1_000_001]}, CONFIG)
    with pytest.raises(ValueError, match="contain zero"):
        validate({"set": [1, 2, 4]}, CONFIG)
    # Here d=5 and q=5, so equality must fail the strict hypothesis.
    with pytest.raises(ValueError, match="strict finite-lemma condition"):
        validate({"set": [0, 1, 2]}, CONFIG)
    with pytest.raises(ValueError, match="configuration must fix"):
        validate({"set": [0, 1, 4]}, {"id": "T080-C01", "parameters": {**PARAMETERS, "max_cardinality": 511}})


def test_claimed_score_fields_do_not_change_validation_result():
    from tasks.t080.init_program import run_code

    candidate = run_code()
    expected = validate(candidate, CONFIG)
    for key, value in (("objective", -100), ("score", float("nan")), ("claimed_score", {"fake": True})):
        assert validate({**candidate, key: value}, CONFIG) == expected


def test_sota_records_and_frozen_interval():
    sota = json.loads((ROOT / "sota.json").read_text())
    records = json.loads((ROOT / "records.json").read_text())
    item = sota["configurations"]["T080-C01"]
    reference = json.loads((ROOT / "data/reference/gyarmati_hennecart_ruzsa_m6_l5.json").read_text())
    result = validate({"set": reference["set"]}, CONFIG)
    assert item["reproduced_value"] == result["objective"]
    assert item["best_reproduced"]["objective_interval"] == result["details"]["objective_interval"]
    assert records["configurations"]["T080-C01"]["frozen_human_baseline"]["value"] == result["objective"]


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T080 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T080 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
