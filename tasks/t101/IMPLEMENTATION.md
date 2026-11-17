# T101 implementation record

Status: accepted by Sol on 2026-11-09.

- Definition: maximize `point_count` for a subset of the 100 by 100 zero-based integer grid. Each triple of distinct points must have pairwise different squared side lengths. This forbids collinear midpoint triples too.
- Human method: replay the classical four-digit ternary no-three-term-progression construction on one row. Its 16 points are valid by the one-dimensional progression property. This is a weak baseline, not a best-human claim.
- Search baseline: seeded randomized greedy insertion, 4 fixed restarts by default. With seed 0 it returns 112 points. It does not read human or reference witness files.
- Public witness: the 164-point `sol_100` construction from the AlphaEvolve paper's linked official notebook, extracted from repository commit `8f447457957deac61e28bf1676746f0753b3b2f8`. The extracted file is hashed in `sota.json` and `records.json`.
- Checker: exact integer squared-distance uniqueness at each selected apex; this covers all triples, including collinear triples. The checker ignores claimed score fields.
- Exact independent audit of the public witness: 164 points, 26,732 apex-to-point distance checks; a separate triple checker is in `test_task.py`.

Validation run:

```sh
.venv/bin/python -m pytest tasks/t101 -q
.venv/bin/python -m json.tool tasks/t101/task.json >/dev/null
.venv/bin/python -m json.tool tasks/t101/sota.json >/dev/null
.venv/bin/python -m json.tool tasks/t101/records.json >/dev/null
```

Result: 11 tests passed; JSON checks passed. Tests cover human and public constructions, seed and search entry points, invalid isosceles triples, invalid types and coordinates, boundary cases, independent triple enumeration, and changed claimed scores. Runner subprocess success, nonzero exit, and timeout controls passed through `mathbench.evaluate._run`; full registry admission remains for Sol's review.

Source scope: checked the AlphaEvolve paper and official problem page, and used the linked repository notebook at the pinned commit for the actual coordinates. A public October 2026 issue reports a newer 58-point lower bound for the separate 32 by 32 instance; its table says the 100 by 100 value remains 164. No optimality proof was located in the checked sources. This source review is not exhaustive.
