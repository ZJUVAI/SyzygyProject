"""Exact regression checks for the formula-generated BCH seed."""
from tasks.t009 import check, evolution


def test_bch_seed_has_rank_15_and_exact_distance_24():
    rows = evolution._bch_rows()
    assert all(((rows[i] >> j) & 1) == (i == j)
               for i in range(15) for j in range(15))
    matrix = [[(row >> col) & 1 for col in range(68)] for row in rows]
    result = check.validate({'generator_matrix': matrix, 'objective': 100},
                            {'id': 'T009-C01', 'parameters': {'n': 68, 'k': 15, 'q': 2}})
    assert result['objective'] == 24
    assert result['details']['codewords_checked'] == 32767
    assert result['details']['claimed_objective_ignored']
