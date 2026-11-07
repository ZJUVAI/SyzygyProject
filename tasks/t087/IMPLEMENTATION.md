# T087 implementation and validation

Status: **accepted by Sol on 2026-11-06**.

## Fixed mathematical model

The configuration fixes 480 nonnegative rational heights on cells of width `13/4800` and support length `13/10`. It maximizes the minimum autocorrelation on all shifts in `[0,1]`, divided by squared L1 mass. For a cell-step function, autocorrelation is linear between multiples of the cell width. Since `1/d=369+3/13`, the checker takes the exact minimum over the 370 nodes `k*d` for `k=0,...,369` and the exact interpolation at `t=1`. This is a whole-interval certificate.

The checker accepts exact integers, rational strings, and finite floats interpreted as their exact binary rationals. It rejects negative heights, zero mass, wrong vector length, nonfinite values, and changed configurations. It ignores reported scores.

## Source review and baseline status

Barnard and Steinerberger, arXiv:1903.08731v2 (19 February 2020), define the underlying continuous problem, give bounds `>0.37` and `≤0.411`, and describe the modified-arcsine construction. The frozen human method reconstruction samples the formula at cell centers and rounds to denominator 100,000. Its exact score is `15833948850637600/43788391811747427` (about `0.361601515732983`). This is a local finite-grid reconstruction, not a score reported in the paper.

The public exact certificate is Kevin Russell / ProjectForty2's CHRONOS-assisted construction. Its repository was pinned to current main commit `b23f2d386eda9963e33c7531eeeb35c8f54cba37`, checked on 2026-11-06. The certificate SHA-256 is `11cc0e743163a1e7f4f3b86bdf1f15c2cfd5fc099db3a323d2ea396b9d28d1fa`. The upstream README and license are saved in `data/source/`. Exact recomputation returns `2378625/5958277`; minimum autocorrelation is `82459/13824000`, and L1 mass is `8801/72000`.

Latest-source check found Chen and Gu, arXiv:2610.18888v1, submitted 2026-10-08. It proves a stronger lower bound `C≥0.410377977432121...` for the unrestricted continuous constant. Its construction uses an atomic-polynomial profile and an atom-removal argument. The paper does not give the fixed 480-cell vector used here, so that continuous result is tracked separately and is not used as this configuration's score. The note also does not claim an optimum. The 480-height finite-dimensional optimum remains unknown in sources checked through 2026-11-06.

## Program separation and local run

- The initial program returns 480 unit heights.
- The baseline starts from those heights and makes 400 seeded block mutations. It uses NumPy only for search feedback. The checker recomputes the final score exactly.
- Evolution runs 1,400 seeded block mutations from the same simple starting vector. It reads no comparison witness.
- The human program reconstructs the modified-arcsine formula without loading reference data.
- The reference program loads only the pinned public certificate from `data/reference/`.

With seed 0, the 400-step baseline scored `40960/135759` (about `0.30171112`). The 1,400-step evolution scored `3345600/10694437` (about `0.31283554`). The evolution result is saved in `best/seed-0.json`, with the environment and shared limits. Both local results are below the frozen human method reconstruction.

## Validation

On Python 3.13.12/Linux, run:

```sh
.venv/bin/python -m pytest tasks/t087/test_task.py -q
.venv/bin/python -m json.tool tasks/t087/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t087/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t087/records.json > /dev/null
git diff --check -- tasks/t087
```

The test command passed all 20 tests in 9.70 seconds on Python 3.13.12/Linux. The tests cover the human and AI witnesses, initial and search entries, exact source score and mass, the `t=1` interpolation using the uniform profile, rational and float inputs, invalid data and altered configurations, claim-score invariance, and `_run` error and timeout controls. All three JSON files parsed, and `git diff --check -- tasks/t087` passed.

Shared limits are 300 seconds for generation, 60 seconds for verification, 4 GiB memory, one thread, and 16 MiB output. Search iteration counts are fixed. No global optimum is known from sources checked.
