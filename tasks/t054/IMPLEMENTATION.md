# T054 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Selected configuration and source check

- T054-C01 fixes a length-100 sequence over `{-1,+1}` and minimizes the largest magnitude among the 99 nonzero-shift aperiodic autocorrelations.
- Nunn and Coxson (2008), IEEE TAES 44(1), Table 2, gives the complete N=100 code `DF490FFB1F8390A54E3CD9AAE` and reports PSL 5. The witness was expanded to 100 bits and checked locally with exact integer arithmetic.
- The latest status source checked on 2026-11-06 is Brest et al., *Binary Sequences with Low Aperiodic Autocorrelations: Small Peak Sidelobe Levels*, version 2, posted 2026-07-28. Section 1 says exact minima are known for n<=61 and n=64, and directs readers to Nunn-Coxson for the reported values at 71<=n<=105. We treat N=100 PSL 5 as a best-known feasible value; the exact minimum is not proved by the checked sources.
- The witness JSON under `data/source/` and `data/reference/` has SHA-256 `0b3b9047edbb1a720ee1c2776ff9cba020a91f972bb965d10937be0ea3693648`.

## Difference from T013

The fixed length is the same as T013-C01, but the objective is different. At length 100, the T013 Dantus record has energy 578 and PSL 8. The Nunn-Coxson record has energy 874 and PSL 5. Both pairs were independently recomputed with exact integer sums. One sequence is better on energy and worse on PSL, so the objectives are not monotone transforms of one another.

## Programs and reproduced values

- `check.py` requires exactly 100 integer signs. It rejects booleans, floats, NaN, infinities, and values outside `{-1,+1}`. It recomputes all 99 sidelobes, returns their maximum absolute value, and ignores any declared score.
- `init_program.py` returns 100 positive signs, a valid seed with PSL 99.
- `baseline.py` uses fixed-seed single-bit-flip simulated annealing. It updates every affected autocorrelation with exact integer deltas and reads no comparison data. The default is 12 restarts of 3000 proposals each.
- `human.py` rebuilds the Nunn-Coxson hexadecimal witness. `reference.py` replays its frozen copy. Both outputs match and score PSL 5.
- Strict runner execution of `baseline.py`, seed 0, returned PSL 9. Generation took 4.408 s and verification took 0.799 s on Python 3.13.12/Linux. The runner enforced 300 s generation, 60 s verification, 4 GiB memory, and one thread. Artifacts are in `best/T054-C01/`; `result.json` SHA-256 `96fb20387004c2c9e4cb9c52ac5f1f63742ddd1568865016e9579d01a8afae7d` and `solution.json` SHA-256 `7ad92f3d7a6e2fd542d7e342c8fd5725c5942969fb311cd7b64bffe32e6a76ef`.

## Tests and commands

`test_task.py` tests the five `run_code()` entries, exact human witness score, simple-seed boundary, repeated signs, malformed lengths and values, fixed configuration types, forged score invariance, exact single-bit delta/rollback, and runner program-error and timeout handling through `mathbench.evaluate._run`.

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t054/test_task.py -q
.venv/bin/python -m json.tool tasks/t054/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t054/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t054/records.json > /dev/null
```

The strict baseline run used an in-process temporary configuration/path override for `evaluate_candidate`; no shared registry was changed. Generation and verification still ran in separate constrained workers.

## Limits

- PSL 5 is a feasible public result, not a proof of the exact minimum for length 100.
- The current survey lists reported values for this length range but does not give a nontrivial certified lower bound for this exact instance.
- Sol should replay the human record, verify the initial and search outputs, reject a damaged sign list, recompute the PSL, and confirm forged objective fields have no effect.

## Added configurations: accepted by Sol on 2026-11-07

- T054-C02 fixes length 101. The Table 2 heading is “Codes with PSL=5”; the row is `101 1A5048216CCF18F83E910DD4C5 7 [8]`. The trailing `7 [8]` is the comparison value and its citation, not the reported score. Exact integer recomputation of the decoded witness gives PSL 5.
- T054-C03 fixes length 102. The Table 2 row is `102 2945A4F11CE44FF664850D182A 7 [6]`; again, the trailing entry is the comparison value and its citation. Exact integer recomputation gives PSL 5.
- The source PDF is Nunn and Coxson, *Best-Known Autocorrelation Peak Sidelobe Levels for Binary Codes of Length 71 to 105*, IEEE TAES 44(1), 2008, DOI 10.1109/TAES.2008.4517015, Table 2. Source URL: https://www.norbertwiener.umd.edu/crowds/documents/best_known_binary.pdf. Source rows and hex strings are frozen in `data/source/`; the saved files have SHA-256 `7f7fc102e3976a0eb5c1dba1454c1b6c7ff48b1fb1fb5054c21879498d6ba953` (N=101) and `df23dfcbfd15a148f96fd50e3f62e63540910398127c37d1cd2afa28ccaf6b3a` (N=102).
- Brest et al., *Binary Sequences with Low Aperiodic Autocorrelations: Small Peak Sidelobe Levels*, v2 (posted 2026-07-28), §1 says exact minima are known for n<=61 and n=64 and reports larger lengths as best-known; it points to Nunn–Coxson for 71<=n<=105. This does not prove the minima at 101 or 102. The source is an unreviewed preprint.
- The checker selects the expected length from the registered config ID and recomputes every nonzero aperiodic correlation with exact integer sums. Tests independently decode both hex rows, verify all correlations, check all-positive boundary scores, reject malformed lengths, and verify the new human/reference entry points.
- C02 and C03 remain accepted by Sol on 2026-11-07. The existing C01 acceptance is unchanged.
