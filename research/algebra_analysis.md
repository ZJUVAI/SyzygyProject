# Algebra, analysis, sequences, matrices and coding theory research scan

**Candidate count: 45** — accept 10, conditional 23, reject 12. Configurations such as dimension, degree and exponents are not separate tasks.

## Candidate inventory

### AA01 — First Autocorrelation Inequality (AC1) (accept)

- **Objective:** Phi1=max_t(f*f)(t) (minimize).
- **Definition:** Find nonnegative integrable f supported on [-1/4,1/4], integral 1, minimizing max_{t in [-1/2,1/2]} (f*f)(t).
- **Human baseline:** SimpleTES (2026 paper table 11 reports human 1.509730; AI-assisted results separate: AlphaEvolve 1.505300; SimpleTES 1.503871). Human attribution cites prior sources [15,82,147], which should be independently checked before benchmark release.
- **Configuration:** {"support": "fixed [-1/4,1/4]", "representation": "piecewise polynomial degree and breakpoints; configure separately"}
- **Solution / verification:** Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass. Verification cost: Medium/high: exact convolution per polynomial segment, certify global maximum via roots/interval arithmetic.
- **Risks:** Sampling the continuum maximum is not a proof; enforce exact mass and nonnegativity. Human baseline provenance needs citation-level audit.
- **Sources:** https://arxiv.org/abs/2604.19341
- **Reason:** Named established objective, human record and one scalar; strict certificate possible with piecewise-polynomial representation.

### AA02 — Second Autocorrelation Inequality (AC2) (accept)

- **Objective:** Phi2=||f*f||_2^2/(||f*f||_1||f*f||_infinity) (maximize).
- **Definition:** Find nonnegative integrable f supported on [-1/4,1/4], integral 1, maximizing ||f*f||_2^2/(||f*f||_1 ||f*f||_infinity).
- **Human baseline:** SimpleTES (2026 table 11) reports best human 0.901500; AI-assisted: AlphaEvolve V2 0.961000; SimpleTES 0.962694.
- **Configuration:** {"support": "fixed [-1/4,1/4]", "representation": "piecewise polynomial degree and breakpoints; configure separately"}
- **Solution / verification:** Exact piecewise-polynomial or rational step function with proof of support, positivity and unit mass. Verification cost: High: exact convolution and certified L2/L1/L-infinity evaluation; maximum requires root isolation/interval methods.
- **Risks:** A sampled supremum gives unsound scores; human record citation chain needs audit. Objective's denominator conventions must be fixed.
- **Sources:** https://arxiv.org/abs/2604.19341
- **Reason:** Explicit published extremal objective with named human and AI baselines; admits rigorous certificates using algebraic pieces.

### AA03 — Third Autocorrelation Inequality (AC3) (accept)

- **Objective:** Phi3=max_t |(f*f)(t)| (minimize).
- **Definition:** Find real integrable f supported on [-1/4,1/4], integral 1, minimizing max_t |(f*f)(t)| over [-1/2,1/2].
- **Human baseline:** SimpleTES (2026 table 11) reports best human 1.458100; AI-assisted results include AlphaEvolve 1.455700 and SimpleTES 1.453675. Paper flags some AI comparisons as using a corrected verifier.
- **Configuration:** {"support": "fixed [-1/4,1/4]", "representation": "piecewise polynomial degree and breakpoints; configure separately"}
- **Solution / verification:** Exact piecewise-polynomial or rational step function, with exact integral and certified global supremum. Verification cost: High: exact convolution; certify absolute maximum by polynomial critical-point isolation or interval arithmetic.
- **Risks:** Continuum maximum cannot be sampled; verifier versions differed in prior AI comparisons; audit human sources.
- **Sources:** https://arxiv.org/abs/2604.19341
- **Reason:** Named objective, scalar and human baseline are directly tabulated; exact semialgebraic witnesses can be certified.

### AA04 — Erdős Minimum Overlap (accept)

- **Objective:** Minimize Ψ(f)=sup_{t∈R}∫_R f(x)g(x+t)dx. Here f:[0,2]→[0,1], ∫₀²f=1; g=1−f on [0,2] and g=0 outside [0,2]. Equivalently, Ψ(f)=sup_{t∈R}∫_{[0,2]∩[−t,2−t]} f(x)(1−f(x+t))dx.
- **Definition:** Both f and its complement g are supported on [0,2]; “1−f” is not extended as 1 outside the interval. Include all real shifts t, hence both directions for nonsymmetric f. This is the published continuous step-function relaxation for the limiting minimum-overlap constant; finite M(N)/N is not the same score on a submitted profile.
- **Human baseline:** Haugland (2016) reports human step-function upper-bound witnesses for this normalized functional: 15 steps gives 0.38153155 (rounded upward), while 51 steps gives 0.3809268534330870. These are literature-reported values, not independently recomputed here. AI-assisted values are separate.
- **Configuration:** `{"step_count": "number of equal-width intervals on [0,2], e.g. 15 or 51; representation setting"}`. Do not create separate tasks by varying finite partition size N.
- **Solution / verification:** Exact rational step function with breakpoints and values, exact mass, and certified maximization over all real shifts. The integral is piecewise polynomial in t on finitely many intervals; certify all intervals, including negative shifts. Verification cost: medium for rational steps, higher for deriving/certifying the continuous relaxation.
- **Risks:** If g=1−f is mistakenly set to 1 outside [0,2], then a large endpoint shift can yield a spurious score of 1. If only t≥0 is tested, nonsymmetric profiles may receive an invalid score. Grid sampling is not a proof.
- **Sources:** https://arxiv.org/abs/1609.08000; https://arxiv.org/abs/2201.05704; https://arxiv.org/html/2604.19341
- **Reason:** Named limiting extremal problem with concrete human step-function upper bounds and a natural scalar; the explicit support convention matches the published 0.38-scale values.
### AA05 — Hadamard Maximum Determinant, order 29 (accept)

- **Objective:** |det A| (equivalently the normalized determinant in the cited benchmark) (maximize).
- **Definition:** Find A in {−1,+1}^{29x29} maximizing |det A|.
- **Human baseline:** Orrick and Solomon's classical record, as reported by Ye et al. (2026): |det|=320·7^12·2^28 (normalized 0.935673). SimpleTES recovers it; this is AI-assisted and is not the human baseline.
- **Configuration:** {"order": 29}
- **Solution / verification:** 29x29 sign matrix; exact determinant certificate; optionally a proving upper-bound certificate if optimality is claimed. Verification cost: Low: Bareiss exact determinant; optimality verification is separate and harder.
- **Risks:** Do not score only existence of Hadamard; exact determinant is the natural scalar. Published value is a best-known lower bound, not necessarily proved global maximum.
- **Sources:** https://arxiv.org/abs/2604.19341; https://caramba.inria.fr/sem-slides/200904301100.pdf
- **Reason:** Explicit known scalar record, human construction, exact cheap evaluator; fixed order is configuration.

### AA06 — Best minimum distance of linear codes (accept)

- **Objective:** Minimum Hamming distance d(C) (maximize).
- **Definition:** For fixed (n,k,q), construct a q-ary linear [n,k] code with maximum minimum Hamming distance d.
- **Human baseline:** Human-computed database: Markus Grassl, John Cannon and Greg White's Magma BKLC tables; Magma reports 33,152 best-known binary codes, all binary entries through n=31 optimal. Row-wise d and construction need retrieval from the database. This is historical human computation, not AI.
- **Configuration:** {"n": "block length", "k": "dimension", "q": "finite-field order; use distinct benchmark rows, not one task per q/n"}
- **Solution / verification:** Generator matrix over GF(q), with independently checked rank and minimum distance. Verification cost: Medium for small k (enumerate q^k codewords); high beyond that. Restrict benchmark to enumerable dimensions or certificate-backed distance.
- **Risks:** Minimum-distance inner enumeration grows exponentially; restrict k (and n) and verify row construction. Database values are best-known, not all proven optimal. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html; https://codetables.de/
- **Reason:** Canonical construction problem and extensively maintained human table, with one exact scalar and matrix output.

### AA07 — Best length of a linear code at fixed dimension and distance (conditional)

- **Objective:** Block length n (minimize).
- **Definition:** For fixed (k,d,q), construct a q-ary linear code having dimension k, distance at least d and minimum possible block length n.
- **Human baseline:** Magma BKLC handbook documents BestLengthLinearCode(K,k,d), implementing the human best-known table; specific row score/construction is configuration-dependent and must be looked up. Historical human database, not AI.
- **Configuration:** {"k": "dimension", "d": "minimum distance constraint", "q": "finite-field order"}
- **Solution / verification:** Generator matrix over GF(q), with exact rank/distance check. Verification cost: Medium/high: minimum distance certification can require q^k enumeration.
- **Risks:** Distance lower-bound validity versus optimality of length; only small k rows are straightforward to verify. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html; https://codetables.de/
- **Reason:** Natural scalar and human tables exist; candidate selection must limit inner codeword enumeration and select open rows.

### AA08 — Maximum dimension of a linear code at fixed length and distance (conditional)

- **Objective:** Dimension k (maximize).
- **Definition:** For fixed (n,d,q), construct a q-ary linear code of length n and distance at least d with maximum dimension k.
- **Human baseline:** Magma BKLC handbook documents BestDimensionLinearCode and Grassl's tables of known bounds/constructions; pin a finite row for an executable baseline. Human-computed, not AI.
- **Configuration:** {"n": "block length", "d": "minimum distance constraint", "q": "finite-field order"}
- **Solution / verification:** Generator matrix, exact rank and verified minimum distance. Verification cost: Medium/high, exponential in k for naive minimum-distance check.
- **Risks:** Same underlying code family as aa06/aa07; likely redundant task formulation unless leaderboard deliberately tests the three dual parameter queries. Restrict k. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html; https://codetables.de/
- **Reason:** Scalar is natural and database-supported, but consolidate with aa06 unless the task suite explicitly wants complementary fixed-parameter views.

### AA09 — Maximum size of a binary code A(n,d) (conditional)

- **Objective:** |C| (maximize).
- **Definition:** Construct a subset C of {0,1}^n with pairwise Hamming distance at least d and maximum cardinality.
- **Human baseline:** A. E. Brouwer's classical tables and ongoing bounds; specific construction/value must be fixed per row. Human literature/database; no AI baseline assumed.
- **Configuration:** {"n": "block length", "d": "minimum distance"}
- **Solution / verification:** List of binary words; verify distinctness and pairwise distances. Verification cost: O(|C|^2 n) for lower-bound witness; proving optimality substantially harder.
- **Risks:** Many instances have only bounds, not exact optimum; select a published construction row and compare witness cardinality, not claim optimality.
- **Sources:** https://www.win.tue.nl/~aeb/codes/; https://doi.org/10.1016/0012-365X(90)90309-4
- **Reason:** Canonical extremal scalar and substantial human research; requires careful row selection and verifiable explicit witnesses.

### AA10 — Constant-weight code A(n,d,w) (accept)

- **Objective:** Code size |C| (maximize).
- **Definition:** Find a largest family of w-subsets of an n-set with pairwise symmetric difference at least d.
- **Human baseline:** Brouwer, Shearer, Sloane and Smith (1990) compiled bounds; many later explicit constructions and improved bounds. Pin row and construction before benchmark inclusion; human baseline, no AI assumed.
- **Configuration:** {"n": "ambient length", "d": "minimum Hamming distance", "w": "constant word weight"}
- **Solution / verification:** List of w-subsets/bitmasks; verify all weights and pairwise Hamming distances. Verification cost: Low/medium: O(|C|^2 n), often under a second for small instances.
- **Risks:** Do not confuse lower-bound construction with known optimum; duplicate of general nonlinear code only if constant-weight constraint is not central. Fixed rows needed. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://doi.org/10.1016/0012-365X(90)90309-4; https://doi.org/10.3934/amc.2016.10.525
- **Reason:** Named classical family, explicit construction tables and a cheap exact scalar verifier.

### AA11 — Constant-dimension subspace code A_q(n,d;k) (accept)

- **Objective:** Code size |C| (maximize).
- **Definition:** Find the largest set of k-dimensional subspaces of GF(q)^n with pairwise subspace distance at least d.
- **Human baseline:** Heinlein, Kiermaier, Kurz and Wassermann (2016, updated 2019) maintain Tables of Subspace Codes; the paper explicitly describes best lower/upper bounds and constructions. Fix an exact table row for score/construction.
- **Configuration:** {"q": "field order", "n": "ambient dimension", "k": "subspace dimension", "d": "minimum subspace distance"}
- **Solution / verification:** Basis matrices/RREFs for subspaces; exact rank/intersection verification. Verification cost: Medium: pairwise intersection ranks O(|C|^2 n^3) with finite-field linear algebra.
- **Risks:** Many rows are intervals rather than exact optima; select modest dimensions and public construction records. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://arxiv.org/abs/1601.02864; https://subspacecodes.uni-bayreuth.de/
- **Reason:** Canonical research objective, maintained human database and exact simple witness verifier.

### AA12 — Mixed-dimension subspace code A_q(n,d) (conditional)

- **Objective:** Code size |C| (maximize).
- **Definition:** Find the largest collection of subspaces of GF(q)^n, with unrestricted dimensions, having minimum subspace distance at least d.
- **Human baseline:** Heinlein et al. (2016/2019) subspace-code tables cover mixed-dimension codes and constructions; specific row must be fixed.
- **Configuration:** {"q": "field order", "n": "ambient dimension", "d": "minimum subspace distance"}
- **Solution / verification:** List of basis matrices for subspaces; verify all pairwise distances. Verification cost: Medium, pairwise finite-field rank calculations.
- **Risks:** Overlap with constant-dimension task; mixed-dimension design is a distinct published problem but sparse exact human baselines need screening.
- **Sources:** https://arxiv.org/abs/1601.02864; https://subspacecodes.uni-bayreuth.de/
- **Reason:** One scalar and database exist, but a good fixed row with comparable human construction is needed.

### AA13 — Partial spread size (conditional)

- **Objective:** Number of subspaces (maximize).
- **Definition:** Construct the largest collection of pairwise disjoint k-dimensional subspaces of GF(q)^n (partial k-spread).
- **Human baseline:** Beutelspacher (1975) established constructions/results; modern best-known constructions are catalogued in subspace-code tables. Fix an exact row for a numerical baseline.
- **Configuration:** {"q": "field order", "n": "ambient dimension", "k": "subspace dimension"}
- **Solution / verification:** List of subspaces; verify pairwise zero intersection. Verification cost: Medium, exact pairwise rank/intersection checks.
- **Risks:** Special case of constant-dimension code at distance 2k; consolidate rather than count independently if benchmark has aa11 at those parameters. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://doi.org/10.1007/BF01214740; https://arxiv.org/abs/1601.02864
- **Reason:** Well-studied scalar, but mathematically a special case of constant-dimension codes and likely duplicate.

### AA14 — Rank-metric code size (conditional)

- **Objective:** Code size |C| (maximize).
- **Definition:** For fixed matrix dimensions, field size and minimum rank distance, construct the largest matrix code with pairwise rank distance at least δ.
- **Human baseline:** Delsarte (1978) established rank-metric bounds and constructions; Gabidulin (1985) gave maximum-rank-distance codes attaining the Singleton bound for standard parameters. These provide explicit human constructions and optimal cardinality in MRD rows.
- **Configuration:** {"q": "field order", "m,n": "matrix dimensions", "delta": "minimum rank distance"}
- **Solution / verification:** List of matrices over GF(q); verify pairwise ranks of differences. Verification cost: Medium: pairwise matrix-rank checks; manageable for small configurations.
- **Risks:** Many canonical MRD instances are already solved exactly, so discovery headroom is limited; choose nontrivial non-MRD rows.
- **Sources:** https://doi.org/10.1007/BF01576918; https://doi.org/10.1007/BF01054462
- **Reason:** Strong human baseline and exact scalar, but standard benchmark rows are closed-form solved.

### AA15 — Quantum stabilizer code distance (conditional)

- **Objective:** Distance d (maximize).
- **Definition:** For fixed n,k,q, construct a stabilizer quantum code with maximum distance d.
- **Human baseline:** Grassl, Beth and Rötteler (2004) and Markus Grassl's maintained quantum-code bounds/tables provide human constructions and best-known bounds; row-wise baseline must be retrieved.
- **Configuration:** {"n": "physical length", "k": "logical dimension", "q": "qudit dimension"}
- **Solution / verification:** Stabilizer/check matrix over finite field with commutation constraint; provide distance certificate or exhaustive low-n check. Verification cost: High: distance search over stabilizer normalizer; limit n and k or use certified search.
- **Risks:** Distance verifier is substantially more complex than classical linear codes; do not treat a bound/table entry as a verified distance without construction.
- **Sources:** https://arxiv.org/abs/quant-ph/0312164; https://codetables.de/
- **Reason:** Clear scalar and human tables, but reliable independent verification is costly.

### AA16 — Self-dual binary code minimum distance (conditional)

- **Objective:** Minimum distance d (maximize).
- **Definition:** For fixed even length n, construct a binary self-dual code maximizing its minimum distance.
- **Human baseline:** Conway and Sloane (1990) developed extremal self-dual codes and bounds; later classification tables report best distances by length. Need pin down an explicit row and matrix.
- **Configuration:** {"n": "even block length", "code_type": "Type I or Type II"}
- **Solution / verification:** Generator/check matrix; verify self-orthogonality, dimension n/2 and minimum distance. Verification cost: Medium for small n: enumerate 2^{n/2} codewords.
- **Risks:** Type I/II and length regime matter; ensure human table source and exact matrix are accessible. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://doi.org/10.1016/0097-3165(90)90057-4; https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/self_dual_codes/
- **Reason:** Natural scalar with historical human constructions; candidate fixed instances can be exactly checked at modest n.

### AA17 — LCD binary code minimum distance (conditional)

- **Objective:** Minimum distance d(C) (maximize).
- **Definition:** For fixed binary [n,k] parameters, construct a linear code C with C∩C^perp={0} maximizing minimum distance.
- **Human baseline:** Massey introduced LCD codes (1992); later papers construct LCD codes and bound their parameters. Specific best-known row/result requires source audit; no numeric baseline asserted here.
- **Configuration:** {"n": "length", "k": "dimension"}
- **Solution / verification:** Generator matrix; verify rank, LCD condition and distance. Verification cost: Medium for small k; LCD test is a matrix-rank check.
- **Risks:** Published constructions may target asymptotic existence rather than finite best d; row-specific human baseline required. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://doi.org/10.1109/18.179379; https://arxiv.org/abs/1608.02170
- **Reason:** Promising structural constraint and scalar, but current finite baseline evidence is not yet pinned down.

### AA18 — Covering code size (conditional)

- **Objective:** Code size |C| (minimize).
- **Definition:** For fixed binary length n and covering radius R, construct a smallest set C whose radius-R Hamming balls cover the whole cube.
- **Human baseline:** Cohen, Honkala, Litsyn and Lobstein (1997) survey and tabulate covering codes; select a small open/nontrivial instance and recover explicit construction.
- **Configuration:** {"n": "length", "R": "covering radius"}
- **Solution / verification:** List of codewords; verify full coverage by exhaustive enumeration for small n. Verification cost: Low for small n (2^n point coverage), exponential and unsuitable for large n.
- **Risks:** Inner covering check scales exponentially; exact optimum often unknown. Only small finite instances qualify.
- **Sources:** https://doi.org/10.1017/CBO9780511524919
- **Reason:** Natural one-scalar design task with historical constructions, but verifier cost bounds useful scale.

### AA19 — Orthogonal-array strength (conditional)

- **Objective:** Strength t (or index λ, but not both in one task) (maximize).
- **Definition:** For fixed alphabet size q and number of columns n, construct an orthogonal array with maximum strength t at a prescribed index λ (or minimize λ for fixed t; choose one convention).
- **Human baseline:** Hedayat, Sloane and Stufken (1999) compile constructions and bounds; choose a concrete table row. Baseline currently pending row-level verification.
- **Configuration:** {"q": "alphabet size", "n": "columns", "lambda": "index when fixed"}
- **Solution / verification:** Finite array; exact count each t-column symbol pattern. Verification cost: Low/medium: enumerate column subsets and symbol tuples for small arrays.
- **Risks:** Objective must fix index or strength; broad parameterization risks conflating different design problems.
- **Sources:** https://doi.org/10.1007/978-1-4612-1478-6
- **Reason:** Construction output and finite exact scalar are suitable, but exact row and direction need normalization.

### AA20 — Best-known binary linear code database reconstruction (reject)

- **Objective:** Minimum distance d(C) (maximize).
- **Definition:** Given a selected [n,k] entry from Grassl/Magma, reconstruct a generator matrix attaining the tabulated best-known distance.
- **Human baseline:** Cannon, Grassl and White's Magma BKLC database; e.g. handbook gives [23,12,7] as optimal, with all best-known binary codes through length 31 optimal.
- **Configuration:** {"n": "length", "k": "dimension", "q": 2}
- **Solution / verification:** Generator matrix plus exact distance certificate. Verification cost: Low for k=12 (4096 codewords) and selected low-dimension entries.
- **Risks:** Duplicates aa06 by design; use only if benchmark specifically values rediscovery of a named explicit construction.
- **Sources:** https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html
- **Reason:** Same underlying objective as aa06 and should not be double-counted.

### AA21 — LABS minimum aperiodic autocorrelation energy (accept)

- **Objective:** E (equivalently merit factor L²/(2E)) (minimize).
- **Definition:** For s_i in {±1}, length L, minimize E=Σ_{k=1}^{L−1}(Σ_{i=1}^{L−k}s_i s_{i+k})².
- **Human baseline:** Bošković, Brglez and Brest (2014; arXiv 2014 / journal 2017) report best-known merit-factor tables and exact optima known through L≤60 at time of publication; Joshua Knauer's solution tables are referenced. Human historical records are distinct from later AI.
- **Configuration:** {"L": "sequence length; select fixed rows, do not count lengths as separate task families"}
- **Solution / verification:** Binary sign sequence. Verification cost: Low: O(L²) integer arithmetic.
- **Risks:** Energy and merit factor are strictly monotone transforms for fixed L, so they are the same task and must not be counted twice. Best known versus proven optimum must be labeled.
- **Sources:** https://arxiv.org/abs/1406.5301; https://www.sciencedirect.com/science/article/pii/S1568494617301023
- **Reason:** Canonical researched objective, explicit human sequence tables, extremely cheap exact scalar verifier.

### AA22 — LABS peak sidelobe level (PSL) (accept)

- **Objective:** PSL=max absolute nonzero aperiodic autocorrelation (minimize).
- **Definition:** For binary sign sequence s of length L, minimize max_{1≤k<L}|Σ_{i=1}^{L−k}s_i s_{i+k}|.
- **Human baseline:** Dmitriev and Jedwab (2005) studied typical PSL; later Best-Known Peak Sidelobe Level Values (2021) reports constructed sequences and search results. Retrieve row-specific construction before instantiation.
- **Configuration:** {"L": "sequence length"}
- **Solution / verification:** Binary sign sequence. Verification cost: Low O(L²).
- **Risks:** PSL optima can conflict with LABS energy; do not present as interchangeable with merit factor. Current row baseline needed.
- **Sources:** https://doi.org/10.3934/dcds.2005.12.315; https://doi.org/10.1109/TSP.2021.3078834
- **Reason:** Independent standard objective with its own human literature and one exact integer score.

### AA23 — LABS merit factor maximization (reject)

- **Objective:** Merit factor F (maximize).
- **Definition:** For a binary sign sequence length L with energy E as above, maximize F=L²/(2E).
- **Human baseline:** Bošković, Brglez and Brest (2014) compare solvers and historical human merit-factor records; known exact optimality was reported only up to length 60 at that time, while best-known sequences extended to L=304 and beyond.
- **Configuration:** {"L": "sequence length"}
- **Solution / verification:** Binary sign sequence. Verification cost: Low O(L²), exact rational score.
- **Risks:** For fixed L this is an exact monotone reparameterization of aa21 energy; merge with aa21 rather than count separately.
- **Sources:** https://arxiv.org/abs/1406.5301; https://militzer.berkeley.edu/sequences.html
- **Reason:** Duplicate objective with LABS energy at fixed length.

### AA24 — Periodic binary autocorrelation energy (conditional)

- **Objective:** Σ_{k=1}^{L−1} C(k)^2 (minimize).
- **Definition:** For s∈{±1}^L, minimize the sum of squares of nonzero periodic autocorrelations C(k)=Σ_i s_i s_{i+k mod L}.
- **Human baseline:** Golay (1949) studied complementary series and periodic autocorrelation; standard sequence-design literature includes explicit constructions. A benchmark row and numerical human construction are pending verification.
- **Configuration:** {"L": "period length"}
- **Solution / verification:** Binary sign sequence. Verification cost: Low O(L²).
- **Risks:** Be precise about periodic versus aperiodic correlation and normalization; known perfect sequences may make selected cases trivial.
- **Sources:** https://doi.org/10.1109/JRPROC.1949.232969; https://doi.org/10.1109/ICASSP.1990.115796
- **Reason:** Natural scalar and mature literature, but needs row-specific open headroom and cited human record.

### AA25 — Golay complementary pair merit (conditional)

- **Objective:** Peak summed aperiodic autocorrelation sidelobe (minimize).
- **Definition:** Construct a pair of equal-length unimodular sequences minimizing the maximum absolute sum of their aperiodic autocorrelations over nonzero shifts.
- **Human baseline:** Golay (1949) introduced complementary series; Davis and Jedwab (1999) give constructions for generalized Boolean functions. Exact zero sidelobe is known for many lengths, giving direct human constructions.
- **Configuration:** {"L": "sequence length", "alphabet": "binary or q-phase, one family per configuration"}
- **Solution / verification:** Pair of sign or polyphase sequences; coefficients and alphabet fixed as configuration. Verification cost: Low O(L²).
- **Risks:** Many instances attain zero exactly and therefore offer little discovery signal; constrain to lengths/alphabet where optimum is unknown, if found.
- **Sources:** https://doi.org/10.1109/JRPROC.1949.232969; https://doi.org/10.1109/18.796380
- **Reason:** Well-defined scalar and human constructions, but conventional complementary-pair rows are solved exactly.

### AA26 — Barker sequence maximum length (reject)

- **Objective:** Maximum feasible length L (maximize).
- **Definition:** Determine the largest length of a binary sequence whose every nontrivial aperiodic autocorrelation has absolute value at most 1.
- **Human baseline:** Known Barker sequences have lengths 2,3,4,5,7,11,13; Turyn and Storer (1961) proved no odd Barker sequence length >13; broader nonexistence remains unresolved in classic formulations.
- **Configuration:** {"alphabet": "{±1}", "sidelobe_bound": 1}
- **Solution / verification:** Binary sequence witness; nonexistence claims need a proof for larger lengths. Verification cost: Low to verify a witness; excluding longer lengths is a deep proof obligation.
- **Risks:** Existence-threshold task, not a smooth construction score; might violate benchmark scalar criterion if only boolean instances are used.
- **Sources:** https://doi.org/10.1016/0022-0000(61)90018-2; https://doi.org/10.1109/TIT.1965.1053768
- **Reason:** Primarily a yes/no existence problem and no practical comparable scalar witness score for fixed parameters.

### AA27 — Polyphase low-autocorrelation merit factor (conditional)

- **Objective:** Polyphase merit factor (maximize).
- **Definition:** For unit-modulus complex sequence z of length L, maximize L² divided by twice the aperiodic autocorrelation energy.
- **Human baseline:** Jedwab, Schmidt and collaborators have studied merit-factor problems and special constructions; best row-level finite sequences and exact score remain待核实 for a standard task.
- **Configuration:** {"L": "length", "phase_order": "root-of-unity alphabet size"}
- **Solution / verification:** Exact cyclotomic/algebraic unit-modulus entries or rigorously certified complex values. Verification cost: Medium: exact algebraic arithmetic if roots of unity; numeric-only candidates need interval certificates.
- **Risks:** Not the binary LABS problem; benchmark can duplicate it if alphabet distinctions are not made explicit. Human baseline must be row-specific.
- **Sources:** https://arxiv.org/abs/1512.02475; https://doi.org/10.1109/18.796380
- **Reason:** A genuinely different phase alphabet and standard scalar, but require concrete record and exact arithmetic protocol.

### AA28 — Maximum determinant of sign matrices, general order (conditional)

- **Objective:** |det A| (maximize).
- **Definition:** For each fixed order n, maximize |det A| over A∈{±1}^{n×n}.
- **Human baseline:** Hadamard's bound and Ehlich/Wojtas bounds; Orrick's maximal-determinant tables report human constructions. Order 29 has human lower-bound 320·7^12·2^28 (AA05); other selected rows require table extraction.
- **Configuration:** {"n": "matrix order; residue class n mod 4 is material"}
- **Solution / verification:** Sign matrix with exact determinant; optional upper-bound proof. Verification cost: Low exact determinant; global maximum proof high.
- **Risks:** General family includes aa05 order 29, so do not count both as independent tasks. Best-known construction does not imply proven optimum. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://caramba.inria.fr/sem-slides/200904301100.pdf; https://doi.org/10.1016/j.disc.2008.09.025
- **Reason:** Broad objective is canonical but fixed finite order instances are required; consolidate with order-29 entry in a 100-task list.

### AA29 — D-optimal design determinant (conditional)

- **Objective:** det(XᵀX) (or |det X| for square designs; choose one formulation) (maximize).
- **Definition:** Construct an n-run, m-factor design matrix under a fixed alphabet/design constraint maximizing determinant of its information matrix XᵀX.
- **Human baseline:** Kiefer (1959) and later D-optimal design literature provide explicit constructions and bounds; row-specific baseline not yet verified.
- **Configuration:** {"n": "runs", "m": "factors", "alphabet": "design levels and constraints"}
- **Solution / verification:** Design matrix with exact entries; verify constraints and exact determinant. Verification cost: Low/medium for exact small integer matrices.
- **Risks:** Maxdet ±1 matrices are a special case; overlaps aa28 if formulation identical. Need a non-equivalent design constraint and explicit row.
- **Sources:** https://doi.org/10.1214/aoms/1177706379; https://doi.org/10.1016/j.disc.2008.09.025
- **Reason:** Research-rich construction goal, but task must avoid being a mere rewording of sign-matrix maxdet.

### AA30 — Weighing matrix maximal order (conditional)

- **Objective:** Order n at fixed w (maximize).
- **Definition:** For fixed weight w, construct a weighing matrix W with entries 0,±1, WWᵀ=wI, maximizing order n among admissible matrices (or fix n and maximize w; choose one).
- **Human baseline:** Geramita and Seberry (1979) and subsequent weighing-matrix literature give constructions and tables; exact modern row needs verification.
- **Configuration:** {"w": "weight", "n": "order when using fixed-order alternative"}
- **Solution / verification:** Integer matrix with exact orthogonality certificate. Verification cost: Low: exact matrix multiplication.
- **Risks:** Mixed objective conventions (maximize order versus weight); many existence-table cells are binary yes/no. Need row with meaningful scalar gap.
- **Sources:** https://doi.org/10.1016/0012-365X(79)90002-7
- **Reason:** Natural exact matrix constraints, but public numerical record and optimization convention need pinning down.

### AA31 — Near-orthogonal sign matrix Gram defect (reject)

- **Objective:** Frobenius Gram defect (minimize).
- **Definition:** For fixed n, construct A∈{±1}^{n×n} minimizing a standard Gram-matrix defect such as ||AAᵀ−nI||_F²; use only if the cited literature has this same target objective.
- **Human baseline:** 待核实: maxdet constructions are often near-orthogonal but the Gram defect is not thereby a separately established human optimization target.
- **Configuration:** {"n": "order"}
- **Solution / verification:** Sign matrix. Verification cost: Low exact integer arithmetic.
- **Risks:** Do not invent an objective from a convenient penalty; not shown to be an independently studied target.
- **Sources:** https://arxiv.org/abs/2604.19341
- **Reason:** No verified literature/baseline for this exact objective; explicitly avoid proxy penalties.

### AA32 — Ultraflat Littlewood polynomial construction (conditional)

- **Objective:** sup_t ||P(e^{it})|/√N−1| (minimize).
- **Definition:** For degree N, find coefficients ε_j∈{±1} so that |P(e^{it})| is uniformly close to √N on the full unit circle, minimizing the worst normalized flatness error.
- **Human baseline:** Erdős posed the ultraflat Littlewood problem (1962); Bombieri and Bourgain (2009) studied Kahane's ultraflat polynomials in the unimodular class. For real Littlewood coefficients, uniform asymptotic ultraflatness is unresolved in classic literature; modern 2026 claims require independent review.
- **Configuration:** {"N": "degree/length", "representation": "exact coefficients; certification method separate"}
- **Solution / verification:** Exact ±1 coefficient polynomial plus rigorous supremum certificate using Bernstein/interval bounds or exact root isolation for squared modulus. Verification cost: High: continuum supremum certification; exact trigonometric polynomial interval bounds.
- **Risks:** Do not sample the unit circle as a strict certificate. Distinguish real ±1 from arbitrary unimodular coefficients; newest claimed results need independent specialist validation.
- **Sources:** https://doi.org/10.1112/blms/23.3.261; https://doi.org/10.1090/S0894-0347-08-00618-5; https://github.com/openai/math/tree/main/preprints/Ultraflat-real-Littlewood-polynomials-October-5-2026
- **Reason:** Named and scalarized classical construction challenge, but baseline status and continuous verifier demand rigorous review.

### AA33 — Littlewood polynomial L4 norm / merit factor (reject)

- **Objective:** Integral_0^{2π}|P(e^{it})|^4 dt normalized by N² (equivalent fixed-length LABS energy) (minimize).
- **Definition:** For P(z)=Σ_{j=0}^{N−1} ε_j z^j with ε_j∈{±1}, minimize its normalized L4 norm on the unit circle, equivalently maximize the binary aperiodic merit factor.
- **Human baseline:** This is mathematically equivalent to LABS merit-factor optimization; Bošković et al. (2014) provide human records/tables. No separate baseline is appropriate.
- **Configuration:** {"N": "coefficient length"}
- **Solution / verification:** ±1 coefficient list. Verification cost: Low O(N²) using correlation identity.
- **Risks:** Exact duplicate of aa21/aa23 under coefficient correspondence.
- **Sources:** https://arxiv.org/abs/1406.5301; https://arxiv.org/abs/1512.02475
- **Reason:** Merge with LABS; do not count equivalent polynomial and sequence representations separately.

### AA34 — Minimum Mahler measure of noncyclotomic integer polynomials (conditional)

- **Objective:** Mahler measure M(P) (minimize).
- **Definition:** For fixed degree bound d, find a noncyclotomic monic integer polynomial minimizing Mahler measure M(P)=∏ max(1,|root|).
- **Human baseline:** Lehmer (1933) exhibited the degree-10 polynomial with Mahler measure ≈1.176280818; it remains a classical smallest-known example and motivates Lehmer's problem.
- **Configuration:** {"degree_bound": "d", "class": "monic integer, irreducible, noncyclotomic"}
- **Solution / verification:** Integer polynomial with irreducibility/noncyclotomic proof and certified roots/Mahler measure. Verification cost: Medium/high: irreducibility and roots/Mahler measure require exact algebraic certification.
- **Risks:** For degree bounded and broad coefficient sizes the search space is ill-defined; specify coefficient/degree constraints and distinguish known lower bound from conjectured minimum.
- **Sources:** https://doi.org/10.1112/jlms/s1-8.4.242; https://doi.org/10.1007/978-3-642-36206-1_6
- **Reason:** Famous named scalar challenge and human construction, but parameterization and exact certification need careful design.

### AA35 — Newman polynomial minimum root radius (reject)

- **Objective:** Maximum root modulus (minimize).
- **Definition:** For fixed degree N, construct a polynomial with coefficients in {0,1}, constant and leading coefficients 1, minimizing the maximum modulus of its roots.
- **Human baseline:** Newman (1970) initiated the study; Boyd (1981) and later authors give constructions and bounds. Specific best polynomial at chosen N is待核实.
- **Configuration:** {"N": "degree", "coefficient_constraints": "Newman polynomial convention"}
- **Solution / verification:** Integer coefficient polynomial; exact root-radius upper bound and certified root isolation/lower bound as needed. Verification cost: Medium: certified complex root bounds.
- **Risks:** Trivial construction x^N+1 attains objective 1 under this definition; would need a different cited objective before reconsidering.
- **Sources:** https://doi.org/10.1007/BF01395666; https://doi.org/10.1007/BF01395681
- **Reason:** The proposed definition is trivial: X^N+1 is a Newman polynomial whose roots all have modulus 1, and the product of root moduli is 1, so its maximum root modulus cannot be below 1. This is not a meaningful search objective as stated.

### AA36 — Chebyshev minimax polynomial approximation (reject)

- **Objective:** Uniform approximation error ||g-p||∞ (minimize).
- **Definition:** For fixed continuous function g and degree d, find a degree-d polynomial minimizing ||g-p||∞ on a specified interval.
- **Human baseline:** Chebyshev's equioscillation theorem gives the classical minimax characterization; many reference functions have standard human polynomials and errors.
- **Configuration:** {"g": "target function", "d": "degree", "interval": "compact interval"}
- **Solution / verification:** Polynomial coefficients with exact or certified uniform-error bound. Verification cost: Medium: certify extrema of error polynomial/analytic function.
- **Risks:** Often solved by standard algorithms with known exact/near-exact answers; likely tests numerical approximation rather than mathematical construction discovery.
- **Sources:** https://doi.org/10.1090/S0002-9904-1934-05817-5; https://dlmf.nist.gov/3.11
- **Reason:** Too routine/closed-form for the intended construction-discovery benchmark; viable only as a calibration task.

### AA37 — Quadrature rule maximal degree of exactness (reject)

- **Objective:** Degree of exactness (maximize).
- **Definition:** For fixed node count m and a prescribed node/domain/weight class, construct nodes and weights maximizing polynomial degree of exactness.
- **Human baseline:** Gaussian quadrature theory (Gauss, 1814; standard numerical-analysis literature) gives degree 2m−1 for positive-weight rules, an exact human optimum.
- **Configuration:** {"m": "node count", "weight": "measure and constraints"}
- **Solution / verification:** Exact algebraic nodes and weights with moment identities. Verification cost: Low/medium for algebraic identities.
- **Risks:** For standard positive-weight rules the optimum is known exactly and construction is formulaic; altered constraints would need separate literature.
- **Sources:** https://dlmf.nist.gov/3.5; https://doi.org/10.1007/978-3-540-70529-1
- **Reason:** Closed-form solved benchmark with little construction discovery headroom.

### AA38 — Turán power-sum minimum (conditional)

- **Objective:** Specified sup norm of trigonometric power sum (minimize).
- **Definition:** For specified integer frequencies and number of unit-circle points, minimize the maximum of a prescribed trigonometric power sum over the unit circle.
- **Human baseline:** Turán (1937) introduced extremal power-sum problems and developed bounds; exact construction/score depends heavily on variant and needs verification.
- **Configuration:** {"number_of_terms": "m", "frequencies": "integer set", "weights": "fixed coefficients"}
- **Solution / verification:** Finite set of phases, preferably roots of unity/algebraic points, with certified global extremum. Verification cost: High: continuum supremum with algebraic/trigonometric certification.
- **Risks:** Problem family contains multiple inequivalent formulations; scalar and human baseline cannot be assigned until one canonical variant is selected.
- **Sources:** https://doi.org/10.1007/BF01456843; https://doi.org/10.1007/978-3-642-36206-1_6
- **Reason:** Longstanding extremal analysis with natural scalar, but current formulation is too broad for direct acceptance.

### AA39 — Minkowski lattice packing density (conditional)

- **Objective:** Packing density (equivalently inverse covolume at fixed minimum distance) (maximize).
- **Definition:** For a fixed dimension and specified lattice class, construct a lattice packing maximizing sphere-packing density.
- **Human baseline:** Minkowski (1896) introduced the problem; human constructions include root lattices, with exact densest lattice results known in some low dimensions (e.g. dimension 8 and 24 via Viazovska and collaborators for all packings). Row-specific lattice optima vary.
- **Configuration:** {"dimension": "d", "lattice_class": "all lattices or specified symmetry"}
- **Solution / verification:** Basis matrix plus rigorous determinant/minimum-vector-length certificate. Verification cost: High: shortest-vector and determinant certification; dimension-dependent.
- **Risks:** May be closed in famous dimensions or difficult to verify in open dimensions; source domain is geometric construction, suitable only with exact finite certificates.
- **Sources:** https://doi.org/10.1007/978-3-642-36206-1_3; https://doi.org/10.4007/annals.2017.185.3.8; https://doi.org/10.4007/annals.2017.185.3.10
- **Reason:** A single meaningful continuous scalar and extensive human constructions, but certificates and open-instance screening are demanding.

### AA40 — Hermite constant lattice construction (reject)

- **Objective:** Hermite invariant γ(L) (maximize).
- **Definition:** For fixed dimension d, construct a lattice maximizing shortest-vector length divided by covolume^(1/d), i.e. attaining a large Hermite invariant.
- **Human baseline:** Hermite constants have classical human values/constructions from Minkowski and root lattices; exact values are known in several dimensions, including 8 and 24 via sphere-packing work.
- **Configuration:** {"d": "lattice dimension"}
- **Solution / verification:** Exact Gram/basis matrix and rigorous shortest-vector certificate. Verification cost: High: exact shortest-vector enumeration and determinant arithmetic.
- **Risks:** Equivalent to lattice packing density at fixed dimension, so merge with aa39 if same lattice class/objective.
- **Sources:** https://doi.org/10.4007/annals.2017.185.3.8; https://doi.org/10.4007/annals.2017.185.3.10
- **Reason:** Duplicate parameterization of lattice packing density; merge rather than count separately.

### AA41 — Erdős–Ko–Rado intersecting family size (reject)

- **Objective:** Family cardinality (maximize).
- **Definition:** For fixed n,r, construct a largest family of r-subsets of [n] in which every two members intersect.
- **Human baseline:** Erdős, Ko and Rado (1961) prove the extremal size for n≥2r; the star construction attains it.
- **Configuration:** {"n": "ground-set size", "r": "subset size"}
- **Solution / verification:** List of r-subsets; verify pairwise intersections. Verification cost: Low for explicit family, O(|F|² r).
- **Risks:** Classical theorem completely solves standard parameter regime; no headroom, and boundary cases can be trivial.
- **Sources:** https://doi.org/10.1016/0001-8708(61)90002-1
- **Reason:** Closed-form solved construction with no competitive discovery challenge.

### AA42 — Maximum determinant of a 0/1 matrix (conditional)

- **Objective:** |det A| (maximize).
- **Definition:** For fixed n, maximize |det A| over A∈{0,1}^{n×n}.
- **Human baseline:** Barba and Ehlich/Wojtas developed upper bounds; explicit constructions and tables exist. Specific n and human record require checking a primary table before inclusion.
- **Configuration:** {"n": "order"}
- **Solution / verification:** 0/1 matrix and exact determinant. Verification cost: Low exact determinant; proof of maximum may be difficult.
- **Risks:** Related by normalization to sign maxdet but not identical; avoid counting as separate unless public target records and matrix family distinction are clear. Parent deduplication note: AA06/07/08 are alternate parameter views of best linear-code parameters; AA10, AA16 and AA17 are constraint-specific code variants/configurations; AA13 is a special case of AA11; AA28 contains AA05; AA42 is related to sign maxdet and should not be counted separately unless an independently studied 0/1 objective/table is established.
- **Sources:** https://doi.org/10.1016/0012-365X(79)90002-7; https://caramba.inria.fr/sem-slides/200904301100.pdf
- **Reason:** Natural scalar objective, but baseline and distinction from sign-matrix maxdet require verification.

### AA43 — Fekete polynomial minimum sup norm (reject)

- **Objective:** ||P||∞/√p (minimize).
- **Definition:** For a fixed prime p, construct a sign polynomial from Legendre symbols (or a clearly stated admissible class) minimizing its supremum norm on the unit circle.
- **Human baseline:** Fekete (1912) and subsequent analytic number theory give explicit character-sum polynomial constructions and bounds. Exact best finite value is not asserted and needs source verification.
- **Configuration:** {"p": "prime degree/length", "coefficient_rule": "Legendre sign convention"}
- **Solution / verification:** Exact coefficient polynomial and certified circle supremum. Verification cost: High: global circle supremum certification.
- **Risks:** If coefficients are prescribed by Legendre symbols there may be no search; if free, this merges into general Littlewood polynomial optimization. Objective's admissible class is unclear.
- **Sources:** https://doi.org/10.1007/BF01456843; https://doi.org/10.1007/BF02567595
- **Reason:** Current formulation either has no construction choice or duplicates Littlewood sup-norm tasks.

### AA44 — Maximum merit factor for ternary sequences (reject)

- **Objective:** Aperiodic autocorrelation energy or equivalent normalized merit factor (minimize).
- **Definition:** For fixed length L and alphabet {−1,0,1} under a stated fixed zero-count or energy constraint, minimize aperiodic autocorrelation energy (equivalently maximize merit factor).
- **Human baseline:** Binary LABS theory is extensive; ternary variants are studied in radar/sequence design, but a specific primary-source human record and canonical constraint were not verified in this pass.
- **Configuration:** {"L": "length", "zero_count": "fixed density/weight constraint"}
- **Solution / verification:** Ternary sequence with exact autocorrelation computation. Verification cost: Low O(L²).
- **Risks:** Admissible coefficient constraint changes the problem materially; current sources are not sufficient to substantiate this exact ternary objective.
- **Sources:** https://doi.org/10.1109/ICASSP.1990.115796; https://doi.org/10.1109/TSP.2021.3078834
- **Reason:** No verified canonical research target or human baseline for this exact variant.

### AA45 — Binary sequence maximum out-of-phase autocorrelation (periodic merit) (conditional)

- **Objective:** max_{k≠0}|Σ_i s_i s_{i+k mod L}| (minimize).
- **Definition:** For fixed length L, construct a binary sequence minimizing the maximum absolute nonzero periodic autocorrelation.
- **Human baseline:** Liu and Fan (1990) and later sequence-design studies report low periodic autocorrelation sequences and bounds; a specific row-level human record remains to be retrieved.
- **Configuration:** {"L": "period length"}
- **Solution / verification:** Binary sign sequence. Verification cost: Low O(L²).
- **Risks:** Related but distinct from aperiodic PSL; ensure periodic definition and cited baseline align exactly.
- **Sources:** https://doi.org/10.1109/ICASSP.1990.115796; https://doi.org/10.1109/TIT.1965.1053768
- **Reason:** Natural exact scalar and historical research, but needs a fixed, sourced comparison row.

## Screening and de-duplication notes

- AA21 (LABS energy), AA23 (merit factor), and AA33 (Littlewood L4) are equivalent at fixed length; retain one canonical LABS task.
- AA28 is the general-order maxdet family and subsumes fixed order-29 AA05. AA05 is a concrete fixed instance, not an independent task family.
- AA06/07/08 are alternate fixed-parameter queries for linear codes; consolidate. AA10, AA16, AA17 are structural code constraints, not automatically independent task families.
- AA13 (partial spreads) is a special case of AA11 (constant-dimension subspace codes). AA42 (0/1 maxdet) should not be separately counted without a distinct researched record.
- AA04 uses f and g both supported on [0,2], with g=1−f only on that interval, and takes the supremum over t∈R. This support convention is required for the reported 0.38-scale functional; do not use the erroneous zero-extension of 1−f or one-sided shifts.
- Continuous AC1–AC3 scores require exact piecewise-polynomial witnesses and certified global suprema; grid sampling alone is invalid. Code minimum-distance checking has an exponential inner loop, so restrict k or require independent certificates.
