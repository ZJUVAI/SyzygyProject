from tasks.t058.evolution import _singer_ruler, _valid


def test_singer_cut_rulers_are_valid():
    ruler = _singer_ruler(29, 29)
    assert len(ruler) == 29
    assert ruler[0] == 0
    assert _valid(ruler)


def test_multi_mark_refill_keeps_exact_differences():
    import random
    import time
    from tasks.t058.evolution import _greedy, _rebuild
    ruler = _greedy(8)
    candidate = _rebuild(ruler, random.Random(10), time.monotonic() + 1)
    assert candidate is None or (len(candidate) == 8 and _valid(candidate) and candidate[-1] <= ruler[-1])
