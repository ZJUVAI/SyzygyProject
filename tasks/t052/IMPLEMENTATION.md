# T052 implementation evidence

Status: accepted by Sol on 2026-11-06.

## Definition and source checks

- `T052-C01` fixes length `n=12`, alphabet `{0,...,11}`, minimum Hamming distance `d=9`, and maximizes code size `M(12,9)`. Every word is a permutation. The exact checker checks all rows and all row pairs.
- Smith and Montemanni, *A New Table of Permutation Codes*, Designs, Codes and Cryptography 63 (2012), Table 3 and §4 item 22, reports `M(12,9) >= 1320` and `M(12,9) <= 11880`. It describes the PGL(2,11) orbit and internal minimum distance 10. DOI: <https://doi.org/10.1007/s10623-011-9551-8>.
- The source's `n=12,d=10` entry equals 1320 at the upper bound and is a separate solved case. This task uses `d=9`; it remains open in the sources checked.
- The 2025 Bereg, Malouf, Morales, and Sudborough article, *Efficient Algorithms for Permutation Arrays from Permutation Polynomials*, Entropy 27(10), article 1031, DOI <https://doi.org/10.3390/e27101031>, was checked. Its §5 result tables list no `(12,9)` entry. The article reports some other lower-bound improvements.
- The current UTD permutation-array index is <https://personal.utdallas.edu/~sxb027100/soft/permutation-arrays/>. Search could find the index, while direct retrieval of the general table returned HTTP 403. Its reachable `n-1` and `n-2` tables do not include `(12,9)`. The survey date is 2026-11-06. The highest same-parameter report located is 1320; this survey is not an exhaustive review of all publications.
- The 11880 upper bound is the value printed in the checked 2012 table. It is retained as a historical published bound, not claimed as the best bound currently known.

## Reproduced human and public construction

- The point set is `F_11 ∪ {∞}`, encoded as `0,...,10,11`. Each projective matrix `[[a,b],[c,d]]` with nonzero determinant is normalized so that its first nonzero row-major entry is 1. This gives one representative for each scalar class in `PGL(2,11)`.
- For finite `x`, the action is `(a*x+b)/(c*x+d)` in `F_11`; a zero denominator maps to infinity. Infinity maps to infinity when `c=0`, and to `a/c` otherwise. The action produces 1320 distinct permutations.
- `human.py` generates these permutations from the formula. `data/reference/pgl_2_11_n12_d9.json` stores the full reproducible output. SHA-256: `f33140d3e4278b1ad4adcc43dbd0823c1e453ff6c97d47e6fb91e17ecb02fb06`.
- The checker validates every row and all `1320*1319/2 = 870540` pairs. The recomputed minimum distance is 10, so the construction is valid for the required distance 9.
- A separate timed verification of the frozen 1320-word reference took `1.9066 s` in the local Python 3.13.12 environment, below the 60-second verification limit.
- The 2012 source predates modern LLM-based generative AI and reports no AI contribution. No AI-assisted or provenance-undisclosed same-parameter record was located in the checked sources.

## Programs, search, and saved result

- `check.py` rejects wrong lengths, non-permutation rows, duplicate rows, booleans, floats, NaN, unsupported parameters, and any pair at distance below 9. It computes code size from the supplied rows and ignores `objective`, `score`, and `claimed_score` fields.
- `init_program.py` returns the 12 cyclic shifts of the identity permutation. Distinct cyclic shifts disagree in all 12 positions, so this is a valid 12-word seed.
- `baseline.py` uses fixed-seed random greedy packing with independent restarts. `evolution.py` runs bounded randomized greedy batches and retains the largest batch. Neither reads the human or reference witness.
- `human.py` generates the classical group construction. `reference.py` loads the task-local frozen witness. These are comparison programs, not model starting programs.
- A replayable search run used Python `3.13.12` on Linux, seed `17`, four generations, 200 candidates per generation, with no wall-clock cutoff. The run took `0.1754 s` and produced 87 words; exact validation recomputed minimum distance 9 and checked all 3741 pairs. The result and replay command are saved in `best/T052-C01/evolution_seed17.json`. Replay:

  ```sh
  MATHBENCH_CONFIG_ID=T052-C01 MATHBENCH_SEED=17 MATHBENCH_SEARCH_ITERATIONS=4 T052_CANDIDATES_PER_GENERATION=200 .venv/bin/python -m tasks.t052.evolution
  ```

- Search defaults use fixed iteration counts. The runner defaults are generation 300 seconds, verification 60 seconds, memory 4 GiB, and one compute thread. Explicit `MATHBENCH_SEARCH_SECONDS` enables a machine-dependent cutoff. The recorded 87-word result is only this task's own search result; it is not a public record.

## Validation performed

From the repository root:

```sh
.venv/bin/python -m pytest tasks/t052/test_task.py -q
.venv/bin/python -m json.tool tasks/t052/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t052/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t052/records.json > /dev/null
```

The task-local suite passed: `5 passed in 32.76s`. It checks both PGL generators, the witness hash, all 870540 reference pairs, an independent size/distance recount, an accepted 12-word construction, a deliberately broken distance-8 pair, repeated rows, invalid symbols and numeric types, score-field tampering, all five `run_code()` entries, and runner error and timeout handling through `mathbench.evaluate._run`.

## Review limits

- The construction is an exact lower-bound witness, not an optimality proof.
- The current best public upper bound could be stronger than 11880; the current author index's general table was not directly accessible.
- The 1320 value is the highest same-parameter report found in the sources checked on 2026-11-06, not a claim that every paper or data set has been surveyed.
