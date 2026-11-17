# T085 implementation notes

T085-C01 fixes order 29. Its frozen human reference is the Orrick et al. (2003) construction. The witness is independently checked with exact integer Bareiss elimination. Its determinant magnitude is `320 * 7^12 * 2^28 = 1188957517256767569920`.

The cited public sources report this as a best-known feasible value and describe the associated Gram matrix as conjectured optimal. They do not prove global optimality.

The evaluator checks dimensions, integer ±1 entries, and the determinant exactly. The baseline and evolution program generate their own constructions and do not read reference assets. The public witness loader is an external comparison only.
