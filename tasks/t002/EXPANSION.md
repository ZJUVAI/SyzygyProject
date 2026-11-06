# Current review status

**Accepted by Sol on 2026-11-04.** The new configurations are in `task.json`. The text below preserves the Luna submission and its source notes. Current results are in `records.json:configuration_records` and the expansion report.

# T002 configuration expansion

Luna submission status: `pending_sol_review`. The release `task.json` remains unchanged. This staged record proposes C03 (`n=29`) and C04 (`n=38`). C02 (`n=17`) was withdrawn after the source review found a formalized reported optimality proof. That claim still needs its own acceptance audit, so the configuration is excluded pending resolution.

The task minimizes the enclosing square side for `n` unit squares. The checker accepts exact rational and Q(√2) center coordinates and half-angle tangents. It computes all four corners, checks every square pair by separating axes, and recomputes the full bounding width and height. Strict mode uses exact rational arithmetic and no numerical tolerance.

## C03, n=29

The human reference is Thomas Schadt’s 2025 packing, found by simulated annealing. The published Schadt coordinates are high-precision numerical coordinates. The `jlevy/squares` project later rationalized that pose and retained an exact rational corner certificate. The source rational YAML is archived at `data/source_schadt_n029_rational.yaml`. `rebuild_witnesses.py` reads it without a YAML package and converts those rational corners to the task input form: each center is the average of four corners, and each rational tangent is recovered from one oriented unit edge. The checker certifies all 29 squares and 406 pairs. Its exact side is approximately 5.933885799813026. This is a reproduced human construction, not the current public best. The Squares Project reports a slightly better upper bound of 5.9338334626769292.

The original selected historical reference was the Gensane–Ryckelynck 2004 method, reported by Friedman as `s(29)<5.9344`. This expansion does not reproduce that earlier witness. The reproduced Schadt layout is a distinct, later human-computed baseline.

## C04, n=38

Friedman’s survey presents Göbel’s diagonal-strip family in Figure 1. The formula gives side `6+1/√2` at `n=38`. The saved witness reconstructs the family at `a=5`: two staircases of axis-aligned squares, two corner squares, and six 45-degree squares. The exact checker returns `6+1/2*sqrt2`; all 703 pair checks pass, and the width and height equal the side.

## Sources and limits

Sources checked on 2026-11-04:

- Friedman, “Packing Unit Squares in Squares: A Survey and New Results,” Figures 1 and 12: https://erich-friedman.github.io/papers/squares/squares.html
- The Squares Project n=29 case: https://squaremath.org/cases/29.html
- The Squares Project n=38 case: https://squaremath.org/cases/38.html
- Schadt’s coordinates and checker: https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record
- Retained exact rational Schadt witness: https://github.com/jlevy/squares/blob/main/packing/witnesses/schadt-n029-2025-rational.yaml
- Göbel-family reconstruction used to derive the n=38 layout: https://github.com/jlevy/squares/blob/main/packing/cases/gobel_strip/packing.py

Neither configuration asserts optimality. The n=29 public page reports a stronger construction than the reproduced human baseline. Sol review must validate source attribution, witness conversion, and the C04 family reconstruction before these configs enter the release registry.

## Sol acceptance, 2026-11-04

All four programs passed strict evaluation for each new configuration. Sol checked a cold seed export, independently recomputed a key quantity, rejected a damaged witness, and confirmed that a claimed score cannot change the score. Public record claims remain separate from reproduced witness scores.
