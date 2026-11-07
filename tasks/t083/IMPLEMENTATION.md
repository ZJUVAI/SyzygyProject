# T083 implementation record

Status: **accepted by Sol on 2026-11-06**.

## Fixed instance and source review

The configuration is T083-C01: four unit equilateral triangles in an axis-aligned square, minimizing its side. Friedman's current `Triangles in Squares` table lists n=4 with side `1+1/sqrt(3)` and credits Erich Friedman in 1996. It labels the result as found, not proved. The same page separately says that n=3 was proved by Omer Zalman in October 2026. Page reviewed on 2026-11-06: https://erich-friedman.github.io/packing/triinsqu/ . The original n=4 image and the downloaded reconstruction source are kept in `data/source/`.

The exact local reconstruction stores the four directed edges and square side as Q(sqrt(3)) coefficients. Its source JSON is a transcription reconstructed from the image, not original author coordinates. The saved source image `data/source/friedman_t4.gif` has SHA-256 `e0784b81873ef0a96ed2a079e94380eeec564e603c53f416c8fad390c8dd6f25`. The checker independently verifies all edge lengths, containment, and six pairwise separations. Exact side is `1+sqrt(3)/3`; the frozen human value 1.577350269189626 is rounded upward.

## Domain and exact verification

Each coordinate is `a+b*sqrt(3)` with arbitrary rational coefficients. An edge direction is any rational unit vector. Q(sqrt(3)) translations and rational points on the unit circle are dense in real translations and rotations. To approximate any unrestricted feasible packing, shrink each unit triangle about its own centroid by a rational factor `lambda<1`. Distinct triangles have distinct centroids, so this creates positive clearance between their interiors. It also moves every triangle strictly inside the square. Approximate the resulting centers by Q(sqrt(3)) points and rotations by rational unit directions closely enough to preserve the clearances. Then scale the whole packing about the square origin by `1/lambda`. This restores unit side lengths, preserves the exact translation domain, and multiplies the square side by `1/lambda`, which tends to 1 as lambda tends to 1. Thus the infimum over the exact representation equals the unrestricted infimum. Individual real poses need not have exact representatives.

The checker performs arithmetic and order comparisons in Q(sqrt(3)). Triangle vertices use the exact 60-degree rotation formula. It checks every vertex against the axis-aligned square and runs separating-axis checks on all six pairs. Side output includes a rational enclosure based on integer square roots; the upper endpoint is conservative for minimization. It rejects floating-point coordinates and has no coordinate magnitude or denominator cap. Shared runner resource limits still apply.

## Program isolation and replay

`init_program.py` is self-contained and returns four upright triangles in a 2-by-2 arrangement. `baseline.py` and `evolution.py` use seeded anchor/direction mutations from that simple arrangement and exact checker feasibility. Their code imports no human/reference code or witness data. `human.py` independently emits Friedman's exact formula. `reference.py` reads only its pinned witness in `data/reference/`.

Default searches use 80 and 160 fixed candidate iterations, respectively, with seed from `MATHBENCH_SEED`. Setting `MATHBENCH_SEARCH_SECONDS` enables a machine-dependent exploration cutoff. Baseline and evolution report tested and valid candidate counts and declare that no comparison data was read.

## Validation commands

Use `.venv/bin/python -m pytest tasks/t083 -q`. Result: **29 passed**. The tests cover the exact published witness, the seed, all five `run_code()` entries, large rational strings beyond Python's default decimal parsing guard, invalid dimensions and types, non-unit edge vectors, boundary violations, overlap, ignored score fields, error/timeout runner paths, and the evaluator through a temporary configuration patch. The source image and source reconstruction provenance are included under `data/source/`.

The saved own-search result is seed 0, 160 fixed evolution iterations: 123 proposals passed feasibility and no proposal beat the initial side 2. The witness and replay metadata are under `best/T083-C01/`.

No Sol review or registry admission has been performed by this task agent.
