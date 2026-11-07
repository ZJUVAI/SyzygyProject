# T093 implementation record

Status: `accepted_by_sol`.

## Frozen data and source review

- Input: `data/source/random_cf2_74ae2d30_50.cgshop2024_instance.json`.
- Input SHA-256: `f2ad180face7d410ec40cf531d8bbf4a5631a9a6c18f9d7a73579717abca9c92`.
- It contains one 15-vertex container, 44 item types, and `sum(quantity)=50`. The exact source-value coordinates and translations are integers. The container turn check has no nonpositive turns; its polygon is convex.
- Public solution: `data/source/shadoks2304.json`, SHA-256 `f6cd869b458df294ec49dd36a73a805f6ec4acda184c935b17d98b3c23830cc1`. `data/source/shadoks2304.json` is an identical frozen copy. These are comparison assets and must not be exported with the cold initial program.
- The official CG:SHOP page states the packing objective and forbids rotation. The Shadoks paper says the task uses translations and describes integer programming and heuristic search. Its public instance page names Shadoks as the best team for this instance. The solution page lists 2304, 2268, and 2105. The exact 2304 solution JSON is replayed and validated here.
- The source file metadata says “before digopt optimization.” The source does not disclose whether AI tools were used. The record keeps this uncertainty.
- Source check on 2026-11-06 did not find an optimality proof for this fixed instance. This is a limited source check, not an exhaustive survey.

## Geometry checker

`check.py` uses only Python standard-library integer and `Fraction` arithmetic. `instance.py` verifies the frozen file hash, source structure, exact item counts, and polygon triangulations. Ear clipping returns CCW triangles and checks that triangle areas sum to each source polygon's area.

For each translated item, the checker clips its triangles against every container triangle. Exact intersection areas must sum to the item area. For each pair of items, it checks all triangle pairs and rejects any positive intersection area. This proves containment and pairwise interior disjointness, including concave polygons and boundary contact. The selected-value sum is recomputed from the fixed item definitions. Claimed score fields are ignored.

The checker accepts zero selected items. It rejects noninteger or Boolean indices/translations, mismatched arrays, more than 50 placements, invalid type IDs, multiplicity overflow, placements outside the container, and positive-area overlap.

## Programs and saved run

- `init_program.py`: standalone empty packing, value 0; no imports from the task package.
- `baseline.py`: value-density order and random integer first-fit placements, checked by the exact geometry kernel. It reads only the public instance. Default: seed 0, 3 trials, 30 placement attempts per available copy.
- `human.py`: replays the published Shadoks file from `data/source/`.
- `reference.py`: replays the frozen copy from `data/reference/`.
- `evolution.py`: task-qualified wrapper for the bounded search.
- `evaluator.py`: shared `evaluate_candidate` adapter. Task registration remains owned by the main reviewer.
- Default seed-0 baseline completed all 3 trials and 3,435 attempts in 18.761 seconds. Its exact score is 711. The search record is saved in `best/seed0_solution.json`, `best/seed0_verification.json`, and `best/seed0_run.json`.
- Public human/reference witness score is 2304 from 23 placements. The exact checker independently recomputed it in about 0.06 seconds.
- Generation and verification budgets are 300 seconds and 60 seconds, 4 GiB memory, one thread.

## Tests and commands

Commands run:

```sh
.venv/bin/python -m pytest tasks/t093/test_task.py -q
.venv/bin/python -m json.tool tasks/t093/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t093/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t093/sota.json > /dev/null
git diff --check -- tasks/t093
```

All 7 test functions passed. They check exact input hashes and counts, all five program entries, the reproduced value against an independent source-value sum, boundary-only triangle contact versus positive-area overlap, invalid translations and multiplicities, strict config matching, ignored claims, seeded repeatability, and `_run` program-error and timeout behavior.

The public 2304 value is a feasible result and is reproduced exactly. This implementation does not prove it is optimal. The CG:SHOP public export whitelist must include only the instance JSON, never either solution JSON.
