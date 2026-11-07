import random
from tasks.t012.evolution import _counts, _incremental_measure, _measure, _proposal


def test_incremental_counts_equal_full_rebuild():
    rng = random.Random(10)
    current = [0, 2, 3, 4, 7, 11, 12, 14]
    for _ in range(100):
        sums, diffs = _counts(current)
        trial = _proposal(current, rng)
        score, ss, dd = _incremental_measure(current, trial, sums, diffs)
        assert (ss, dd) == _counts(trial)
        full = _measure(trial)
        assert score == (None if full is None else full[0])
        current = trial


def test_bit_support_score_matches_pairwise_sets():
    import math
    from tasks.t012.evolution import _bit_score
    rng = random.Random(60451)
    for count in (3, 8, 26, 80, 200):
        values = rng.sample(range(-150, 500), count)
        sums = {a+b for a in values for b in values}
        differences = {a-b for a in values for b in values}
        expected = math.log(len(sums)/count)/math.log(len(differences)/count)
        assert abs(_bit_score(values)-expected)<1e-14
