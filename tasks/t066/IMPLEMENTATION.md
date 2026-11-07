# T066 implementation record

Status: `accepted_by_sol`.

The task fixes 17 distinct planar points and maximizes the number of distinct lines containing exactly three input points. A line with four or more input points is excluded. Coordinates are encoded in one real algebraic number field. The checker proves the minimal polynomial irreducible, proves the rational interval contains exactly one real root, reduces coordinates modulo the polynomial, canonicalizes each line over the field, and counts its point incidences exactly.

The primary source is Green and Tao's §2 acnodal-cubic parametrization and subgroup count, Theorem 2.5 and Proposition 2.6. At n=17 their formula gives 40 lines. Pegg's page is separate same-parameter evidence and is not the source of the exact coordinates here. The task witness is reconstructed by the classical cubic-curve method from `alpha=tan(pi/17)` and the 17 parameters `t_k=tan(k*pi/17)`; its coordinates are not claimed to match Pegg's figure. The minimal polynomial coefficients are stored in ascending order. The frozen witness file is `data/reference/cubic_tangent_17.json`, SHA-256 `0575565b5d4993e07ffcf34a3f4a7799bf214b2486b36c9d1bcec6b966fef77c`. Exact checker output is 40 lines; the maximum line incidence is 3. The independent determinant identity reduces collinearity to `i+j+k=0 mod 17`; direct enumeration gives 40 unordered triples. Since the cubic has no line component, these 40 triples define 40 distinct lines with exactly three points each.

The checked current sources give `a(17) in {40,41,42}`. The witness confirms the lower endpoint. No exact optimum claim is made. The asymptotic Green–Tao theorem is documented without using it to infer a finite-n answer.

The initial program uses 17 points on a rational parabola. The traditional baseline samples fixed-seed 17-point subsets of a 13 by 13 integer grid. Neither reads comparison assets. The human entry rebuilds the algebraic witness; the reference entry reads only its frozen witness under `data/reference/`.

Validation command:

```sh
.venv/bin/python -m pytest tasks/t066/test_task.py -q
```

The shared generation and verification budgets are 300 and 60 seconds. Field and determinant arithmetic use exact `Fraction` operations. The checker requires the repository's already declared SymPy dependency for irreducibility and Sturm root isolation.
