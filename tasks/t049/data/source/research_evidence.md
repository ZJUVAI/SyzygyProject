# T017-C01 source check

Checked 2026-11-06.

Erdős and Fishburn, “Maximum planar sets that determine k distances,”
*Discrete Mathematics* 160 (1996), Table 1, p. 124, reports for the
triangular lattice `L_delta` the entry `n=91, k=34, s=6`. The regular
hexagonal array with six lattice points per side is reconstructed as
`max(|i|, |j|, |i+j|)<=5`, with coordinates
`(i+j/2, sqrt(3)j/2)`. It has 91 points. Its squared distances are integers
of the form `a^2+ab+b^2`; exact enumeration gives 34 values. The paper says
that table counts account for duplications and says it does not claim its
lattice choices are globally optimal.

Erdős's 1946 Theorem 1 gives the lower estimate `n-1<=k(k+1)` when a planar
set has `n` points and determines `k` distinct distances. At `n=91`, this
implies `90<=k(k+1)`, hence `k>=9`. The current OEIS A186704 entry describes
the sequence as the minimum number of distinct distances but lists its exact
sequence values only through `n=13`. In the sources checked, we found no
exact value or optimality proof for the fixed `n=91` instance. This is a
source-survey conclusion, not a proof that no result exists.

The maintained Erdős Problems page for Problem #89 marks the general
minimum-distances lower-bound conjecture open. The current Formal Conjectures
repository also tags Problem 89 as research-open. These status records
support that the wider problem remains active; they do not alone prove that
the particular finite value at n=91 is unknown.

The current Erdős Problems database marks the general distinct-distances
lower-bound problem #89 open. The related non-uniqueness problem #91 asks
about minimizers for sufficiently large n; it does not establish a value
for n=91. Guth and Katz (2015) prove a lower bound
`Omega(n/log n)` for the minimum number of distances; we do not turn that
asymptotic statement into an unverified numerical lower bound for n=91.

Sources:

- Erdős and Fishburn article record:
  <https://doi.org/10.1016/0012-365X(95)00153-N>
- Public PDF, Table 1, p. 124:
  <https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Erdos2.pdf>
- Erdős (1946), Theorem 1, lower bound for the number of distinct distances:
  <https://www.cs.umd.edu/~gasarch/TOPICS/erdos_dist/erdos.pdf>
- OEIS A186704, inspected 2026-11-06:
  <https://oeis.org/A186704>
- Erdős Problem #89, inspected 2026-11-06:
  <https://erdosproblems.ai/problems/89>
- Erdős Problem #91, related non-uniqueness question, inspected 2026-11-06:
  <https://www.erdosproblems.com/91>
- Erdős Problem #89, inspected 2026-11-06:
  <https://erdosproblems.ai/problems/89>
- Formal Conjectures, Problem 89 marked research-open:
  <https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/89.lean>
- Guth and Katz (2015):
  <https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p02-p.pdf>
