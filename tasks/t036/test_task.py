import pytest

from tasks.t036.check import _orientation, validate
from tasks.t036.human import run_code as human_run_code

CONFIG = {
    "id": "T036-C01",
    "parameters": {
        "vertices": 28,
        "graph": "complete graph K28",
        "general_position": "no three points collinear",
        "crossing_definition": "unordered pairs of disjoint straight edges whose relative interiors intersect",
    },
}


def parabola():
    return {"points": [[i, i * i] for i in range(28)]}


def test_convex_reference_and_claimed_score_ignored():
    candidate = human_run_code()
    checked = validate(candidate, CONFIG)
    assert checked["objective"] == 20475
    assert checked["details"]["general_position_triples_checked"] == 3276
    assert checked["details"]["disjoint_edge_pairings_checked"] == 61425
    candidate["claimed_objective"] = -999
    candidate["score"] = float("nan")
    assert validate(candidate, CONFIG)["objective"] == 20475


def test_exact_orientation_boundary_values():
    assert _orientation((0, 0), (2, 0), (1, 1)) == 2
    assert _orientation((0, 0), (2, 0), (1, -1)) == -2
    assert _orientation((0, 0), (2, 0), (1, 0)) == 0


def test_rejects_collinear_and_duplicate_points():
    candidate = parabola()
    candidate["points"][2] = [2, 2]
    with pytest.raises(ValueError, match="collinear"):
        validate(candidate, CONFIG)
    candidate = parabola()
    candidate["points"][1] = candidate["points"][0]
    with pytest.raises(ValueError, match="distinct"):
        validate(candidate, CONFIG)


@pytest.mark.parametrize("bad_coordinate", [True, 1.25, float("nan"), float("inf"), "2/4", "1/0"])
def test_rejects_invalid_coordinate_values(bad_coordinate):
    candidate = parabola()
    candidate["points"][0][0] = bad_coordinate
    with pytest.raises(ValueError):
        validate(candidate, CONFIG)


def test_accepts_exact_rational_coordinates():
    candidate = parabola()
    candidate["points"][0] = ["1/3", "1/7"]
    assert validate(candidate, CONFIG)["verification_status"] == "exact"


def test_rejects_wrong_size_or_configuration():
    candidate = parabola()
    candidate["points"].pop()
    with pytest.raises(ValueError, match="exactly 28"):
        validate(candidate, CONFIG)
    with pytest.raises(ValueError, match="configuration"):
        validate(parabola(), {"id": "T036-C02", "parameters": CONFIG["parameters"]})
