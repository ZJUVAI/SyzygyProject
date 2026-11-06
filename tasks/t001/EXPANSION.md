# Current review status

**Accepted by Sol on 2026-11-04.** The new configurations are in `task.json`. The text below preserves the Luna submission and its source notes. Current results are in `records.json:configuration_records` and the expansion report.

# T001 configuration expansion: C02 and C03

Luna submission status: **pending Sol review**. These configurations are staged in `configuration_expansion.json`. They are not in `task.json` and are not yet in the formal run registry.

Both configurations place equal circles in the unit square and maximize their common radius. The checker parses each coordinate and radius as an exact rational number. It checks all boundary clearances and every center pair. The reported objective is the radius in the verified construction. This proves feasibility and gives a lower bound; it does not prove optimality.

## T001-C02: 32 circles

The local human witness is copied from T005's saved construction at `tasks/t005/data/human32.json` and stored here as `data/human_reference_n32.json`. It has 32 centers and a common radius `10982269511/125000000000` (`0.087858156088`). T005's circles have equal radii. Their centers and radii are reused as exact decimal/rational strings, and this task independently checks the common-radius constraints.

Packomania reports 0.087858157088 for n=32 and exposes a coordinate page. The saved T005 construction has a slightly smaller radius, 0.087858156088, so the staged human reference uses its independently verified value. This copy is a reproduced construction, not a claim of a new best result. Packomania marks proven optima in bold; this entry is listed as a best-known result, not as proven optimal. The source's detailed attribution was not independently resolved in this expansion.

Sources: [Packomania table](https://packomania.com/csq/), [n=32 page](https://packomania.com/csq/csq32.html), [coordinate text](https://packomania.com/csq/txt/csq32.txt). A task-local copy avoids runtime imports from T005.

## T001-C03: 50 circles

The public coordinate file `https://packomania.com/csq/txt/csq50.txt` was retrieved on 2026-11-04 and copied to `data/packomania_n50.json`. Its centered-square coordinates were translated by `(1/2, 1/2)` to the unit square. The source radius is `0.071377103865`; this task uses the smaller exact rational `14275420753/200000000000` (`0.071377103765`), a reduction of `10^-10`. The checker validates all 1,225 pairs and all boundary clearances exactly.

Packomania reports `0.071377103865` at n=50 and uses boldface to distinguish proven optima from best-known constructions. The n=50 entry is not identified as proven optimal in the checked table. Its reference [14] attribution was not resolved to author and year during this implementation; no author attribution is claimed here. This is a reproduced public witness, not a claim of a new record.

Sources: [Packomania table](https://packomania.com/csq/), [n=50 page](https://packomania.com/csq/csq50.html), [coordinate text](https://packomania.com/csq/txt/csq50.txt).

## Reproduction and validation

Set `MATHBENCH_CONFIG_ID` to `T001-C02` or `T001-C03`. The seed makes a rectangular grid with exact rational spacing. The traditional baseline uses bounded seeded SLSQP multistart search and accepts improvements only after the same exact checker passes; otherwise it returns the grid. Human and reference programs read only the task-local copied witness.

The tests verify both saved human witnesses, exact score recomputation, grid feasibility, invalid and overlapping constructions, strict boundary checks, and ignored claimed scores. No witness has a claim of globally optimal packing.

## Sol acceptance, 2026-11-04

All four programs passed strict evaluation for each new configuration. Sol checked a cold seed export, independently recomputed a key quantity, rejected a damaged witness, and confirmed that a claimed score cannot change the score. Public record claims remain separate from reproduced witness scores.
