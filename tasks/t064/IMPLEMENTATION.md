# T064 implementation and source review

Status: **已通过 Sol 验收（2026-11-06）** (`accepted_by_sol`).

## Configuration and exact checks

- Configuration: `T064-C01`, official instance `ortho_40_56a6f463`, a simple orthogonal polygon with 40 boundary vertices and no added constraints.
- Objective: minimize the number of added Steiner points in the rational-coordinate version of the instance. Coordinates are arbitrary-precision integers/rationals; finite JSON floats are converted to their exact binary rational values. There is no denominator-bit or coordinate-string-length limit beyond the shared runner's 16 MiB output, 4 GiB memory, and 60 second verification limits. The checker caps Steiner points at 2,000; because the public feasible upper bound is 19, any improvement uses at most 18 points and is not excluded by this cap. The original geometry problem permits real coordinates; this task profile does not claim to represent every real-coordinate construction.
- The exact checker validates each point, edge, boundary interval and face. It checks non-crossing, containment, graph connectivity, coverage of all 40 boundary segments, one outer face, triangular bounded faces, nonnegative angle dot products, and exact equality of total triangle area and polygon area.
- Public witness: 19 Steiner points, 59 vertices, 121 edges, 63 bounded triangles. Both exact doubled areas equal `2711189126024`.
- Reconstructed traditional baseline: Cartesian grid from all distinct input x/y coordinates, with each interior rectangle split into two right triangles; 129 Steiner points. The code rebuilds it from the public input and does not read comparison witnesses.
- Fixed-seed evolution run: `best/search_seed_0.json`, 129 Steiner points after 20 pattern trials. It ties the grid baseline and does not improve on it.

## Sources checked

- Official instance `ortho_40_56a6f463`, saved at `data/source/ortho40.instance.json`, SHA-256 `f379e17cc7b4370d092ed37dcb6293dcb01c71d4f4c8e6cc4418c39ce178cad7`.
- Abrahamsen, Brunck, Conradi, Kolbe, and Nusser, “Computing Non-Obtuse Triangulations with Few Steiner Points,” SoCG 2025, Figure 10. It shows this instance with 19 Steiner points. https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.79/LIPIcs.SoCG.2025.79.html
- The corresponding software artifact is DOI `10.4230/artifacts.23288`, source repository commit `77920a0e578e5bff13c710f988ec1c52d61dcfd8`. The copied witness SHA-256 is `56bb1631924d9d254a399df25cb2ef0a1d9d18f228395dbefca98940b9151877`.
- Ahn, Lee, Kang, and Kim, “Incremental Algorithm and Local Search for Minimum Non-Obtuse Triangulations,” SoCG 2025, describes grid-based constructions for orthogonal instances. https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.80/LIPIcs.SoCG.2025.80.html
- The cited paper and artifact report a construction; they do not prove that 19 is optimal for this instance. No smaller same-instance witness or instance-specific lower-bound proof was found in the reviewed sources as of 2026-11-06. This is a bounded source review, not an exhaustive survey.
- AI provenance for the winning construction is not stated in the paper or artifact.

## Programs and isolation

- `init_program.py` is standalone apart from the whitelisted public input file. It imports no task modules and has paired EVOLVE markers.
- `baseline.py` searches three grid-diagonal patterns with fixed iteration and seed rules. It uses the input file only.
- `evolution.py` tests 20 seeded grid-diagonal patterns. It imports no human or reference program and reads no comparison witness.
- `human.py` reconstructs the 129-point grid method from the fixed input. `reference.py` reads only the saved public 19-point construction.
- `check.py` scales exact rational coordinates to integers by a common denominator, then uses exact orientation, dot-product, planar-face, coverage, and area checks. The checker does not trust candidate score fields.

## Validation

Command:

```sh
.venv/bin/python -m pytest tasks/t064 -q
```

The tests cover the public and reconstructed witnesses, all five `run_code()` entries, an exported seed with only the public input, deterministic budgets, zero-second cutoff, invalid and arbitrary-length rational coordinates, invalid indices, duplicate points and edges, a missing edge, a crossing edge, wrong instance/configuration, non-finite and forged scores, exact binary-float interpretation, an obtuse triangle, and runner failure and timeout handling through `mathbench.evaluate._run`.

Command: `.venv/bin/python -m pytest tasks/t064 -q` — **26 passed in 6.56 seconds**.

The key public witness values were independently recomputed with this task checker: 19 Steiner points, 63 triangles, and exact area equality. The human grid and fixed-seed search each return 129 points. The source and witness hashes are checked in the tests.

## Unresolved points

The exact minimum for this instance is not proved by the reviewed sources. The public 19-point construction is a feasible result only. The checker accepts arbitrary-precision rational coordinates within the shared runtime resources, but it does not certify constructions requiring non-rational coordinates. The reconstructed grid baseline is intentionally weak.
