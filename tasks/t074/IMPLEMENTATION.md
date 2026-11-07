# T074 implementation and verification record

## Configuration and status

- Configuration: `T074-C01`, 12 distinct rational points in the plane, no three collinear, with no coordinate bounds or fixed container.
- Objective: maximize minimum triangle area divided by convex-hull area.
- Reproduced public record: exact ratio `2/51`.
- Status: `accepted_by_sol`.

## Source and provenance

The current [Convex, n=12 archive page](https://math.tejstead.com/heilbronn/convex/12/) lists `2/51` and credits David Cantrell, June 2007. The page says that coordinate material was later supplied by an external contributor and re-verified; it cites a 2007 Cantrell Mathematica notebook received in September 2026. The archive's [methods page](https://math.tejstead.com/heilbronn/methods/) describes local reconstruction for some Cantrell records and says those reconstructions are not claimed as the original author's exact arrangements. This implementation preserves those provenance steps and does not label the locally rationalized coordinates as Cantrell's original coordinates.

The archived decimal JSON is stored at `data/source/tejstead_convex_n12.json`, SHA-256 `c5eaf80a1b3f270b949fe891eb9777541f0330c6d33a33e7b3d1eaa267c03b27`. `human.py` reads those decimal strings as exact base-10 rationals, maps the first three points affinely to `(0,0),(1,0),(0,1)`, then applies `limit_denominator(100)` to each normalized coordinate. The resulting fixture is `data/reference/cantrell_n12_rationalized.json`, SHA-256 `6e7f78156eac11badf81609e08f0c4600e98e31c42000867585e9d6d9cda11b4`.

Exact recomputation gives minimum triangle area `1/4`, convex-hull area `51/8`, and ratio `2/51`. The hull has 9 vertices. All 220 triples have nonzero determinant. The archive's current record table shows `2/51`; no n=12 optimality proof was found in the checked sources. Its 2026 machine-checked free-convex results for n=3 through n=8 do not cover n=12.

## Rational and real coordinate domains

The task accepts arbitrary rational coordinates. The rational and real domains have the same supremum. Given any feasible real configuration, its 220 determinants are all nonzero. Small coordinate perturbations preserve this condition. Rational coordinates are dense, and triangle areas, convex-hull area, and their ratio are continuous while hull area remains positive. Thus every feasible real value can be approached by rational configurations. This does not prove that a real maximizer has rational coordinates.

## Programs

- `check.py` parses integer, rational-string, and finite decimal coordinates as exact fractions. It rejects booleans, invalid rationals, duplicates, and every collinear triple. It checks all 220 triples and computes the hull with an exact monotone-chain algorithm followed by exact shoelace area.
- `init_program.py` is standalone and returns the 12 points `(i,i^2)` for `i=0,...,11`. A line meets a parabola in at most two points, so this seed has no collinear triple.
- `baseline.py` runs seeded one-point integer-coordinate hill climbing, with occasional equal-score moves.
- `evolution.py` keeps an elitist population and mutates one integer-coordinate point at a time.
- Both search programs start from the parabola seed and do not read comparison data. They default to proposals in `[-40,40]`; this is a search proposal range only. The checker does not limit coordinate size or rational denominator. `MATHBENCH_SEARCH_COORDINATE_LIMIT` changes the search range.
- `human.py` rebuilds the local rational witness from the archived decimal source. `reference.py` replays the fixed local rational witness.
- `evaluator.py` connects the shared runner. This task does not edit the shared registry.

## Checks performed

Tests cover source and fixture hashes, local reconstruction, independent exact determinant and shoelace calculations, all five program entries, translation/scale invariance at very large integer coordinates, duplicates, collinear points, wrong sizes, malformed coordinate pairs, bool/NaN/infinity/invalid rational inputs, a wrong configuration, forged score fields, runner errors, and timeouts.

Commands:

```sh
.venv/bin/python -m pytest tasks/t074 -q
.venv/bin/python -m json.tool tasks/t074/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t074/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t074/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t074/data/source/source_notes.json > /dev/null
```

Results on CPython 3.13.12, Linux x86_64:

- `.venv/bin/python -m pytest tasks/t074 -q`: 8 passed in 0.44 seconds.
- Seed 0, default fixed budgets, no wall-clock cutoff: initial objective `1/220`; baseline after 300 steps returned `1/199` in 4.343 seconds; evolution after 60 generations returned `1/220` in 0.111 seconds; human and reference each returned `2/51`.
- JSON parsing passed for all four JSON records listed above.
- The public witness was independently checked by enumerating all 220 determinants and using a separately specified 9-vertex hull order for shoelace area. It yielded minimum double area `1/2`, hull double area `51/4`, and ratio `2/51`.
- Default runner limits remain 300 seconds for generation, 60 seconds for verification, 4 GiB memory, and one thread. The tests exercise `_run` error and timeout paths. The full task suite was not run.

This implementation has not been accepted by Sol. It remains `accepted_by_sol`.
