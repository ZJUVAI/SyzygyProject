# T039 implementation record

## Delivered

Configuration `T039-C01` implements an `(n,k)=(7,5)` difference triangle set: seven rows, six distinct nonnegative integer marks per row. The exact checker evaluates the 105 positive within-row differences and minimizes the largest row span. Shared marks in separate rows are allowed.

The published 112 construction, its pinned repository archive, and Shearer's lower-bound paper are stored in `data/` with source SHA-256 values. `human.py` and `reference.py` replay the published witness. `init_program.py` provides a self-contained powers-of-three seed. `baseline.py` starts from that seed and runs 100 seeded greedy attempts without reading comparison data. `evolution.py` exports the shared search entry point.

## Evidence and source limits

The primary article defines `(n,k)` with `k+1` marks per row and reports 112 as an upper bound for `(7,5)`, with 113 as the previous value. The authors attribute the method to FPGA search. The article does not disclose AI provenance.

The GitHub main branch was checked on 2026-11-06. Its HEAD was `2ccff8e767c3fe6390fd3af056dfda11847011fc`, matching the pinned commit. Its FPGA search archive has one `(7,5)` row, `7-5-112-755.txt`. This is a check of that archive only; it does not prove that no better construction exists elsewhere.

Shearer's lower bound is `(91I+6)/6`. At `I=7`, `643/6 = 107 + 1/6`, so the integer lower bound is 108. The 108–112 interval contains five possible integer values. The selected record is not established as optimal.

The 112 witness SHA-256 is `9ad412af0b33d51190956b866398bfdd42e6a6e0a894e59f531d28be949e4d1f`. The checker independently recomputed all 105 differences and the value 112. The local traditional search ran 100 iterations with seed 0 and returned a valid value of 243. Runtime and replay details are in `runs/validation_20261106.json`; the local search witness is in `best/traditional_search_seed0.json`.

## Validation

Command: `.venv/bin/python -m pytest tasks/t039 -q`

Result: 18 passed. Tests cover the published witness, simple seed, search entries, exact objective recomputation, repeated differences, legal repeated marks across rows, malformed row sizes, bool and float marks, non-finite marks, negative marks, claimed-score tampering, deterministic seed behavior, program errors, and generation timeouts.

JSON validation: `python3 -m json.tool` was run on `task.json`, `records.json`, and `sota.json`.

## Status

**Pending Sol review.** Sol should independently recheck the primary article's table and appendix, replay the human/reference witness, inspect the simple seed and traditional search, and run an independent legal and deliberately invalid case before admission.
