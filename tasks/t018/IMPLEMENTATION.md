# T018 implementation notes

## Configurations

- C01 fixes order 29. Its frozen human reference is the Orrick et al. (2003) construction, independently checked by exact integer Bareiss elimination.
- C02 fixes order 27. Its frozen human reference is the printed Orrick et al. (2003) construction (determinant magnitude 12611693314584870912). Brent's public archive lists order-27 representatives; the first archived matrix is saved at `data/reference/order27.json` and has exact determinant magnitude 13293406466724593664.

The public archive describes Tamura's Gram matrix as conjectured optimal and lists known equivalence classes. This is not a proof of global optimality. C02 is accepted by Sol on 2026-11-07. The withdrawn order-31 draft is not part of the task.

The evaluator checks dimensions, integer ±1 entries, and determinant exactly. The baseline and evolution program start from generated constructions; neither reads reference assets. The public witness loader is an external comparison only.
