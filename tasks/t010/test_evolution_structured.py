"""Distance and parity checks for puncturing the search space."""
import pytest
from tasks.t010 import evolution


def test_puncturing_distance_six_and_parity_extension():
    words = [0, 31 | (1 << 16), 31 << 5 | (1 << 16)]
    assert evolution._valid(words)
    projected = evolution._puncture(words)
    assert projected == [0, 31, 31 << 5]
    extended = [evolution._extend(word) for word in projected]
    assert evolution._valid(extended)
    assert all(word.bit_count() % 2 == 0 for word in extended)


def test_puncturing_rejects_collisions_and_distance_four():
    with pytest.raises(RuntimeError):
        evolution._puncture([0, 1 << 16])
    with pytest.raises(RuntimeError):
        evolution._puncture([0, 15])


def test_start_rejects_invalid_integer_words():
    assert not evolution._valid([])
    assert not evolution._valid([-1])
    assert not evolution._valid([1 << 17])
    assert not evolution._valid([True])
    assert not evolution._valid([[0] * 17])


def test_local_clique_returns_compatible_words():
    import time
    words = [0, 31, 31 << 5, 15, 30]
    found = evolution._local_clique(words, 3, time.monotonic() + 1)
    assert len(found) == 3
    assert all((a ^ b).bit_count() >= 5 for i, a in enumerate(found) for b in found[i + 1:])


def test_integer_kernel_cold_start_is_exact(monkeypatch):
    monkeypatch.delenv("MATHBENCH_WARM_START", raising=False)
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T010-C01")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_SECONDS", "3")
    monkeypatch.setenv("MATHBENCH_SEED", "20")
    from tasks.t010.check import validate
    result = evolution.run_code()
    config = {"parameters": {"n": 17, "distance": 6}}
    checked = validate(result, config, strict=True)
    assert checked["objective"] >= 128
    result["objective"] = 10**8
    assert validate(result, config, strict=True)["objective"] == checked["objective"]
    result["codewords"].append(result["codewords"][0] ^ 1)
    with pytest.raises(ValueError):
        validate(result, config, strict=True)
