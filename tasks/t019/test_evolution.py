from tasks.t019.evolution import _primes, _missing, _interval_counts, _coordinate_update


def test_residue_incremental_counts_match_rebuild():
    primes = _primes(13)
    excluded = {p: 0 for p in primes}
    counts = _interval_counts(-3, 50, primes, excluded)
    for p in primes:
        _coordinate_update(-3, counts, 50, p, 0, 1)
        excluded[p] = 1
        assert counts == _interval_counts(-3, 50, primes, excluded)


def test_missing_rejects_duplicates():
    assert _missing([0]*343, _primes(343)) is None
    assert _missing([0]*1000, _primes(1000)) is None
