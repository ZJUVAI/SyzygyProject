# AlphaEvolve analysis and extremal-constant candidates — round 2

**Candidate count: 23** — accept 1, conditional 12, reject 10. Configurations such as dimension, degree and exponents are not separate tasks.

## Candidate inventory

### AA46 — Sign uncertainty principle (Fourier sign changes) (conditional)

- **Objective:** A(f)A(fhat), which is an upper bound on the sharp constant C (minimize).
- **Definition:** For even real f∈L1(R), define A(f)=inf{r>0:f(x)≥0 for |x|≥r}; with f(0), fhat(0)<0, seek constructions making A(f)A(fhat) small, hence an upper bound on the best universal constant C in A(f)A(fhat)≥C.
- **Human baseline:** Gonçalves, Oliveira e Silva and Steinerberger (2016): upper bound 0.353 and lower bound 0.2025. Cohn and Gonçalves (2017): upper bound 0.32831. Georgiev et al. (2025) AlphaEvolve-assisted construction: 0.321591. Cohn–de Laat–Gonçalves announced unpublished 0.3102 in 2025; distinguish this human result from AI-assisted AlphaEvolve.
- **Configuration:** {"Fourier_convention": "fix once", "function_family": "certifiable analytic family; degree/support settings are representation parameters"}
- **Solution / verification:** Explicit even real function with a rigorous Fourier transform/sign certificate and certified sign-change radii; use compactly supported piecewise-polynomial or Gaussian-polynomial forms with analytic transforms. Verification cost: High: certify signs of f and Fourier transform on unbounded domains, plus exact/rigorous threshold radii.
- **Risks:** A finite sample grid cannot certify eventual sign. Human 0.3102 is reported as unpublished in the AlphaEvolve problem page; use the published 0.32831 as baseline unless the unpublished artifact is publicly reproducible.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/11.html; https://arxiv.org/abs/2511.02864; https://arxiv.org/abs/1710.09008
- **Reason:** Named sharp-constant problem, natural one-number witness objective, and documented human published bounds; only include with rigorous Fourier-tail/sign certification.

### AA47 — Hausdorff–Young sharp constant (reject)

- **Objective:** C(p)=sup ||fhat||_{p'}/||f||_p (maximize).
- **Definition:** For 1≤p≤2, find the sharp C(p) in ||fhat||_{p'}≤C(p)||f||_p for real test functions on R, under fixed Fourier normalization.
- **Human baseline:** Beckner (1975) proved C(p)=(p^(1/p)/(p′)^(1/p′))^(1/2) under the paper's Fourier convention, with Gaussian extremizers; AlphaEvolve (2025) rediscovered the Gaussian form for p=1.1,...,2 in one or two iterations.
- **Configuration:** {"p": "exponent, with p′=p/(p−1)", "Fourier_convention": "fixed normalization"}
- **Solution / verification:** An extremizing function plus exact evaluation; for a lower-bound witness use a Gaussian and symbolic integral certificate. Verification cost: Low for Gaussian witness; proof of sharpness is classical and already known.
- **Risks:** Normalization convention changes the formula. Closed-form solved and easy to retrieve, so this is a calibration task only.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/14.html; https://doi.org/10.1002/cpa.3160280505; https://arxiv.org/abs/2511.02864
- **Reason:** Exact sharp constant and extremizer are classical solved results; little discovery headroom.

### AA48 — General one-dimensional Gagliardo–Nirenberg sharp constant (conditional)

- **Objective:** C(j,p,q,r,m)=sup ratio (maximize).
- **Definition:** For fixed admissible (j,p,q,r,m,θ), maximize ||D^j u||_p/(||D^m u||_r^θ ||u||_q^(1−θ)) over nonzero test functions u on R, with the scale relation in the AlphaEvolve problem statement.
- **Human baseline:** Classical Gagliardo (1958) and Nirenberg (1959) inequalities establish finiteness for the stated admissible regime. The AlphaEvolve paper states that the tested constants are known theoretically; it supplies the explicit solved special case aa49 but does not identify a single general-parameter human score. A fixed row and its sharp-constant reference remain待核实.
- **Configuration:** {"j": "derivative order", "m": "higher derivative order", "p,q,r,theta": "admissible exponents; select one fixed row"}
- **Solution / verification:** Explicit analytic or piecewise-polynomial function with rigorous norm and derivative-integral evaluation; certificate for a lower bound on C. Verification cost: High: improper integrals and derivative norms require certified tails; upper-bound proof of the sharp constant is harder than a witness score.
- **Risks:** General family is too broad as written; configure a single parameter tuple and distinguish a rigorous lower-bound witness from the unknown sharp constant.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html; https://arxiv.org/abs/2511.02864; https://doi.org/10.1007/BF02592041
- **Reason:** Natural one-number extremal objective and rich research, but benchmark needs a concrete row with an explicit human sharp value and certified witness evaluator.

### AA49 — Special Gagliardo–Nirenberg constant (one-dimensional sharp interpolation) (reject)

- **Objective:** C(p)=sup_f Q(f) (maximize).
- **Definition:** For p>2, maximize Q(f)=||f||_p^(4p)/(||f||_2^(2(p+2)) ||f′||_2^(2(p−2))) over nonzero smooth rapidly decaying real f.
- **Human baseline:** Weinstein (1983) sharp one-dimensional Gagliardo–Nirenberg inequality gives sech-type extremizer; AlphaEvolve paper states the exact extremizer f(x)=sech(x)^(2/(p−2)) and reports rediscovering it for tested p values in at most two iterations. This is human solved baseline, distinct from AlphaEvolve.
- **Configuration:** {"p": "real exponent >2; tested choices were in (2,10]"}
- **Solution / verification:** Exact extremizer sech(x)^(2/(p−2)) up to symmetries, with exact integrals; alternatively a certified function witness. Verification cost: Medium: exact beta/gamma integrals; certify the extremal proof is external to witness score.
- **Risks:** The AlphaEvolve paper explicitly derives C_6.15(0,p,2,2,1)=C_6.16(p)^(4p); it is a subfamily of aa48, not an independent task family. Standard p instances are fully solved.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/16.html; https://doi.org/10.1016/0022-0396(83)90022-3; https://arxiv.org/abs/2511.02864
- **Reason:** Closed-form human extremizer and constant; also mathematically a parameter specialization of aa48, so merge rather than count separately.

### AA50 — Young convolution sharp constant (reject)

- **Objective:** C(p,q,r)=sup_{f,g} ||f*g||_r/(||f||_p||g||_q) (maximize).
- **Definition:** For 1≤p,q,r≤∞ satisfying 1/r+1=1/p+1/q, maximize ||f*g||_r/(||f||_p||g||_q) over nonzero test functions.
- **Human baseline:** Beckner (1975) sharp constants: Gaussian extremizers f=e^(−αx²), g=e^(−βx²), α/β=√(q/p), with C(p,q,r)=C_HY(p) C_HY(q) C_HY(r′). AlphaEvolve (2025) recovered Gaussian parameter coupling in most runs.
- **Configuration:** {"p,q,r": "admissible exponents satisfying Young scaling", "Fourier_convention": "not applicable"}
- **Solution / verification:** Pair of Gaussians with exact norm/convolution integrals. Verification cost: Low for the Gaussian candidate; proof of sharpness classical.
- **Risks:** Endpoint conventions need care. Known exact answer and extremizer.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/17.html; https://doi.org/10.1002/cpa.3160280505; https://arxiv.org/abs/2511.02864
- **Reason:** Classical exact solution; only useful as a calibration case.

### AA51 — Centered one-dimensional Hardy–Littlewood maximal weak-(1,1) constant (conditional)

- **Objective:** C=sup λ·|{Mf≥λ}|/||f||_1 (maximize).
- **Definition:** For nonnegative f∈L1(R), maximize the ratio |{x: sup_{h>0}(1/(2h))∫_{x−h}^{x+h}f≥λ}| λ/||f||_1 over f,λ; this equals the best weak-(1,1) constant.
- **Human baseline:** Melas (1992) proved the exact constant C=(11+√61)/12≈1.5675208. Aldaz improved the known lower bound beyond 3/2 before the sharp solution. AlphaEvolve (2025) found a 1.5080 lower-bound witness unaided and about 1.533 with hints; later Station (2026) reports 1.557069 from 356 point masses. AI results are separate from Melas's human theorem.
- **Configuration:** {"centered": "centered intervals only", "finite_support_size": "number of atoms in lower-bound witness"}
- **Solution / verification:** Finite point-mass/interval witness with exact rational locations and weights; reduce score to a finite union of intervals and compute exactly. Verification cost: Low/medium for finite atom witnesses: enumerate interval endpoints and evaluate finite unions exactly.
- **Risks:** Sharp constant is already solved; make this a finite-certificate rediscovery task, not claim an open problem. Require a proof that the finite witness's computed ratio is valid.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/18.html; https://doi.org/10.1215/S0012-7094-92-06632-1; https://arxiv.org/abs/2511.02864
- **Reason:** Strong human scalar baseline and tractable finite witness scoring; suitable as a calibration task if solved problems are allowed.

### AA52 — Cohn–Elkies linear-programming bound for sphere packing (conditional)

- **Objective:** Normalized linear-programming upper bound C(d) (minimize).
- **Definition:** For a fixed dimension d, construct an admissible radial function f with f(0)>0, Fourier transform nonnegative and f(x)≤0 outside a specified radius, minimizing the normalized Cohn–Elkies upper bound on packing density.
- **Human baseline:** Cohn and Elkies (2003) introduced the LP bound; Viazovska (2017) proved its sharpness for E8, and Cohn, Kumar, Miller, Radchenko and Viazovska (2017) for Leech lattice dimension 24. For other dimensions, use published human LP bounds; choose an explicit row before acceptance.
- **Configuration:** {"d": "Euclidean dimension", "function_family": "radial basis / polynomial-Gaussian representation; exact certificate settings separate"}
- **Solution / verification:** Exact polynomial-times-Gaussian or rigorously certified radial function with Fourier positivity and sign constraints, plus computed bound. Verification cost: High: global Fourier positivity and sign verification on continuous domains; interval/analytic certificates required.
- **Risks:** Do not score sampled radial values. Dimensions 8 and 24 have solved packing optima; select open dimensions and compare only a certified bound.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html; https://doi.org/10.1007/s00454-003-2929-1; https://doi.org/10.4007/annals.2017.185.3.8; https://doi.org/10.4007/annals.2017.185.3.10
- **Reason:** Canonical scalar optimization with exceptional human constructions and rich public research, but the continuous certificate is demanding.

### AA53 — Rudin spherical harmonic Lp extremizer (conditional)

- **Objective:** C^p(d,D)=max_u ||u||_p/||u||_2 (maximize).
- **Definition:** For fixed d≥2, degree D and p∈{4,∞}, maximize ||u||_Lp(S^d)/||u||_L2(S^d) over real degree-D spherical harmonics, with sphere measure normalized to one.
- **Human baseline:** AlphaEvolve repository problem 57 and Georgiev et al. (2025) identify the finite-dimensional extremal problem, but the exact row-level human record/value was not retrieved in this pass; mark score待核实 before inclusion.
- **Configuration:** {"d": "sphere dimension", "D": "harmonic degree", "p": "4 or infinity"}
- **Solution / verification:** Harmonic coefficient vector in an exact orthonormal basis; certify norm ratio, using exact polynomial integration for p=4 or global optimization on sphere for p=∞. Verification cost: Medium for p=4 (finite algebraic integral); high for p=∞ (continuous sphere supremum).
- **Risks:** Need a published human construction/value for a specific (d,D,p); continuum maximization for p=∞ cannot be sampled as proof.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html; https://arxiv.org/abs/2511.02864
- **Reason:** Clean single scalar and finite-dimensional search space; baseline evidence and strict p=∞ verifier remain incomplete.

### AA54 — Ovals curvature Schrödinger eigenvalue (conditional)

- **Objective:** λ0(Hγ) (minimize).
- **Definition:** Minimize the lowest periodic eigenvalue λ0 of Hγ=−d²/ds²+κ(s)² over simple closed convex plane curves of length 2π.
- **Human baseline:** Benguria and Loss (2004) identified the circle/equality family with value 1, giving C≤1; Linde's 2015 work gives a global lower bound C>0.81 and numerical evaluation C>0.8246 (as summarized in later research). AlphaEvolve (2025) recovered the circle but not the noncircular equality family. Human constructions are explicit.
- **Configuration:** {"length": "fixed 2π", "curve_representation": "Fourier coefficients/breakpoints and exact closure constraints"}
- **Solution / verification:** Certified convex curve (e.g. rational Fourier curvature/tangent data satisfying closure and total turning) and rigorous eigenvalue upper bound; lower-bound claims need proof. Verification cost: High: certify convexity/closure and periodic Schrödinger ground-state eigenvalue; use validated spectral bounds.
- **Risks:** Circle immediately attains the known upper value 1; to create a useful benchmark, target a different construction such as recovery of noncircular equality family, but that is structural and not a scalar improvement.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html; https://doi.org/10.1007/s00023-004-0186-8; https://doi.org/10.1007/s00023-005-0005-2; https://arxiv.org/abs/2511.02864
- **Reason:** A named spectral variational problem with explicit human extremizers, but the scalar is already attained by the circle and meaningful discovery headroom is limited.

### AA55 — Sendov extremal critical-point distance (conditional)

- **Objective:** C(n)=sup_f max_k min_j |z_k−w_j| (maximize).
- **Definition:** For fixed degree n, maximize over degree-n complex polynomials with all roots in the unit disk the quantity max_k min_j |z_k−w_j|, where z_k are roots and w_j roots of f′; this is the sharp constant C(n).
- **Human baseline:** The human construction f(z)=z^n−1 gives C(n)≥1 exactly. Sendov conjectured C(n)=1. Meir–Sharma proved n<6; Brown n<7 and n<8; Brown–Xiang proved n≤8 (1999); Tao proved the sufficiently large-degree regime. Medium degrees remain open in the 2025 paper.
- **Configuration:** {"n": "polynomial degree; choose a single unresolved medium degree"}
- **Solution / verification:** Polynomial coefficients or roots, with certified root/critical-point distances; provide exact algebraic or interval-certified roots. Verification cost: Medium for candidate polynomial: certify roots and derivative roots; proving global supremum ≤1 is a deep theorem.
- **Risks:** For n≤8 or sufficiently large n human theory proves the conjectured value; choose a genuinely unresolved medium n. Numerical polynomial candidate is only a lower-bound witness.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/20.html; https://doi.org/10.1090/S0002-9939-1991-1050035-6; https://doi.org/10.1016/S0022-0396(99)00027-4; https://arxiv.org/abs/2511.02864
- **Reason:** Strong named open family and exact human construction at scalar 1; select a medium degree and rigorously certify root distances.

### AA56 — Schmeisser polynomial critical-point barycenter constant (conditional)

- **Objective:** C(n)=sup_{f, weights} min_j |Σ l_k z_k−w_j| (maximize).
- **Definition:** For fixed n, determine the least C(n) such that for each degree-n polynomial with roots in the unit disk and every convex combination of its roots, some critical point lies within distance C(n) of that combination.
- **Human baseline:** Schmeisser conjectured C(n)=1; the AlphaEvolve repository states the conjectured value but no numeric human construction or row-specific best lower bound was verified in this scan. Treat numerical baseline as待核实.
- **Configuration:** {"n": "degree n≥2", "weights": "simplex weights; part of optimization variables"}
- **Solution / verification:** Explicit polynomial roots and convex weights for lower-bound witness; exact derivative roots and certified distances. Verification cost: Medium/high: polynomial root certification and optimization over a continuum of convex weights.
- **Risks:** Human construction/record not verified; worst-case optimization includes a continuous simplex and polynomial family. Need a finite witness protocol.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/21.html; https://arxiv.org/abs/2511.02864
- **Reason:** Natural scalar extremal constant and cited human conjecture, but presently lacks a verified numeric construction baseline.

### AA57 — Borcea p-moment critical-point distance constant (conditional)

- **Objective:** C(p,n)=sup_f max_{root ζ} min_{critical ξ}|ξ−ζ| (maximize).
- **Definition:** For fixed (p,n), maximize the worst root-to-nearest-critical-point distance over degree-n polynomials whose roots satisfy n^−1Σ|z_i|^p≤1; this defines C(p,n).
- **Human baseline:** Borcea (1996) proved Sendov's conjecture for polynomials with at most seven distinct zeros. Khavinson, Pereira, Putinar, Saff and Shimorin (2011) formulated Borcea's variance conjectures; AlphaEvolve paper notes Borcea's conjecture C(p,n)=1 and verifies special cases (p,n)=(1,3),(2,4) in the cited literature. No general numeric row baseline retrieved.
- **Configuration:** {"p": "moment exponent, 1≤p<∞", "n": "degree n≥2"}
- **Solution / verification:** Polynomial roots and derivative roots with exact/interval algebraic data; verify moment constraint and distances. Verification cost: High: root and derivative root enclosures plus moment constraint; global sharpness unverified.
- **Risks:** Related to Sendov but genuinely adds a p-moment condition; parameter p=∞ recovers Sendov-like behavior. Need a concrete open row and numeric human lower construction.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/22.html; https://doi.org/10.1007/s00208-005-0660-2; https://doi.org/10.1007/978-3-0348-0105-5_10; https://arxiv.org/abs/2511.02864
- **Reason:** A distinct published strengthening with a single scalar; current baseline data are insufficient for a frozen benchmark row.

### AA58 — Smale mean-value extremal constant (reject)

- **Objective:** M_d=sup_p min_{p′(c)=0}|p(c)/c| (maximize).
- **Definition:** For degree d, maximize over normalized complex polynomials p(0)=0,p′(0)=1 the quantity min_{p′(c)=0}|p(c)/c|, defining a degree-dependent extremal constant; use the exact definition and normalization from the selected primary source.
- **Human baseline:** Smale (1981) proved the universal upper constant 4 and conjectured 1. Human literature supplied lower bounds approaching 1; Jatar and Ng (2026) report M≥√(8081/6656)=1.1018586788… with AI-assisted numerical exploration and author-written proof. Separately, Adamczewski (2026) reports an AI-found Lean counterexample to K=1; this is not a human baseline.
- **Configuration:** {"d": "degree"}
- **Solution / verification:** Exact polynomial coefficients with certified critical roots and quotient intervals. Verification cost: High: exact/algebraic critical roots and quotient; global degree-d extremum is much harder.
- **Risks:** The original K=1 conjecture was refuted by an AI-assisted construction in 2026; later quantitative result is AI-assisted. Human-only baseline and status require careful attribution.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/23.html; https://arxiv.org/abs/2511.02864; https://arxiv.org/abs/2608.27047; https://aixiv.online/abs/2609.01654
- **Reason:** Task status and best record are now materially AI-driven, and the scalar's degree-normalized canonical version needs definition audit before use.

### AA59 — de Bruijn–Sharma fourth-moment region (reject)

- **Objective:** No single canonical scalar: Ω(n) is a two-parameter feasible region. (not scalar-valued).
- **Definition:** For fixed n≥4, determine the feasible region Ω(n) of nonnegative pairs (α,β) such that for every zero-sum-root polynomial, the fourth moment of derivative roots is bounded by α times the root fourth moment plus β times the square of the root second moment.
- **Human baseline:** de Bruijn and Sharma's classical conjectural inequality family is documented in AlphaEvolve Problem 24; a concrete human boundary table/optimal pair was not verified in this scan.
- **Configuration:** {"n": "degree n≥4"}
- **Solution / verification:** Region boundary/certified inequalities and extremal root configurations. Verification cost: High: complex-root moment inequalities and a two-dimensional boundary certificate.
- **Risks:** Original target is set-valued rather than one scalar; choosing a weighted scalarization would be an invented benchmark objective unless a paper establishes it.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/24.html; https://arxiv.org/abs/2511.02864
- **Reason:** Fails the one-scalar comparison requirement as stated; do not impose an arbitrary penalty or scalarization.

### AA60 — Crouzeix numerical-range constant (reject)

- **Objective:** Universal Crouzeix constant C (minimize).
- **Definition:** Find the smallest C such that ||p(A)||≤C max_{z∈W(A)}|p(z)| for every complex matrix A and polynomial p; scalar-matrix-valued complete versions require their own specification.
- **Human baseline:** Crouzeix and Palencia (2017) proved C≤1+√2; nilpotent 2×2 matrix gives sharp lower bound C≥2. In 2026, Qinyu Luo and others published candidate/formal proofs of the sharp constant 2, so current status is solved/under review as of this scan.
- **Configuration:** {"matrix_dimension": "n", "polynomial_degree": "m", "complete_or_scalar": "fix formulation"}
- **Solution / verification:** Proof or finite matrix/polynomial lower-bound witness with certified numerical range and operator norm. Verification cost: High for universal proof; finite witness low/medium.
- **Risks:** Recent proof claims and independent review status are evolving; exact task is proof discovery, not a scalar construction benchmark. The simple 2×2 witness already attains lower bound.
- **Sources:** https://doi.org/10.1090/memo/1372; https://arxiv.org/abs/2608.03841; https://zenodo.org/records/22105428
- **Reason:** The sharp scalar is already established or subject to current proof review, and the natural lower-bound construction is elementary.

### AA61 — Noncommutative matrix AM–GM ratio (conditional)

- **Objective:** C(n,m,d)=inf/sup ratio as defined in the primary problem statement (direction and normalization must be transcribed exactly before acceptance) (待核实).
- **Definition:** For PSD matrices A_1,…,A_n and m≤n, optimize the published average norm ratio comparing products with repeated indices to products over distinct indices; use the exact unitarily invariant norm and index normalization of the chosen source.
- **Human baseline:** Duchi (2012) posed noncommutative AM–GM conjectures; Recht and Ré (2012) gave commentary/counterexample context. De Sa (2020) constructed counterexamples to a related matrix inequality. Exact parameter-row record and theorem status need primary-source audit.
- **Configuration:** {"n": "number of matrices", "m": "product length", "d": "matrix dimension", "norm": "fixed unitarily invariant norm"}
- **Solution / verification:** Finite PSD matrices with rational/algebraic entries; exact products, norms, and ratio or certified eigenvalue bounds. Verification cost: Medium/high: exact matrix products and spectral norms; PSD/eigenvalue constraints need certification.
- **Risks:** The problem definition is a ratio with multiple index sums and norm choices; transcription errors can invert the objective. A particular row and human construction must be validated first.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html; https://doi.org/10.5555/3042573.3042658; https://proceedings.mlr.press/v23/recht12.html
- **Reason:** Published matrix inequality family offers a natural scalar ratio, but objective direction and row-level baseline need exact primary-source reconstruction.

### AA62 — Factoring N! into N balanced factors (accept)

- **Objective:** min_i a_i, with the task maximizing this minimum (lower bound on C(N)) (maximize).
- **Definition:** For a fixed integer N, partition prime factors of N! among N integer factors and maximize the smallest factor; C(N) is the largest c for which N! can be factored into N factors all at least c.
- **Human baseline:** Guy and Selfridge studied the problem; the AlphaEvolve paper cites asymptotic C(N)/N=1/e−c0/log N+O(1/log^(1+c)N). Andrew Sutherland's public GuySelfridge.m implements a human search, and exact values C(N) for N≤10^4 are listed in the cited erdos-guy-selfridge repository/OEIS A034258. Retrieve a fixed row/value before freeze; not AI baseline.
- **Configuration:** {"N": "positive integer; choose a fixed table row"}
- **Solution / verification:** N positive integers with product exactly N!; verify exact product and minimum factor. Verification cost: Low for witnesses (big integer product); exact optimum is a bin-covering problem and may be expensive.
- **Risks:** Product factorization means integer factors, not arbitrary reals; fixed N and exact table baseline are mandatory. Optimality verification can be NP-hard.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/38.html; https://github.com/teorth/erdos-guy-selfridge; https://math.mit.edu/~drew/GuySelfridge.m; https://oeis.org/A034258; https://arxiv.org/abs/2511.02864
- **Reason:** Natural discrete construction score, exact cheap witness verification, and a public human algorithm plus extensive value table.

### AA63 — Spherical linear-programming bound (conditional)

- **Objective:** Upper bound on A(d,θ) from the Delsarte LP (minimize).
- **Definition:** For fixed sphere dimension and angular separation, optimize an admissible positive-definite Gegenbauer polynomial to minimize the Delsarte upper bound on spherical-code cardinality.
- **Human baseline:** Delsarte (1977) introduced the LP method; Levenshtein (1979–1998) derived explicit best-known bounds across parameter ranges. Human construction tables are public in the coding/spherical-code literature; choose an exact (d,θ) row and report its value before benchmark freeze.
- **Configuration:** {"d": "sphere dimension", "theta": "minimum angular separation", "degree": "polynomial degree / truncation"}
- **Solution / verification:** Exact Gegenbauer coefficients with positivity on the admissible interval and certified objective bound. Verification cost: Medium/high: certify Gegenbauer positivity and exact polynomial objective.
- **Risks:** Do not confuse bound optimization with finding an actual code; open dimension/angle row needed. Degree and angle are configuration, not separate tasks.
- **Sources:** https://doi.org/10.1007/BF01535476; https://doi.org/10.1007/BF01219469; https://arxiv.org/abs/2511.02864
- **Reason:** A genuine scalar construction optimization with extensive human baseline tables and tractable algebraic certificates.

### AA64 — Centered versus non-tangential Hardy–Littlewood constants (conditional)

- **Objective:** Cα=sup λ·|{Mα f≥λ}|/||f||1 (maximize).
- **Definition:** For α∈[0,1], define the one-dimensional maximal operator using intervals whose center is constrained by the evaluation point to the published α-range; maximize the weak-(1,1) ratio to obtain Cα.
- **Human baseline:** Centered α=0 constant is Melas's exact (11+√61)/12≈1.5675208; uncentered α=1 has classical constant 2. Recent 2026 research reports exact non-tangential constant 2 for 1/3≤α<1, with intermediate α still open. The benchmark must use a human-reviewed primary source for this variant.
- **Configuration:** {"alpha": "centering parameter in a fixed operator convention", "finite_support_size": "number of atoms"}
- **Solution / verification:** Finite atomic measure with exact interval geometry, producing a rigorous lower-bound witness for Cα. Verification cost: Low/medium for finite atoms; endpoint enumeration and rational interval-union measure.
- **Risks:** Operator convention varies across centered/non-tangential definitions; recent AI work claims results. Do not merge with centered AA51 unless α is part of the configured task family.
- **Sources:** https://doi.org/10.1215/S0012-7094-92-06632-1; https://arxiv.org/abs/2608.23691; https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/18.html
- **Reason:** Potentially active scalar extremal family and exact finite witness score, but variant definition and attribution need specialist review.

### AA65 — Rudin–Shapiro polynomial Lp extremizer (reject)

- **Objective:** C^p(d,D) (maximize).
- **Definition:** For fixed sphere dimension d and degree D, maximize ||u||_p/||u||_2 over real spherical harmonics u of degree D for p=4 or ∞.
- **Human baseline:** Rudin's problem is the named human research challenge; the AlphaEvolve paper presents no row-specific numerical best human score in the surfaced excerpt. Best-known value for a selected row remains待核实.
- **Configuration:** {"d": "sphere dimension", "D": "harmonic degree", "p": "4 or infinity"}
- **Solution / verification:** Exact harmonic expansion, certified spherical integral or supremum. Verification cost: High for p=∞, medium for p=4.
- **Risks:** This is the same task as AA53; duplicate entry intentionally demonstrates nomenclature overlap and should be merged.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html; https://arxiv.org/abs/2511.02864
- **Reason:** Duplicate of AA53; no distinct objective or separate baseline.

### AA66 — Sharp constant region for de Bruijn–Sharma inequalities (reject)

- **Objective:** No unique scalar unless an established linear functional of (α,β) is specified. (not scalar-valued).
- **Definition:** As AA59, determine the coefficient region Ω(n) governing fourth moments of derivative roots versus root moments, for fixed n≥4.
- **Human baseline:** de Bruijn and Sharma are the human originators; public AlphaEvolve statement is available, but no single baseline point/optimal boundary value was verified.
- **Configuration:** {"n": "degree"}
- **Solution / verification:** Certified boundary of feasible (α,β) region. Verification cost: High, two-dimensional feasible-region verification.
- **Risks:** Duplicate of AA59 and violates scalar-score criterion.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/24.html; https://arxiv.org/abs/2511.02864
- **Reason:** Duplicate set-valued formulation; do not scalarize without published rationale.

### AA67 — Optimal noncircular equality oval construction (reject)

- **Objective:** λ0(Hγ), with equality target 1; structural noncircularity is an additional constraint (minimize).
- **Definition:** Construct a noncircular closed convex curve of length 2π attaining λ0(−d²/ds²+κ²)=1 within the Benguria–Loss equality family.
- **Human baseline:** Benguria and Loss (2004) give a continuous equality family including noncircular ovals; AlphaEvolve (2025) reported only the circle. Thus the human construction already supplies the objective 1; later 2026 Station work independently recovered the noncircular family.
- **Configuration:** {"length": "2π", "family_parameter": "noncircle equality parameter"}
- **Solution / verification:** Exact curvature or curve parameter with closure, convexity and eigenfunction/eigenvalue proof. Verification cost: High spectral/curve certificate, though explicit equality family simplifies it.
- **Risks:** The natural scalar is already achieved by a circle, so requiring noncircularity changes the feasible class and is an added constraint; the underlying human construction is known.
- **Sources:** https://doi.org/10.1007/s00023-004-0186-8; https://arxiv.org/abs/2511.02864; https://dualverse.ai/station/math/ovals-problem/
- **Reason:** The proposed noncircle requirement is structural and does not improve the established scalar; it is not a separate scalar-optimization task.

### AA68 — Rudin spherical harmonic L4/ L-infinity constants (duplicate audit) (reject)

- **Objective:** C^p(d,D)=max ||u||_p/||u||_2 (maximize).
- **Definition:** Same as AA53: optimize the Lp-to-L2 norm ratio for real spherical harmonics of degree D on S^d.
- **Human baseline:** Rudin problem as listed in AlphaEvolve Problem 57; row-specific human value is待核实.
- **Configuration:** {"d": "dimension", "D": "degree", "p": "4 or infinity"}
- **Solution / verification:** Exact harmonic coefficient vector and certified norm ratio. Verification cost: High for L∞ continuous sphere supremum.
- **Risks:** Intentional duplicate check of AA53; do not retain twice.
- **Sources:** https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html; https://arxiv.org/abs/2511.02864
- **Reason:** Duplicate formulation; merge with AA53.

## Screening and de-duplication notes

- AA48 is the general Gagliardo–Nirenberg family; AA49 is its stated one-dimensional special case, so merge them as one family with a configured exponent row.
- AA53, AA65 and AA68 are duplicate names/formulations of the same Rudin spherical-harmonic Lp/L2 problem; retain at most one.
- Centered Hardy–Littlewood is solved exactly by Melas; AA51 is suitable only as finite-certificate calibration. AA64 describes a different parameterized non-tangential operator and needs a primary definition audit.
- Any continuous-domain norm/sign/eigenvalue objective needs a rigorous global certificate; finite sampling is not strict verification.
- AI-assisted 2026 results are labeled separately; the human baseline for uncertainty uses the published 0.32831 unless the reported unpublished 0.3102 becomes reproducible.
