# T034 implementation record

Status: **已通过 Sol 验收（2026-11-06） / accepted by Sol on 2026-11-06**.

## Construction and sources

- `human.py` reconstructs the p=617 quadratic-residue coloring reported as the 2-color, length-7, 3703 lower bound by Herwig et al. (2007), Table 3. It independently uses the set of squares modulo 617; it does not call the checker.
- `reference.py` exposes that fixed reproduction. No saved public witness is needed because the historical method is a short formula.
- Monroe (2025), Tables 1 and 2, reports the same 3703 bound and the prime 617. The paper cites `hmonroe/vdw`; the main reviewer later pinned commit f1223097f4adc0a41ccb92ace51ebafd2b996fb1 and archived README/uc2.cpp without running the upstream distributed search.
- Campos, Fox, and Schildkraut (2026), arXiv:2608.20824, was checked for newer results. It gives a general asymptotic statement and does not report a stronger explicit k=7 witness.
- The full same-parameter check enumerates all starts and positive differences. A separate verification loop in `test_task.py` recomputes the condition independently.

## Programs

- `init_program.py` is self-contained and returns six entries of one color.
- `baseline.py` greedily extends from that short seed, chooses among legal colors with a saved random seed, and restarts at a dead end. It reads no reference assets.
- `evolution.py` exposes the baseline with a task-qualified import.
- `human.py` and `reference.py` are comparison programs only.

## Validation

Command: `.venv/bin/python -m pytest tasks/t034/test_task.py -q` — 9 passed in 5.19 seconds. The suite checks the full 3703 witness with an independent AP enumeration, a deliberately broken step-1 example, a broken step-2 example, score tampering, booleans, non-integers, NaN, infinity, bounds, seed, repeatability, timeout, and candidate errors. The checker rejects malformed color arrays and any monochromatic 7-term progression. Repeated color labels are valid by design.

Seed-0 traditional search produced length 241 after 20,000 permitted placements and 190 restarts. Its checker result was exact; a separate enumeration checked 4,720 progressions. Runtime was Python 3.13.12 on Linux, one thread. The saved task-owned result is in `best/T034-C01/`; replay with `MATHBENCH_SEED=0` and `baseline.py`. The required shared evaluator run is pending temporary admission by the main reviewer because T034 is not yet in the runner registry.

## Review limits

The source survey is not complete. The cited Monroe repository snapshot is pinned by the main reviewer. The construction is a lower-bound witness and gives no upper bound at 3704. Sol must independently replay the human program, review the source formulas, run a legal and broken example, and confirm score claims do not change the recomputed objective.
