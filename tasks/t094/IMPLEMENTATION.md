# T094 implementation record

Status: `accepted_by_sol`.

## Fixed configuration

- `T094-C01`: regular convex 120-gon; all straight-line vertex triangulations are allowed; minimize the maximum vertex-pair shortest-path/chord ratio.
- Objective direction: minimize.
- Human reference: certified 6-fan score rounded upward to `1.449476373154` for compatibility scoring.
- Public theorem bound: Sattari–Izadi prove a regular-polygon triangulation below `1.4482`; its specific 120-gon witness is not reconstructed here.

## Verification method

The checker validates integer endpoint labels, uniqueness, all boundary edges, the required `2n-3=237` edge count, and pairwise diagonal noncrossing. For a convex polygon these conditions establish a triangulation. It computes rational pi bounds with Machin's formula and alternating arctangent series. It bounds each chord with monotone sine and alternating Taylor bounds. Dijkstra runs on scaled integer lower and upper edge weights. For each pair, lower path / upper chord and upper path / lower chord form a certified interval for that pair's stretch. The maximum pair interval encloses the triangulation dilation. The reported objective is the conservative upper endpoint.

For the rebuilt 6-fan, the interval is
`[2890016242467687188760789/1993834667466255952395547, 481669373744614531460135/332305777911042658732591]`.

## Source review

- Fekete, Sándor P., Phillip Keldenich, and Michael Perk. “Exact Algorithms for Minimum Dilation Triangulation.” Journal of Computational Geometry 17(2), 2026. DOI: <https://doi.org/10.20382/jocg.v17i2a1>. The paper reports optimal regular n-gons for `4≤n≤100`; 120 is outside this range.
- UBC Theory Problem Solving Group, “Triangulating Regular Polygons to Minimize Dilation,” <https://www.cs.ubc.ca/labs/algorithms/tpsg/dilation.html>. It defines dilation and gives the 6-fan construction when n is divisible by 6.
- Sattari and Izadi, “An improved upper bound on dilation of regular polygons,” 2019, DOI: <https://doi.org/10.1016/j.comgeo.2019.01.009>. The theorem gives a bound below 1.4482 for regular polygons. The bound is recorded separately from the reproduced witness.

## Programs and isolation

The simple initial program emits a vertex-0 fan. The baseline samples random recursive split triangulations and uses floating-point dilation only as search feedback. It does not read human or reference files. The human and fixed-reference entries load their own task-local witness files. The source and reference files contain the same 6-fan edge set.

Default baseline: six trials, seed 0, bounded by the task runner's 300-second generation limit. The saved run took 0.556 seconds to generate and 6.713 seconds to verify on Python 3.13.12/Linux, with seed 0. Its certified interval was
`[2966313149770450274602155/1999314649951114560073522, 988771049923483424867388/666438216650371520024507]`.
Verification uses the runner's 60-second limit. One CPU thread is used by the scripts. The saved witness and environment are in `best/seed-0.json` and `best/seed-0.metadata.json`.

Validation command: `.venv/bin/python -m pytest tasks/t094/test_task.py -q` — 14 passed in 23.16 seconds after the directed interval checks were added. Tests also compare unrounded Taylor bounds at angle 1 with an independent 120-digit Decimal sine calculation, and compare every scaled chord bound with an independently evaluated 120-digit value. JSON parsing and `git diff --check -- tasks/t094` passed. Tests call the shared runner's `_run` helper directly for program error and timeout behavior; no registry change is needed.

## Limitations

This task records one feasible 120-gon triangulation. It does not prove it is optimal. The published `<1.4482` theorem gives a stronger upper bound on the optimum, but this implementation does not reproduce that construction. The 2026 exact-computation paper covers regular n-gons through 100 only. This source review is not an exhaustive literature survey.
