# MVP audit: algebra, analysis, codes, sequences, and matrices

> Historical audit, superseded on 2026-11-03 by [the configuration confirmation report](confirmation_summary.md). Several small configurations below are now excluded because their optima are proved. The AC3 value 1.45810 is the positive peak, not the maximum absolute value. Exact recomputation of the 150-step witness gives the absolute score 2.426895802097483. Use the current report for selection.

This is a source audit of seven proposed construction tasks. The numerical values below are literature-reported baselines; none of the cited witnesses were independently recomputed in this audit. A reported score and a reconstructed/revalidated artifact are distinct statuses. Configurations (length, dimension, number of steps) are parameters of one task family, not separate benchmark families.

## Summary

| Task | Proposed configs | Human baseline status | MVP status |
|---|---|---|---|
| Binary linear-code minimum distance | [15,7] and [23,12] | Exact published construction/table values 5 and 7; very small exhaustive verification | Accept, after pinning matrix/artifact |
| Sign maxdet | orders 29 and 31 | Exact human record matrices and determinants in 2003 paper; order-29 mirrors downloadable ANU data | Accept; benchmark order 29 |
| LABS | N=64 and 66 | Packebusch–Mertens exact exhaustive records E=208 and 257, with RLE witnesses | Accept |
| AC1 | n=10 and n=208 step functions | Matolcsi–Vinuesa 2009 appendix: 1.56618… and 1.50972… | Accept with certified continuum scoring |
| AC2 | n=20 and n=24 step functions | Exact human witness only at n=20, c=0.88922…; no same-config baseline yet found for n=24 | Conditional; use n=20 first |
| AC3 | signed n=20 and n=150 step functions | The n=150 witness has positive peak 1.45810… and absolute peak 2.426895802097483, independently recomputed in the later audit | See current confirmation report |
| Erdős minimum overlap | 15 and 51 equal-width steps on [0,2] | Haugland 2016: 0.38153155 and 0.3809268534330870 | Accept, with exact all-shift certification |

## 1. Binary linear-code minimum distance

**Task and scalar.** For fixed binary parameters (n,k), submit a rank-k generator matrix G over GF(2); score its minimum nonzero codeword Hamming weight d(C), higher is better. This is a natural, long-studied scalar objective. Verification by enumerating all 2^k messages is exact and easy for the suggested small dimensions. The endpoint score is the distance of the submitted code, not a claim that no better code exists.

**Two proposed configurations / historical human baseline.**

1. `(n,k)=(15,7)`: the standard binary BCH code has published parameters [15,7,5]; baseline distance 5. This code is small enough to check by enumerating 127 nonzero codewords. Treat the standard BCH construction as the human baseline; before release, attach an explicit fixed generator matrix so that the artifact is unambiguous.
2. `(n,k)=(23,12)`: Magma's BKLC example prints an explicit 12×23 generator matrix for a [23,12,7] cyclic binary Golay code; its displayed weight distribution has minimum nonzero weight 7, and its lower and upper bounds both equal 7. Thus the exact same-parameter human baseline is d=7 and the source contains the concrete matrix and distribution. Exhaustive check is 4095 nonzero words.

Magma describes this as its human-curated best-known linear-code database (33,152 binary entries, full through length 256; entries through length 31 are optimal in its stated sense). For these MVP rows, however, use the directly displayed matrices/weight distributions, not a blanket assertion about all database rows. The matrix in the handbook is a published table artifact; this audit has not independently enumerated it.

**Cost / risks.** Exact scalar verification costs O(2^k n). Cap k, and publish the field representation and generator matrix. Separate “candidate has distance d” from “d is globally optimal among all [n,k] codes.”

Sources: [Magma Best Known Linear Codes handbook](https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html) (explicit [23,12,7] matrix and distribution); [Magma code creation handbook](https://docs.magma-maths.org/CodingTheory/LinearCodes/creation.html) (standard constructions). The second proposed row's [15,7,5] parameter set should have its exact systematic/BCH generator matrix pinned from the selected public source before final benchmark freeze.

## 2. Sign maxdet

**Task and scalar.** For fixed order n, construct A∈{−1,+1}^{n×n} maximizing |det A|. The determinant is an exact integer scalar; verification uses exact integer arithmetic. This is not a Hadamard-existence yes/no task.

**Two proposed configurations / historical human baseline.**

1. `n=29` (primary MVP row): Orrick, Solomon, Dowdeswell, and Smith (2003) print a 29×29 record matrix and report `|det A|=2^28·7^12·320`. Richard Brent's ANU order-29 page independently records the corresponding Solomon Gram matrix and says that 4,918 Hadamard equivalence classes R satisfying G=RRᵀ=RᵀR are available in a gzip file at `https://maths-people.anu.edu.au/~brent/maxdet/order29/s29allsofar.txt.gz`. This provides direct downloadable matrix data; the paper's displayed human matrix is the straightforward source to pin for an MVP witness. The determinant is a historical human record/lower bound, not a proof of global optimality.
2. `n=31` (stretch row): the same 2003 paper prints a 31×31 ±1 matrix and reports `|det A|=2^30·7^12·5324`. It is an exact same-parameter human construction baseline, although the exhaustive matrix-optimization difficulty is higher.

**Cost / risks.** Exact determinant is cheap at n=29/31. A candidate's determinant can be certified cheaply, but proving it globally maximum is a different and much harder task. Keep the score as candidate |det| and annotate the human value “best known record,” not “proved maximum.” The Brent page describes the Gram matrix as conjectured optimal; do not claim the list of 4,918 decompositions is complete among all possible matrices.

Sources: [Orrick et al., *New lower bounds for the maximal determinant problem* (2003), arXiv](https://arxiv.org/abs/math/0304410) (paper text displays matrices and exact determinant values for n=29 and n=31); [Brent, Order 29 maxdet records and downloadable gzip](https://maths-people.anu.edu.au/~brent/maxdet/order29/); [direct gzip file](https://maths-people.anu.edu.au/~brent/maxdet/order29/s29allsofar.txt.gz).

## 3. Low-autocorrelation binary sequences (LABS)

**Task and scalar.** For sᵢ∈{−1,+1}, define `C_k=Σ_{i=1}^{N−k}s_i s_{i+k}` and `E=Σ_{k=1}^{N−1} C_k²`; minimize E (equivalently maximize merit factor `F=N²/(2E)`). These are natural classical objective definitions, not proxy violation counts.

**Two proposed configurations / historical human baseline.**

1. `N=64`: Packebusch and Mertens (2016) list an optimal sequence modulo symmetries with `E=208` and merit factor `F=9.846`; the RLE witness is printed in their Table 2. This is an exact exhaustive human computation at the same length.
2. `N=66`: the same paper reports all optima computed through N≤66 and lists `E=257`, `F=8.475`, with RLE witness `2112111211222b2221111111112224542` (their `b` means a run of length 11). This is also an exact exhaustive human result at the same length.

These are historical human algorithmic computations, not AlphaEvolve or later AI-assisted values. Their paper reports all optimal sequences up to 66; the printed sequence tables are modulo sequence symmetries. This audit did not decode the RLE and independently recompute E.

**Cost / risks.** Candidate scoring is O(N²) directly or faster using correlations, with exact integer arithmetic. The optimization problem at 64/66 is hard, but baseline checking is straightforward. Decode run lengths under the paper's convention and verify the resulting length before scoring. Do not use the heuristic/uncertified N>66 records as exact optimum baselines.

Source: [Packebusch & Mertens, *Low autocorrelation binary sequences* (2016), arXiv HTML](https://arxiv.org/html/1512.02475); [published J. Phys. A article, DOI 10.1088/1751-8113/49/16/165001](https://doi.org/10.1088/1751-8113/49/16/165001). The source defines E and F in Eqs. (2)–(3), states exhaustive optimality for N≤66, and provides the N=64 and 66 table entries and sequences.

## 4. AC1: nonnegative autoconvolution supremum

**Task and scalar.** Over nonnegative real f supported on [−1/4,1/4] with integral 1, minimize `||f*f||∞`, where `(f*f)(x)=∫f(t)f(x−t)dt`. This is the normalization stated by Matolcsi–Vinuesa (2009), not the unrelated coefficient normalization sometimes used to encode polynomials. Restrict proposed solutions to exact/rational step functions for the MVP.

**Two proposed configurations / historical human baseline.**

1. `n=10` equal step bins on the support: the 2009 paper gives the coefficient list `0.41241661, 0.45380115, 0.51373388, 0.6162143, 0.90077119, 0.14003277, 0.16228556, 0.19989487, 0.2837527, 0.78923292` and reports value `1.56618…`. The authors describe it as their small-n counterexample. The coefficients are the associated polynomial coefficients under the paper's discrete formulation; map them according to Eq. (13) and the paper's stated normalization, not blindly as step heights.
2. `n=208`: the online appendix gives a full 208-coefficient nonnegative witness whose coefficients sum to √416 and reports `||f*f||∞=1.50972…`. This is the paper's best known human step function at the time.

These are historical human numerical constructions; no re-evaluation here. SimpleTES later reports a human value around 1.509730, but the primary 2009 source's concrete witness/value is the baseline cited above. Do not substitute SimpleTES's AI result as human performance.

**Cost / risks.** A step function has an exactly piecewise-linear autoconvolution; its global maximum can be checked by evaluating exact breakpoints/critical points. Use rationalized inputs and certify mass/nonnegativity. The paper's displayed decimal coefficients give approximate witnesses; a benchmark-ready certificate should rationalize them, renormalize exactly, and recompute the scalar. Never score a sampled grid as a continuum supremum.

Source: [Matolcsi & Vinuesa, *Improved bounds on the supremum of autoconvolutions* (2009), original PDF](https://math.bme.hu/~matolcsi/sch0914.pdf), especially the definition in §1, discrete-polynomial normalization Eq. (13), and online appendix for n=10/208.

## 5. AC2: autoconvolution inequality constant

**Task and scalar.** For the same nonnegative, unit-integral support class, maximize `c(f)=||f*f||₂²/(||f*f||∞·||f*f||₁)`. Matolcsi–Vinuesa's Eq. (15) states the inequality in exactly this ratio orientation. Since `||f*f||₁=1` for the nonnegative unit-mass class, the normalization can simplify, but the benchmark should retain the printed ratio to prevent silent convention changes.

**Two proposed configurations / human baseline.**

1. `n=20` equal step bins: the 2009 appendix prints a 20-coefficient human witness and states that it achieves `c=0.88922…`, exceeding `log(16)/π=0.88254…`. This is a verified-in-literature same-config baseline; the authors explicitly say they did not extensively optimize it.
2. `n=24` equal step bins: proposed only as a held-out/refinement configuration. No matching n=24 human witness/value was found in the checked primary sources. Label baseline “unknown/not yet matched”; do not propagate 0.88922 to n=24 or claim it is its record.

The later SimpleTES table's human figure `0.9015` is attributed to Matolcsi–Vinuesa and Vinuesa's thesis, but this audit did not locate a matching step count and coefficient table in the checked sources. Therefore it is a literature-attributed aggregate, not an artifact-level same-config baseline. Keep it distinct from the directly inspectable n=20/0.88922 witness.

**Cost / risks.** For step functions, f*f is piecewise linear, so L1/L2 integrals and the global maximum can be computed/certified by segment arithmetic and exact critical-point checks. Rationalize and renormalize the decimal witness before accepting a certificate. The maximize direction matters; do not accidentally optimize the inequality's upper bound in the wrong direction.

Source: [Matolcsi & Vinuesa (2009), original PDF](https://math.bme.hu/~matolcsi/sch0914.pdf), Eq. (15) and Appendix (20 coefficients and c=0.88922…). Later human attribution: [SimpleTES (2026), arXiv](https://arxiv.org/html/2604.19341), mathematical discovery results table and its cited sources; [Vinuesa thesis (2010)](https://repositorio.uam.es/bitstream/handle/10486/4230/28565_vinuesa_del_rio_carlos.pdf?sequence=1). The .9015 value should remain unaligned until a matching primary witness is found.

## 6. AC3: signed autoconvolution supremum

**Task and scalar.** The historical extension allows real-valued f (including negative values), support [−1/4,1/4], and integral 1, minimizing `||f*f||∞=ess sup |f*f|`. This is not AC1 because nonnegativity is removed. SimpleTES also explicitly describes AC3 as controlling the largest absolute autoconvolution value, so these two stated conventions align at the objective level.

**Two proposed configurations / historical human baseline.**

1. `n=150` equal step bins, signed: Matolcsi–Vinuesa's 2009 appendix lists the 150 associate-polynomial coefficients. Later exact recomputation gives positive peak 1.458105685768 and absolute peak 2.426895802097483. For the absolute-value objective, use the latter score.
2. `n=20` signed: proposed as an easier diagnostic configuration only; the n=20 vector immediately above is an AC2 witness for a different objective and is not an AC3 baseline. No same-config signed AC3 human value is claimed here.

The norm notation alone does not establish that the reported decimal matches the absolute-value objective. The later coefficient check resolves this mismatch. The saved witness and exact rational calculation are in `baseline_examples/T081_matolcsi_vinuesa.json`. Check the released evaluator against its stated formula before comparing results.

**Cost / risks.** Signed step functions also yield piecewise-linear convolution, but the certificate must optimize the absolute value over both positive and negative lobes. This audit recommends **conditional** until the rounded appendix coefficients are rationalized/renormalized and independently checked against the continuous objective. Sampling is not sufficient.

Source: [Matolcsi & Vinuesa (2009), original PDF](https://math.bme.hu/~matolcsi/sch0914.pdf), §4 and online appendix for the signed n=150 vector. Comparison context: [SimpleTES (2026), arXiv](https://arxiv.org/html/2604.19341), AC task statement and table of human/AI results.

## 7. Erdős minimum-overlap constant

**Task and scalar.** Use Haugland's continuous step-function relaxation of `lim M(n)/n`. A candidate is f:[0,2]→[0,1] with integral 1; define g(x)=1−f(x) for x∈[0,2] and g(x)=0 outside [0,2]. Thus both f and g are supported on [0,2]. Minimize `Ψ(f)=sup_{t∈R}∫_R f(x)g(x+t)dx`, equivalently `sup_{t∈R}∫_[0,2]∩[−t,2−t] f(x)(1−f(x+t))dx`. Do not zero-extend `1−f` as a function equal to 1 outside the interval: that creates a spurious value 1 at large shifts. Take both positive and negative shifts; nonsymmetric candidates cannot be scored on one direction only. This is the continuous normalized constant, not the finite partition score M(n)/n.

**Two proposed configurations / historical human baseline.**

1. `15` equal-width intervals `(2i/15,2(i+1)/15)`: Haugland reports a human step function attaining `0.38153155` (rounded upward) in the continuous objective with both complements supported as above.
2. `51` equal-width intervals: Haugland reports `0.3809268534330870`; this is the best upper-bound witness in his 2016 paper. The source presents the coefficient vector in displayed equations, and both configurations are human constructions under the [0,2] support convention for f and g.

These are upper bounds from admissible witnesses, not proofs that the infimum equals the quoted number. Later AI-assisted and 2026 results are not used as human baselines. This audit has not transcribed, reconstructed, or independently evaluated either vector.

**Cost / risks.** For a rational step function, the shift functional is piecewise polynomial/linear with finitely many breakpoints; certify the maximum over every shift interval for all real shifts, including both signs. Confirm exact mass and that g is zero outside [0,2]. Haugland's original statement gives the [0,2] formulation and values; some later summaries shift to [−1,1] or rewrite the lag domain, so freeze one normalization only. A one-sided lag scan invalidly scores nonsymmetric functions.

Source: [Haugland, *The minimum overlap problem revisited* (2016), arXiv](https://arxiv.org/abs/1609.08000), especially statement of the [0,2] step-function infimum and reported 15-, 19-, and 51-step values. For this MVP, the 15/51 step-function coefficients must be transcribed from the PDF and certified; reported decimal scores alone are not revalidation.

## Final inclusion recommendation

For the first release, prioritize binary linear codes [15,7]/[23,12], sign maxdet n=29, LABS N=64/66, AC1 n=10, and minimum-overlap 15/51 steps with the corrected two-supported-functions/all-real-shifts definition. AC2 n=20 is viable once its decimal witness is rationalized and certified; keep n=24 baseline-unknown. AC3's stated absolute-value convention aligns between the historical L∞ notation and SimpleTES description; validate the n=150 witness under the exact continuous score before release. None of these tasks should score mere feasibility or violations of an existence constraint as a substitute for the cited natural scalar objective.
