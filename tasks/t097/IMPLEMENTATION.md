# T097 implementation record

## Frozen configuration

`T097-C01` is the official `socg_fixed92` instance. The input file has 92 boundary vertices and no holes. Its SHA256 is `573eb5e64a29369d17396fca899008702ba154865ec9ae343db173cd9aa04f38`. The objective is to minimize the number of convex polygons, with all cover pieces contained in the region and overlap allowed.

The task includes all real-coordinate covers. A solution uses a single real algebraic number field `Q(alpha)` for all vertex coordinates. The checker accepts arbitrary irreducible integer minimal polynomials, rational isolating intervals, and rational coefficient polynomials in `alpha`. It imposes no degree or coordinate cap. For rational input, a feasible finite cover is a first-order real-algebraic condition; real-closed-field transfer ensures a same-size cover exists with algebraic coordinates. Every finite algebraic tuple is contained in a simple extension, so the shared-field encoding does not change the optimum.

The checker validates the exact algebraic field, each convex polygon, and equality between the cover union and the fixed region. It computes all segment intersections, forms vertical slabs, and checks every open arrangement cell with exact arithmetic in `Q(alpha)`. Since the input and cover pieces are closed and regular, matching membership on all open cells proves equality of regions. The check does not use sampling or floating-point tolerances.

## Source and witness review

The official CG:SHOP 2023 download supplies the fixed region. The Shadoks viewer reports 15 pieces for `socg_fixed92`. The page has only rounded SVG coordinates. The reference program reverses its affine view transform and rounds nearby coordinates to integers. This does not recover the original submission coordinates uniquely. The resulting 15 integer polygons are one same-count feasible reconstruction, checked exactly by this task checker.

The main reviewer also ran an independent exact-fraction audit. It triangulated the input with recursive interior diagonals, checked each cover polygon's containment, and clipped the cover complement against the triangulation. The audit reported target area `206848`, uncovered area `0`, and 15 polygons. Its summary is in the ignored task-local run directory.

The viewer's CPLEX `Optimal` status is for a set-cover model over a generated candidate collection. It is not a global lower bound over all convex polygons. The official ranking gives aggregate team scores; DIKU (AMW) ranks above Shadoks overall, but the ranking does not expose per-instance values. The per-instance record inventory is therefore incomplete. The checked sources do not prove global optimality for `socg_fixed92` as of 2026-11-06. The 2026 rotten-potato paper provides an approximation algorithm and does not close this instance. The challenge accepted rational-coordinate submissions; this task extends the objective to all real coordinates and does not restrict the model to rational witnesses.

As a lower-bound check, an exact visibility-graph calculation over the 92 input vertices found a maximum hidden set of size 12. This rules out a 15-point certificate that uses only input vertices. It is not an upper bound on hidden sets with arbitrary points and does not prove a cover lower bound above 12.

The Shadoks paper and viewer do not disclose AI-use provenance for this witness. The source record therefore says “not disclosed.” It does not claim an unaided human process.

## Programs

- `init_program.py` independently implements exact ear clipping and reads only `data/source/socg_fixed92.instance.json`. The exported cold-start workspace needs this public input file.
- `baseline.py` runs a deterministic seeded greedy convex-hull merge search from the triangulation.
- `evolution.py` runs two seeded greedy merge restarts. Neither search reads human or reference data.
- `human.py` emits the nearby-integer 15-piece reconstruction.
- `reference.py` decodes the public rounded SVG and emits the same-count reconstruction.
- `check.py` returns the exact piece count after full feasibility validation.
- `evaluator.py` adapts the shared runner.

The saved own-search run uses seed 0, 65 sweeps (limit 200), 2,890 candidate pairs checked, and 64 successful merges. Its score is 26 pieces. It ran on Python 3.13.12, Linux x86_64, with the task budget of 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread. Its replay command and solution hash are in `best/T097-C01/manifest.json`.

## Validation

Command: `.venv/bin/python -m pytest tasks/t097 -q -x`

Result after the checker and coordinate-provenance wording updates: 38 tests passed. Tests cover the human and reference witnesses, simple triangulation, all five `run_code()` entries, exact validation of irrational degree-2 and degree-5 fields, large rational coefficients, malformed fields and coordinates, convexity and coverage failures, outside pieces, duplicate pieces, configuration direction and parameter checks, input checksums, tampered claimed scores, cold export with only the public input, runner errors/timeouts, and a temporary evaluator registry patch.

The saved search result was independently revalidated by `check.validate`: 26 pieces, 2,837 open arrangement cells, `certified`. The reconstructed human/reference cover was independently checked by `check.validate`: 15 pieces, `certified`. The root review also completed the separate exact-fraction cover audit noted above.

The task status remains `accepted_by_sol`.
