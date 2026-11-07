# T037 implementation record

Status: `accepted_by_sol`.

The verifier parses integer and rational-string coordinates as exact fractions. It rejects floats, booleans, zero directions, malformed vectors, and any pair below 60 degrees. It recomputes the cardinality and ignores submitted scores. The test suite checks the 40-point D5 witness, the 10-point seed, a strict angle violation, the exact 60-degree boundary, proportional duplicate directions, invalid numeric values, configuration mismatch, score tampering, and shared-runner program-error and timeout controls.

The human witness is generated from the Korkine–Zolotareff D5 root description. Its 40 squared norms are 2, its 780 pairs meet the exact angle bound, and the verifier independently returns 40. Witness SHA-256: `f5ac23ea0d52d6ec38f73792424fefea1eff30b664bf531b459a3a6ec49cc807`. The literature upper bound 44 was not reproduced. A web search on 2026-11-06 found no unrestricted optimality proof after the cited 2026 paper; finite-alphabet ternary results are kept separate.

Commands and results:

- `.venv/bin/python -m pytest tasks/t037 -q` — 15 passed.
- `.venv/bin/python -m pytest tasks/t037 -q` after runner-control coverage — 16 passed.
- `.venv/bin/python -m pytest tests tasks -q` — 450 passed, 32 subtests passed.
- `.venv/bin/python -m json.tool tasks/t037/task.json`, `records.json`, and `sota.json` — passed.
- Human construction replay — 40 directions, 780 exact pair checks.
- Traditional greedy baseline replay, seed 0 — 11 directions, 121 ternary candidates checked.
- Evolution entry replay, seed 0 and 200 iterations — 18 directions, 8 accepted additions; checker passed.
- Own search construction and exact result are saved under `best/T037-C01/`; provenance marks Sol review and formal runner admission pending.

Search uses fixed seed 0 and 200 default integer-direction proposals. The baseline uses a fixed shuffled greedy pass over nonzero ternary directions modulo antipodes. Neither program reads the saved human witness. Runner defaults are generation 300 seconds, verification 60 seconds, 4 GiB and one CPU thread. Candidate directions are rational-coordinate certificates; the search space is not asserted to cover all real configurations. Task metadata records the seed and iteration count; exact replay command is recorded in `records.json`.
