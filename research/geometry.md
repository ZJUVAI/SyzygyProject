# Geometry benchmark research

**Audit date:** 2026-11-03. This is a candidate ledger, not an implementation. The JSON contains 45 rows (11 accept, 21 conditional, 13 reject), including explicit duplicate/replacement rows so the parent curation can collapse overlapping names. After duplicates and umbrella items are removed, this is a pool of roughly 30 distinct task families; do not count the duplicate rows toward the final benchmark target.

## Strongest first-pass candidates

1. **Equal circles in a square** — [Packomania table](https://packomania.com/csq/) provides best-known records through 10,000 disks and downloadable coordinates/contact graphs. Radius in the unit square is a direct scalar; containment and non-overlap are directly verifiable. Records are not all proven optimal.
2. **Equal circles in a circle** — [Packomania table](https://www.packomania.com/cci/) is complete through 2,600, gives coordinates, contact graphs, and marks proven optima. Radius in a unit container is directly comparable.
3. **Unit squares in a square** — Friedman’s [dynamic survey](https://erich-friedman.github.io/papers/squares/squares.html) includes named historical human constructions, exact proven cases, upper/lower bounds, and a finite range through n=100. Score minimum container side; keep proof status separate from best-known construction.
4. **Unit squares covering a square** — Friedman–Paterson’s [paper and records](https://erich-friedman.github.io/papers/covering/covering.html) define a maximum target-side objective and state which n have known optimality (2, 3, 5, 10 and square n). Coverage can be verified geometrically.
5. **n unit circles covering a square** — Friedman’s [per-n record table](https://erich-friedman.github.io/packing/circovsqu/) gives named human constructions/proofs and numeric values for n=1–12. Max target side is a natural scalar.
6. **n unit circles covering a circle** — [per-n table](https://erich-friedman.github.io/packing/circovcir/) gives values and named historical records. It has recent updates, so freeze the version and distinguish found vs proved.
7. **n squares covering a square** — Friedman’s [catalogue](https://erich-friedman.github.io/packing/squcosqu/) gives numeric area values and attribution (e.g. Dudeney 1931; Trevor Green 2000; David Paterson 2002). Max target area is natural; source is image-led so coordinates need extraction.
8. **Area-optimal simple polygonalization, min/max separately** — the [CG:SHOP 2019 challenge](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2019/) and [UNICAMP dataset](https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Poly/) provide point instances, rankings/results, and solution permutations. Area of a submitted simple polygon is directly computable. Never use an uncertified global optimum as oracle.
9. **Minimum convex cover (CG:SHOP 2023)** — official [challenge page](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/) has instances/ranking; Copenhagen identifies the human winning team and result [here](https://barc.ku.dk/news/bachelor-project-at-barc-wins-computational-geometry-challenge/). Number of pieces is a natural scalar. Confirm the precise official validity rules before admission.
10. **Circles in a minimum-area arbitrary triangle** — Friedman’s [records](https://erich-friedman.github.io/packing/cirinttt/) give named human constructions by David W. Cantrell for multiple n and numeric area/sides. Min triangle area is directly checkable.

These are provisional recommendations based on named/public evidence. Attribution to a human author or a human competition does **not** establish that AI was not used. Where page attribution is historical and tool-use is unstated, the JSON says AI involvement unknown.

## Other viable replacements to investigate

- Equal squares in a circle: [Friedman’s table](https://erich-friedman.github.io/packing/squincir/), with selected proof claims and named constructions; freeze a historical instance because the page changes.
- Equilateral triangles in squares: [Friedman’s table](https://erich-friedman.github.io/packing/triinsqu/), with named constructions; needs coordinate extraction and optimality status.
- Consecutive dominoes in squares: [Friedman’s record sequence](https://erich-friedman.github.io/packing/domino/), with named builders and values, but optimality is conjectural for many n.
- Consecutive rectangles in similar rectangles: [Friedman’s table](https://erich-friedman.github.io/packing/minrect/) gives named Morandi (2015) values; inspect the source’s exact coverage-ratio convention before use.
- Unequal disks in a circle: [Packomania unequal-circle catalogue](https://www.packomania.com/ccib/), with cited papers and coordinate records. It needs an exact fixed instance/objective and provenance audit.
- CG:SHOP 2022 minimum partition into plane subgraphs: likely viable, but inspect the official challenge formulation and ranking before promoting.
- CG:SHOP 2024 maximum polygon packing: likely viable, but verify the challenge’s exact weight/area scalar and geometry rules.

## Exclusions and cautions

- I rejected duplicate formulations and umbrella families so distinct task count is not inflated.
- I rejected exact-optimum variants where the challenge would require an uncertified inner NP-hard optimum. Feasible candidate scalar values remain usable for the polygonalization and convex-cover tasks, with valid bounds kept separate.
- Heilbronn point-placement variants have a natural directly-computable scalar (minimum triangle area), but this pass did not verify an instance-level human record/data set; remain conditional/reject until that evidence is checked.
- The moving-robot CG:SHOP task has a natural makespan scalar, but may be out of scope for static geometric construction. It is marked conditional.
- Several Friedman/Packomania pages are living tables and many list best-known constructions rather than proven optima. Freeze page versions/coordinates; the score should compare explicit scalar objective values and provenance must label proof vs record.
- Pure feasibility puzzles were not accepted by inventing penalties. Rows without a source-defined scalar are rejected or left conditional.

## Source coverage

The primary source checks for this pass were the Friedman packing/covering pages and survey, Packomania’s equal-circle and unequal-circle catalogs, official CG:SHOP competition materials, a university press release for the 2023 winner, the CG:SHOP polygonalization data portal, and original/published papers. Exact URLs and per-row rationale, configuration parameters, verification cost, provenance caveats, and recommendations are in [geometry.json](geometry.json).
