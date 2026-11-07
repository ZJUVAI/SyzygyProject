"""Task-local tests for periodic length-64 binary autocorrelation energy."""

import copy
import json
import os
from pathlib import Path
import random
import sys
import time

import pytest

from tasks.t090 import baseline, check, evolution, human, init_program, reference
from tasks.t090.heuristics import correlations, energy, flip_deltas


TASK = Path(__file__).resolve().parent
CONFIG = json.loads((TASK / "task.json").read_text(encoding="utf-8"))["configurations"][0]


def test_all_program_entries_and_published_hex_reconstruction(monkeypatch):
    monkeypatch.setenv("T090_SEARCH_TRIALS", "1")
    monkeypatch.setenv("T090_ANNEAL_STEPS", "500")
    outputs = [
        init_program.run_code(),
        baseline.run_code(),
        human.run_code(),
        reference.run_code(),
        evolution.run_code(),
    ]
    values = [check.validate(item, CONFIG)["objective"] for item in outputs]
    assert values[0] == 258048
    assert values[2] == values[3] == 240
    assert check.validate(outputs[2], CONFIG)["details"]["peak_sidelobe_level"] == 4
    assert baseline.run_code()["search_metadata"]["reference_data_read"] is False
    assert evolution.run_code()["search_metadata"]["reference_data_read"] is False


def test_delta_update_matches_full_exact_recomputation():
    rng = random.Random(218)
    sequence = [rng.choice((-1, 1)) for _ in range(64)]
    corr = correlations(sequence)
    current_energy = energy(corr)
    for index in (0, 1, 31, 32, 63):
        deltas, delta_energy = flip_deltas(sequence, corr, index)
        changed = list(sequence)
        changed[index] *= -1
        changed_corr = correlations(changed)
        assert [corr[k] + deltas[k] for k in range(1, 64)] == changed_corr[1:]
        assert current_energy + delta_energy == energy(changed_corr)


def test_claim_fields_do_not_change_full_validation():
    witness = human.run_code()
    expected = check.validate(witness, CONFIG)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "0")):
        forged = copy.deepcopy(witness)
        forged[key] = value
        assert check.validate(forged, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


@pytest.mark.parametrize(
    "sequence",
    [
        [1] * 63,
        [0] + [1] * 63,
        [True] + [1] * 63,
        [1.0] + [1] * 63,
        [float("nan")] + [1] * 63,
        [float("inf")] + [1] * 63,
    ],
)
def test_invalid_sequences_are_rejected(sequence):
    with pytest.raises(ValueError):
        check.validate({"sequence": sequence}, CONFIG)


def test_fixed_config_is_required():
    with pytest.raises(ValueError):
        check.validate(init_program.run_code(), {**CONFIG, "id": "T090-C02"})
    with pytest.raises(ValueError):
        check.validate(
            init_program.run_code(),
            {**CONFIG, "parameters": {**CONFIG["parameters"], "length": 63}},
        )
    with pytest.raises(ValueError):
        check.validate(
            init_program.run_code(),
            {
                **CONFIG,
                "parameters": {**CONFIG["parameters"], "alphabet": [-1, True]},
            },
        )
    with pytest.raises(ValueError):
        check.validate(
            init_program.run_code(),
            {**CONFIG, "parameters": {**CONFIG["parameters"], "integer_domain": False}},
        )


def test_seeded_baseline_is_repeatable(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T090-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "5")
    monkeypatch.setenv("T090_SEARCH_TRIALS", "1")
    monkeypatch.setenv("T090_ANNEAL_STEPS", "500")
    first = baseline.run_code()
    second = baseline.run_code()
    assert first == second
    assert check.validate(first, CONFIG)["objective"] >= 1
    assert evolution.run_code() == first


def test_runner_errors_and_timeouts_without_registry_changes():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional failure')"], env, 5)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
    assert time.monotonic() - start < 3
