"""Exact count and interval tests for T077-C01."""

import hashlib
import json
import math
import os
from math import comb
from pathlib import Path
import sys

import pytest

from tasks.t077.check import PARAMETERS, validate
from tasks.t077.construction import projected_simplex


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T077-C01", "parameters": PARAMETERS}
WITNESS_SHA256 = "0a2b6d7e40a16688d66f6c5e4ad322edb5f7fa38b6015dc4c9a4ce475bc873c4"
BEST_WITNESS_SHA256 = "916221446c05549172b608ad38361ee4008e9b4a5a9516cced3eace4ffbbfa8b"
REVERSAL_SHA256 = "5175a59efe1c75781c6f6b96e3ef748e998e81c05512b5e2e322711e42d430d9"


def _counts(values):
    sums = {a + b for a in values for b in values}
    differences = {a - b for a in values for b in values}
    return len(sums), len(differences)


def _interval_bounds(interval):
    import mpmath as mp
    def endpoint(text):
        return mp.mpf(text)
    return endpoint(interval[0]), endpoint(interval[1])


def _iv_bounds(value):
    def low(endpoint):
        return str(endpoint).strip().strip("[]").split(",", 1)[0].strip()
    def high(endpoint):
        return str(endpoint).strip().strip("[]").split(",", 1)[-1].strip()
    return low(value.a), high(value.b)


def test_published_projection_formula_and_saved_witness_match():
    witness_path = ROOT / "data/reference/gyarmati_hennecart_ruzsa_m6_l5.json"
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == WITNESS_SHA256
    saved = json.loads(witness_path.read_text(encoding="utf-8"))
    projected, weights = projected_simplex(6, 5)
    assert weights == [1, 11, 111, 1111, 11111, 111111]
    assert projected == saved["set"]
    assert len(projected) == comb(11, 6) == 462
    assert max(projected) == 555555
    sums, differences = _counts(projected)
    formula_difference_size = sum(comb(6, k) ** 2 * comb(11-k, 6) for k in range(7))
    assert sums == comb(16, 6) == 8008
    assert differences == formula_difference_size == 39733

    stronger_path = ROOT / "data/reference/gyarmati_hennecart_ruzsa_m7_l4_shifted.json"
    assert hashlib.sha256(stronger_path.read_bytes()).hexdigest() == BEST_WITNESS_SHA256
    stronger = json.loads(stronger_path.read_text(encoding="utf-8"))
    raw_m7, weights_m7 = projected_simplex(7, 4)
    assert weights_m7 == [1, 9, 73, 585, 4681, 37449, 299593]
    assert stronger["set"] == [x - 599186 for x in raw_m7]
    assert (len(raw_m7), min(stronger["set"]), max(stronger["set"])) == (330, -599186, 599186)
    m7_sums, m7_differences = _counts(stronger["set"])
    m7_formula_difference_size = sum(comb(7, k) ** 2 * comb(11-k, 7) for k in range(8))
    assert m7_sums == comb(15, 7) == 6435
    assert m7_differences == m7_formula_difference_size == 33111


def test_human_reference_and_exact_set_counts_replay():
    from tasks.t077.human import run_code as human_run
    from tasks.t077.reference import run_code as reference_run

    human = human_run()
    reference = reference_run()
    assert human != reference
    human_counts = _counts(human["set"])
    assert (len(human["set"]), *human_counts) == (462, 8008, 39733)
    human_checked = validate(human, CONFIG, strict=True)
    assert human_checked["verification_status"] == "certified"
    assert human_checked["details"]["sumset_size"] == 8008
    assert human_checked["details"]["difference_set_size"] == 39733

    sum_size, difference_size = _counts(reference["set"])
    assert (len(reference["set"]), min(reference["set"]), max(reference["set"]), sum_size, difference_size) == (330, -599186, 599186, 6435, 33111)
    checked = validate(reference, CONFIG, strict=True)
    assert checked["verification_status"] == "certified"
    assert checked["details"]["objective_interval"][0] == checked["objective"]
    assert checked["details"]["sumset_size"] == 6435
    assert checked["details"]["difference_set_size"] == 33111

    import mpmath as mp
    mp.mp.dps = 100
    lower, upper = _interval_bounds(checked["details"]["objective_interval"])
    point_value = mp.log(33111) / mp.log(6435)
    assert lower <= point_value <= upper


def test_t012_and_t077_are_not_order_equivalent():
    source_path = ROOT / "data/source/t012_order_reversal_examples.json"
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == REVERSAL_SHA256
    examples = json.loads(source_path.read_text(encoding="utf-8"))
    A = examples["A"]
    B = examples["B"]
    assert len(B) == 16 and set(B) == set(A) | {x + 1000 for x in A}
    counts = [_counts(values) for values in (A, B)]
    assert [len(A), len(B)] == [8, 16]
    assert counts == [(26, 25), (78, 75)]
    assert all(sum_size > difference_size > len(values)
               for values, (sum_size, difference_size) in zip((A, B), counts))
    assert all(len(values) <= 512 and min(values) >= -1_000_000 and max(values) <= 1_000_000
               for values in (A, B))

    from mpmath import iv
    iv.dps = 70
    t012_scores = [iv.ln(iv.mpf(s) / n) / iv.ln(iv.mpf(d) / n)
                   for (n, (s, d)) in zip((len(A), len(B)), counts)]
    t077_scores = [iv.ln(iv.mpf(d)) / iv.ln(iv.mpf(s)) for s, d in counts]
    t012_a, t012_b = (tuple(map(__import__("mpmath").mpf, _iv_bounds(value))) for value in t012_scores)
    t077_a, t077_b = (tuple(map(__import__("mpmath").mpf, _iv_bounds(value))) for value in t077_scores)
    assert t012_a[0] > t012_b[1]
    assert t077_a[1] < t077_b[0]


def test_all_five_program_entries_return_valid_sets(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T077-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "7")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_BASELINE_ITERATIONS", "6")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_POPULATION", "2")
    from tasks.t077.init_program import run_code as initial
    from tasks.t077.baseline import run_code as baseline
    from tasks.t077.evolution import run_code as evolution
    from tasks.t077.human import run_code as human
    from tasks.t077.reference import run_code as reference

    outputs = [initial(), baseline(), evolution(), human(), reference()]
    results = [validate(output, CONFIG, strict=True) for output in outputs]
    assert results[0]["details"]["cardinality"] == 3
    assert results[1]["details"]["cardinality"] in range(2, 513)
    assert results[2]["details"]["cardinality"] in range(2, 513)
    assert results[3]["details"]["sumset_size"] == 8008
    assert results[3]["details"]["difference_set_size"] == 39733
    assert results[4]["details"]["sumset_size"] == 6435
    assert results[4]["details"]["difference_set_size"] == 33111
    assert float(results[4]["objective"]) > float(results[3]["objective"])
    assert outputs[1]["search_metadata"]["iterations_run"] == 6
    assert outputs[2]["search_metadata"]["generations_run"] == 2


def test_checker_accepts_config_boundaries_and_rejects_invalid_sets():
    assert validate({"set": [-1_000_000, 1_000_000]}, CONFIG)["details"]["cardinality"] == 2
    boundary512 = list(range(512))
    check512 = validate({"set": boundary512}, CONFIG)
    assert check512["details"]["cardinality"] == 512
    assert check512["details"]["sumset_size"] == 1023
    assert check512["details"]["difference_set_size"] == 1023

    for invalid in (True, 1.0, float("nan"), float("inf"), None, "2"):
        with pytest.raises(ValueError):
            validate({"set": [0, 1, invalid]}, CONFIG)
    with pytest.raises(ValueError, match="distinct"):
        validate({"set": [1, 1]}, CONFIG)
    with pytest.raises(ValueError, match="2..512"):
        validate({"set": [1]}, CONFIG)
    with pytest.raises(ValueError, match="2..512"):
        validate({"set": list(range(513))}, CONFIG)
    for out_of_range in (-1_000_001, 1_000_001):
        with pytest.raises(ValueError, match="outside"):
            validate({"set": [0, out_of_range]}, CONFIG)
    with pytest.raises(ValueError, match="configuration must fix"):
        validate({"set": [0, 1, 3]}, {"id": "T077-C01", "parameters": {**PARAMETERS, "max_cardinality": 511}})


def test_claimed_scores_do_not_change_full_validation_result():
    from tasks.t077.init_program import run_code

    candidate = run_code()
    expected = validate(candidate, CONFIG)
    for key, value in (("objective", -1000), ("score", float("nan")), ("claimed_score", {"fake": 1})):
        assert validate({**candidate, key: value}, CONFIG) == expected


def test_record_schema_and_frozen_interval():
    sota = json.loads((ROOT / "sota.json").read_text())
    records = json.loads((ROOT / "records.json").read_text())
    result = validate({"set": json.loads((ROOT / "data/reference/gyarmati_hennecart_ruzsa_m7_l4_shifted.json").read_text())["set"]}, CONFIG)
    entry = sota["configurations"]["T077-C01"]
    assert entry["reproduced_value"] == result["objective"]
    assert entry["public_value"] == result["objective"]
    assert entry["best_reproduced"]["objective_interval"] == result["details"]["objective_interval"]
    assert "m=6,L=5" in records["configurations"]["T077-C01"]["frozen_human_baseline"]["endpoint_policy"]


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T077 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T077 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
