# T081 implementation record

Status: accepted by Sol on 2026-11-06.

## Fixed objective and domain

`T081-C01` uses 12 distinct points in the plane and minimizes the exact ratio
of the largest squared pair distance to the smallest squared pair distance.
The formal candidate domain is all of `Q^2` with no coordinate or coefficient
bound. Since rational points are dense and the objective is continuous around
every 12-point set with positive separation, the infimum over rational point
sets equals the infimum over all real point sets. The input is 12 pairs of
integers or rational strings. The checker recomputes all 66 squared distances
and returns an exact rational objective. Candidate claims are ignored.

## Sources and construction

Friedman's current max/min page lists the n=12 report `r^2 = 5+2*sqrt(3)`
and credits Ingo Rechenberg (2006). The captured page and diagram are:

- `data/source/index.html`, 5,862 bytes, SHA-256
  `2e4558ef1115ba5ca203fb0474a9dc8e4eb39558ff0c76e74e8feec84e98658e`.
- `data/source/mm12.gif`, 9,218 bytes, SHA-256
  `3b7ecd7f25e1253479bc997869642631a5c2c3a4ebba8e5f3de3b8d6e4a75c09`.

The source page gives a diagram and exact reported value, but it does not give
coordinate strings. The local human program independently reconstructs the
pictured 12-point pattern by the formula documented in `README.md`. Exact
arithmetic in `Q(sqrt(3))` gives minimum squared distance 1, maximum squared
distance `5+2*sqrt(3)`, and 21 minimum-distance pairs.

The frozen candidate replaces `sqrt(3)` with
`floor(10^63*sqrt(3))/10^63`. `isqrt(3*10^126)` computes this numerator and
proves the two strict rational bounds. The exact rational checker gives:

- objective: `33856406460551018348219570732046978935542442030483045024446455830434458106192147637714398026789709384238645547380720042905106441/3999999999999999999999999999999999999999999999999999999999999998434458106192147637714398026789709384238645547380720042905106441`;
- minimum squared distance: `3999999999999999999999999999999999999999999999999999999999999998434458106192147637714398026789709384238645547380720042905106441/4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`;
- maximum squared distance: `33856406460551018348219570732046978935542442030483045024446455830434458106192147637714398026789709384238645547380720042905106441/4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`.

The rational objective is strictly larger than `5+2*sqrt(3)`. The source
diagram reconstruction and the rational witness are kept distinct. The
compatibility reference is the positive JSON number `8.464101615137755`,
rounded upward from the exact rational witness objective.

The 2026-11-06 Friedman page still lists this n=12 value as the smallest known.
AlphaEvolve's 2025 v1 paper, Problem 6.50, lists exact values through n=8 and
describes the n=9 through n=30 values as numerical candidates. The exact
minimum for 12 points is open in the sources checked; the reported value is an
upper bound, not a proof of optimality.

## Programs and saved baseline

- `init_program.py` returns a 4 by 3 grid with objective 13.
- `baseline.py` runs 12,000 seeded simulated-annealing moves on the rational
  grid with denominator 64. It uses integer squared distances to rank moves
  and reads no comparison witness.
- `human.py` builds the rational reconstruction directly from its formula.
- `reference.py` loads the frozen rational points.
- `evolution.py` invokes the baseline search.

The seed-0 search took 1.69 seconds on Python 3.13.12 / Linux and returned the
exact ratio `48625/5274`. The witness and run metadata are in
`best/seed-0.json` and `best/seed-0.metadata.json`. The recorded runner budget
is 300 seconds generation, 60 seconds verification, 4 GiB, and one thread.

## Tests

Command:

```sh
.venv/bin/python -m pytest tasks/t081/test_task.py -q
```

The tests cover all five program entries, exact Q(sqrt(3)) extrema, local
rational witness values, source hashes, invalid shapes and coordinates,
duplicate points, a 5,001-digit coordinate, ignored score claims, repeatable
seeds, and runner errors and timeouts through `mathbench.evaluate._run`.
Result: 16 passed in 5.70 seconds. All task and witness JSON files parse.
`git diff --check` passes.

## Sources checked on 2026-11-06

- Erich Friedman, [Minimizing the Ratio of Maximum to Minimum Distance](https://erich-friedman.github.io/packing/maxmin/), n=12 entry and `mm12.gif`.
- Ingo Rechenberg, “Point configurations with minimal distance ratio,” 2006, cited in [AlphaEvolve v1](https://arxiv.org/html/2511.02864v1), reference 237.
- Georgiev, Gómez-Serrano, Tao, and Wagner, [Mathematical exploration and discovery at scale](https://arxiv.org/abs/2511.02864), v1 dated 2025-11-03, Problem 6.50.
