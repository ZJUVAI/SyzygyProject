"""Iterated local search for binary A(17, 6), starting from an owned witness."""

import json
import os
import random
import time
import subprocess
import tempfile
from pathlib import Path

import numpy as np

N = 17
SEARCH_N = 16
UNIVERSE = 1 << SEARCH_N


def _valid(words):
    if not isinstance(words, list) or not words or any(type(w) is not int or not 0 <= w < (1 << N) for w in words):
        return False
    if len(words) != len(set(words)):
        return False
    return all((a ^ b).bit_count() >= 6
               for i, a in enumerate(words) for b in words[i + 1:])


def _read_start():
    path = os.environ.get("MATHBENCH_WARM_START")
    if path:
        with open(path, encoding="utf-8") as source:
            words = json.load(source)["codewords"]
    else:
        # Keep the public run_code() contract useful without runner-provided
        # warm starts. This is the task's deterministic traditional seed.
        try:
            from baseline import _start
        except ModuleNotFoundError:
            from tasks.t010.baseline import _start
        words = list(_start())
    if not isinstance(words, list) or not _valid(words):
        raise RuntimeError("warm start failed exact A(17, 6) validation")
    return words


def _conflict_masks():
    return [x for x in range(UNIVERSE) if x.bit_count() < 5]


def _extend(word):
    return word | ((word.bit_count() & 1) << SEARCH_N)


def _puncture(words):
    # Puncturing reduces distance by at most one. Adding parity raises every
    # odd distance by one, so every 16-bit distance-five code extends to six.
    projected = [word & (UNIVERSE - 1) for word in words]
    if len(projected) != len(set(projected)) or any(
            (a ^ b).bit_count() < 5 for i, a in enumerate(projected)
            for b in projected[i + 1:]):
        raise RuntimeError("punctured code failed exact distance-five validation")
    return projected


def _change_counts(counts, word, masks, delta):
    """Update exact counts of selected words within distance five."""
    for mask in masks:
        counts[word ^ mask] += delta


def _local_clique(vertices, target, deadline):
    """Find compatible words with exact bit sets and a coloring bound.

    The time limit can stop this local search. Every returned set is exact;
    failure to find a larger set does not prove local optimality.
    """
    size = len(vertices)
    adjacent = [0] * size
    for i, a in enumerate(vertices):
        for j in range(i):
            if (a ^ vertices[j]).bit_count() >= 5:
                adjacent[i] |= 1 << j
                adjacent[j] |= 1 << i
    best = []
    nodes = 0

    def expand(chosen, available):
        nonlocal best, nodes
        nodes += 1
        if nodes % 64 == 0 and time.monotonic() >= deadline:
            return
        if len(chosen) > len(best):
            best = chosen[:]
        if len(best) >= target:
            return
        # Greedy coloring of the compatibility graph bounds clique size.
        order, bounds = [], []
        remaining, color = available, 0
        while remaining:
            color += 1
            independent = remaining
            while independent:
                bit = independent & -independent
                v = bit.bit_length() - 1
                order.append(v)
                bounds.append(color)
                remaining ^= bit
                independent &= ~bit & ~adjacent[v]
        for v, bound in zip(reversed(order), reversed(bounds)):
            if len(chosen) + bound <= len(best):
                return
            if time.monotonic() >= deadline or len(best) >= target:
                return
            expand(chosen + [v], available & adjacent[v])
            available &= ~(1 << v)

    expand([], (1 << size) - 1)
    return [vertices[i] for i in best]


def run_code():
    """Run the single-thread integer kernel using only the supplied start."""
    config_id=os.environ.get("MATHBENCH_CONFIG_ID", "T010-C01")
    if config_id in ("T010-C02", "T010-C03"):
        # The available compiled kernel is specific to the C01 puncturing
        # scheme. For these larger instances, use the same fixed-budget
        # add-only search as the traditional baseline.
        try:
            from baseline import run_code as baseline_run
        except ModuleNotFoundError:
            from tasks.t010.baseline import run_code as baseline_run
        result=baseline_run()
        result["search_method"]="configuration_safe_add_only_greedy"
        return result
    if config_id != "T010-C01": raise ValueError("unsupported configuration")
    started = time.monotonic()
    best = _read_start()
    projected = _puncture(best)
    try:
        budget = max(0.0, min(255.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    except (TypeError, ValueError):
        budget = 45.0
    if budget == 0:
        return {"codewords": best, "search_method": "exact_start_only",
                "search_start_size": len(best), "search_final_size": len(best)}
    seed = int(os.environ.get("MATHBENCH_SEED", "0")) % (1 << 32)
    source = Path(__file__).with_name("search_kernel.cpp")
    with tempfile.TemporaryDirectory(prefix="t010_kernel_") as temporary:
        executable = Path(temporary) / "search_kernel"
        subprocess.run(["g++", "-O3", "-std=c++17", str(source), "-o", str(executable)],
                       check=True, capture_output=True, text=True, timeout=35)
        remaining = max(0.0, budget - (time.monotonic() - started))
        payload = f"{seed} {remaining:.6f} {len(projected)}\n" + " ".join(map(str, projected)) + "\n"
        result = subprocess.run([str(executable)], input=payload, capture_output=True,
                                text=True, check=True, timeout=remaining + 10)
    header, raw = result.stdout.strip().split("\n")
    size, moves, cavities, improvements = map(int, header.split())
    candidate = [_extend(word) for word in map(int, raw.split())]
    if len(candidate) != size or not _valid(candidate):
        raise RuntimeError("kernel result failed exact A(17, 6) validation")
    if len(candidate) > len(best):
        best = candidate
    return {"codewords": best,
            "search_method": "integer_multibit_switch_tabu_Hamming_ball_coloring_cavity",
            "search_iterations": moves + cavities, "search_tabu_moves": moves,
            "search_cavities": cavities, "search_improvements": improvements,
            "search_start_size": len(projected), "search_final_size": len(best),
            "search_kernel_log": result.stderr.strip()}
