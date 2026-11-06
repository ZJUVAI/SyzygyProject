# Geometry task families, round 2

Audit performed 2026-11-03. This file contains 20 distinct problem families, separate from round 1’s fixed-container packing variants. Every row is in [geometry_round2.json](geometry_round2.json) with the requested definition, solution format, natural scalar objective/direction, configuration, human baseline, primary URLs, verification cost, risks, and recommendation.

## Recommended first candidates

- **Tammes / spherical codes.** Sloane and Cohn tables provide coordinates and best-known minimum-distance records; use fixed N and distinguish proven cases from numerical records.
- **Riesz energy, Thomson s=1.** The Cambridge Riesz database gives coordinates and energy values; it currently lists 53 s=1 configurations (N=512–9913), e.g. energy 124673.9055677 for N=512. Entries are lowest minima located, not universally certified global minima.
- **Maximum-volume inscribed polytope.** Sloane’s tables include coordinates. The N=9 case has a recent exact human proof and value 3√(2√3−3).
- **Free-convex Heilbronn, N=8.** Tej Stead’s public table includes coordinates and a rational verifier; A=0.0800001393294664…, construction by David Cantrell (2007), proved optimal by Tej Stead (2026).
- **Minimum max/min distance ratio.** Bateman–Erdős prove exact values for small planar N, e.g. r²=(3+√5)/2 for N=5 and r²=4 for N=7.
- **Kissing configurations.** Exact, human-proven calibration dimensions include 3, 4, 8, 24 with values 12, 24, 240, 196560 and explicit contact arrangements.
- **Minimum-dilation triangulation.** UNICAMP publishes 210 instances (10–70 points) plus results; 2025 work extends exact methods and reports many larger solved instances.
- **Perfect squared square.** Duijvestijn’s unique order-21 construction has side 112 and a public Bouwkamp code; order 21 is proved minimal.
- **Mrs. Perkins quilt.** The 13×13 case has an optimal 11-square construction with side multiset 1,1,2,2,2,3,3,4,6,6,7.
- **Empty-hexagon-free point set.** Overmars’s 29-point construction and the 30-point empty-hexagon theorem give an exact cardinality calibration.
- **Largest small polygon.** Reinhardt’s exact odd-N result and published global small even-N results provide clean area-scalar tasks.

## Conditional or limited cases

- Spherical designs have a natural minimum-N objective and downloadable constructions, but every chosen instance needs exact moment verification and a valid lower bound.
- Minimum-weight triangulations have large human-solved benchmark classes, but a convenient matching public instance/solution certificate still needs checking; the general problem is NP-hard.
- Minimum convex partition has a natural piece-count objective, but convention and dataset provenance require more source work.
- Polyomino order has published constructions (e.g. P-pentomino order 2, Y-pentomino 5×10), but a nontrivial benchmark should pin the piece and prove minimal order.
- Moving sofa has a now-proved human optimum: Gerver’s area 2.21953166887197… was established optimal by Baek (2024). However, validating a continuous motion/boundary certificate is expensive.
- Ambidextrous sofa has a human candidate near 1.6449552184, but no optimality proof and weakly standardized coordinate artifacts.
- Orchard planting has a natural integer objective and historical value tables, but selected-N coordinate/construction files need to be pinned.
- No-isosceles grid has a direct exact verifier and a 164-point n=100 incumbent, but the published incumbent trail is AI/LLM-assisted (PatternBoost then AlphaEvolve), so it is not a clean human-only baseline.
- Erdős distinct distances has a natural integer scalar and human theory/constructions, but this audit did not locate a benchmark coordinate/result package; small N=4 square (two distances) is only a calibration.

Rows that were genuinely unbounded (empty 7-gon avoidance), duplicate convex-partition formulations, or a second Heilbronn container variant were removed from the 20-row file rather than inflating the task count. No scalar penalties were invented for feasibility-only questions. Human attribution does not imply AI-free provenance; the JSON records unknown or AI-assisted provenance where applicable.
