import json
import math
import os
from pathlib import Path
import subprocess
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t057.baseline import run_code as baseline_run
from tasks.t057.check import CONFIG_ID, PARAMETERS, validate
from tasks.t057.evolution import run_code as evolution_run
from tasks.t057.human import run_code as human_run
from tasks.t057.init_program import run_code as init_run
from tasks.t057.instance import load_instance, rounded_euc_2d_distance, total_route_cost
from tasks.t057.io import read_solution
from tasks.t057.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _checked(routes):
    return validate({"routes": routes}, CONFIG)


def test_all_program_entries_and_simple_initial_solution(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("T057_SEARCH_TRIALS", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    initial = init_run()
    assert _checked(initial["routes"])["objective"] == total_route_cost(initial["routes"])
    assert len(initial["routes"]) == 1000
    human = human_run()
    reference = reference_run()
    baseline = baseline_run()
    evolved = evolution_run()
    for item in (human, reference, baseline, evolved):
        assert isinstance(item, dict)
        assert isinstance(item["routes"], list)
        _checked(item["routes"])
    assert _checked(human["routes"])["objective"] == 77398
    assert _checked(reference["routes"])["objective"] == 72332


@pytest.mark.parametrize(
    ("filename", "expected"),
    [("public_72332.sol", 72332), ("historical_72355.sol", 72355)],
)
def test_saved_official_witnesses(filename, expected):
    routes = read_solution(TASK / "data" / "reference" / filename)
    result = _checked(routes)
    assert result["objective"] == expected
    assert result["verification_status"] == "exact"
    assert len(routes) == 43
    assert max(result["details"]["route_loads"]) == 131


def test_human_witness_is_saved_and_exact():
    evidence = json.loads((TASK / "data/source/human_clarke_wright_77398.json").read_text())
    result = _checked(evidence["routes"])
    assert result["objective"] == evidence["verification"]["objective"] == 77398
    assert evidence["construction"]["method"] == "parallel Clarke-Wright savings"


def test_exact_distance_rounding_against_integer_definition():
    instance = load_instance()
    for left, right in ((1, 2), (2, 3), (17, 991), (1, 1001)):
        x1, y1 = instance["coordinates"][left]
        x2, y2 = instance["coordinates"][right]
        square = (x1 - x2) ** 2 + (y1 - y2) ** 2
        floor_root = math.isqrt(square)
        expected = floor_root + (1 if 4 * square >= (2 * floor_root + 1) ** 2 else 0)
        assert rounded_euc_2d_distance(left, right, instance) == expected


def test_route_count_is_not_limited_by_k43():
    routes = read_solution(TASK / "data/reference/public_72332.sol")
    first = routes.pop(0)
    routes.extend([[first[0]], first[1:]])
    result = _checked(routes)
    assert result["details"]["route_count"] == 44
    assert result["details"]["route_count_unrestricted"] is True


@pytest.mark.parametrize(
    "routes",
    [
        [],
        [[2]],  # missing customers
        [[2, 2]],  # duplicate
        [[True]],  # bool is not an integer node id
        [[2.0]],
        [[float("nan")]],
        [[1]],  # depot is not a customer
        [[1002]],
        [[]],
    ],
)
def test_invalid_routes_rejected(routes):
    with pytest.raises(ValueError):
        _checked(routes)


def test_capacity_violation_rejected():
    instance = load_instance()
    overloaded = []
    load = 0
    for customer in instance["customer_ids"]:
        if load > 131:
            break
        overloaded.append(customer)
        load += instance["demands"][customer]
    assert load > 131
    overloaded_set = set(overloaded)
    routes = [[node] for node in instance["customer_ids"]]
    routes = [route for route in routes if route[0] not in overloaded_set]
    routes.insert(0, overloaded)
    with pytest.raises(ValueError, match="exceeds capacity"):
        _checked(routes)


def test_claimed_objectives_never_change_validation():
    routes = read_solution(TASK / "data/reference/public_72332.sol")
    baseline = validate({"routes": routes}, CONFIG)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "999999999")):
        altered = validate({"routes": routes, key: value}, CONFIG)
        assert altered == baseline
    assert baseline["details"]["claimed_objective_ignored"] is True


def test_runner_error_and_timeout_without_task_registration():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional worker failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
