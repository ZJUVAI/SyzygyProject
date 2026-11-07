import copy
import os
import sys

import pytest

from tasks.t049.baseline import run_code as baseline_run
from tasks.t049.check import validate
from tasks.t049.evolution import run_code as evolution_run
from tasks.t049.human import run_code as human_run
from tasks.t049.init_program import run_code as seed_run
from tasks.t049.reference import run_code as reference_run


CONFIG = {
    "id": "T049-C01",
    "parameters": {
        "point_count": 91,
        "ambient_space": "Euclidean plane R^2",
        "coordinate_domain": "real algebraic coordinates in a common real algebraic number field",
    },
    "direction": "minimize",
    "human_reference": 34,
}


def test_human_and_reference_reconstruct_the_reported_91_point_witness():
    human = human_run()
    reference = reference_run()
    assert human == reference
    result = validate(human, CONFIG, strict=True)
    assert result["objective"] == 34
    assert result["verification_status"] == "exact"
    assert result["details"]["unordered_pair_count"] == 4095
    assert result["details"]["coordinate_field_degree"] == 2
    assert result["details"]["claimed_objective_ignored"] is True


def test_simple_seed_is_valid_and_has_90_exact_distances():
    seed = seed_run()
    result = validate(seed, CONFIG, strict=True)
    assert result["objective"] == 90
    assert result["details"]["coordinate_field_degree"] == 1


def test_exact_algebraic_distance_equality_and_embedding_isolation():
    witness = human_run()
    alternate_interval = copy.deepcopy(witness)
    alternate_interval["isolating_interval"] = ["3/2", "2"]
    assert validate(alternate_interval, CONFIG, strict=True)["objective"] == 34


@pytest.mark.parametrize(
    "mutate",
    [
        lambda s: s.update(minimal_polynomial=[-1, 0, 1]),
        lambda s: s.update(isolating_interval=["2", "3"]),
        lambda s: s.update(isolating_interval=["2", "1"]),
        lambda s: s.update(minimal_polynomial=[-3, 0, True]),
        lambda s: s["points"][0]["x"].__setitem__(0, 1.25),
        lambda s: s["points"][0]["y"].__setitem__(0, float("nan")),
        lambda s: s["points"].__setitem__(1, copy.deepcopy(s["points"][0])),
        lambda s: s["points"].pop(),
        lambda s: s["points"][0].update(z=[0]),
    ],
)
def test_invalid_algebraic_or_point_data_are_rejected(mutate):
    solution = human_run()
    mutate(solution)
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)


def test_bool_float_and_nonfinite_polynomial_data_are_rejected():
    for value in (True, 1.0, float("inf"), float("nan")):
        solution = human_run()
        solution["minimal_polynomial"][0] = value
        with pytest.raises(ValueError):
            validate(solution, CONFIG, strict=True)


def test_configuration_is_fixed():
    with pytest.raises(ValueError, match="91 distinct points"):
        validate(human_run(), {"parameters": {"point_count": 90}})


def test_forged_score_fields_do_not_change_full_validation_result():
    solution = human_run()
    base = validate(solution, CONFIG, strict=True)
    for key, value in (("objective", -500), ("score", "0"), ("claimed_score", 999999)):
        forged = {**solution, key: value}
        assert validate(forged, CONFIG, strict=True) == base
    assert base["details"]["claimed_objective_ignored"] is True


def test_search_is_seeded_bounded_and_reference_independent(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T049-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "2718")
    first = baseline_run()
    assert baseline_run() == first
    assert evolution_run() == first
    assert first["search_metadata"]["iteration_limit"] == 128
    assert first["search_metadata"]["iterations"] == 128
    assert first["search_metadata"]["reference_data_read"] is False
    assert 1 <= validate(first, CONFIG, strict=True)["objective"] <= 90


def test_zero_second_search_budget_keeps_simple_valid_seed(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    result = baseline_run()
    assert result["search_metadata"]["iterations"] == 0
    assert validate(result, CONFIG, strict=True)["objective"] == 90


def test_runner_reports_program_errors_and_timeouts():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
