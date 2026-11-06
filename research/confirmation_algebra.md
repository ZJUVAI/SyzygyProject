# Algebra and analysis configuration confirmation audit

Date: 2026-11-03

Configuration-level candidate screen for the 34 requested records. “confirmed_suitable” requires a fixed configuration, a public human construction/value, and checked evidence that the cited material does not prove optimality. It does not claim a complete state-of-the-art search. “pending” records have unresolved witness, sharpness, or configuration checks; “excluded” records are solved or unsuitable. Recomputed tracks local witness validation separately.

## Status counts

- `confirmed_suitable`: 27
- `pending`: 7

## Records

### T073

- Status: **confirmed_suitable**
- Parameters: `{"L": 100}`
- Scalar: aperiodic energy E=Σ_{k=1}^{L−1} C_k² (equivalently maximize merit factor L²/(2E)) (minimize)
- Human baseline: Militzer, Zamparelli and Beule (1998): length-100 binary sequence, exact energy E=638, merit factor 10000/(2·638)=7.8369905956, PSL=7. The published sequence is in the saved source artifact.
- Current record: Not exhaustively audited; the witness is historical and not claimed current.
- Open evidence: No optimality proof is identified; older source explicitly says its historical sequence was later improved. This is a feasible incumbent, not current best.
- Recomputed: **yes**
- Remaining: Historical feasible incumbent only; the local artifact reproduces energy 638 and merit factor 7.836990595611285. Current-best and optimum status are not surveyed.
- Source: https://militzer.berkeley.edu/sequences.html
- Source checks:
  - https://arxiv.org/abs/1512.02475: Packebusch–Mertens report all optimal sequences through N≤66. Limitation: Does not provide open proof status for N=100.
  - https://militzer.berkeley.edu/sequences.html: Human length-100 sequence with historical merit factor 7.84. Limitation: Historical result; page explicitly notes later improvements; value rounded.
  - https://greif.geo.berkeley.edu/sequences.html: Author-hosted sequence archive includes the human low-autocorrelation constructions. Limitation: Historical archive, not a current record survey.

### T074

- Status: **confirmed_suitable**
- Parameters: `{"L": 100, "aperiodic_sequence": "published length-100 binary construction"}`
- Scalar: PSL=max absolute nonzero aperiodic autocorrelation (minimize)
- Human baseline: Nunn–Cox (2008) report length-100 binary code with aperiodic PSL 5. This is a published human feasible sequence construction, not a proof of optimality.
- Current record: Not exhaustively audited; no current frontier claim.
- Open evidence: The former L=64 configuration is excluded: Leukhin–Potehin report exhaustive minimum PSL sequences through length 68. At L=100, Nunn–Cox give PSL 5; no optimality proof for L=100 was found in the sources checked.
- Recomputed: **no**
- Remaining: Retrieve the length-100 coefficient row and independently score it before publication; do not claim the value is current.
- Source: https://www.norbertwiener.umd.edu/crowds/documents/best_known_binary.pdf
- Source: https://arxiv.org/abs/1212.4930
- Source checks:
  - https://arxiv.org/abs/1212.4930: Leukhin–Potehin abstract states exhaustive minimum PSL results through length 68; this closes L=64. Limitation: Does not address length 100.
  - https://www.norbertwiener.umd.edu/crowds/documents/best_known_binary.pdf: Nunn–Cox 2008 primary paper reports PSL 5 for lengths 83–105, including 100. Limitation: Sequence coefficients were not extracted; current best status not audited.

### T075

- Status: **pending**
- Parameters: `{"L": 101, "period": "prime length; Legendre binary sequence with s_0=1"}`
- Scalar: Σ_{k=1}^{L−1} C(k)^2 (minimize)
- Human baseline: Legendre binary sequence at prime p=101: s_0=1 and s_i=χ(i) for i≠0. Since 101≡1 (mod 4), its periodic correlations are C(k)=−1+2χ(k), so the energy is 5(101−1)=500.
- Current record: No current-record survey; this is an explicit classical construction witness.
- Open evidence: The Legendre construction gives a feasible energy 500 at L=101. The checked sources do not establish the status of this exact finite configuration; no inference of openness is made from the absence of a proof in this audit.
- Recomputed: **no**
- Remaining: Locate a primary source for this exact construction and check whether length-101 energy 500 is known optimal or improved.
- Source: https://arxiv.org/abs/1401.2530
- Source: https://arxiv.org/abs/1411.4340
- Source: https://doi.org/10.1016/j.tcs.2009.02.021
- Source checks:
  - https://arxiv.org/abs/1401.2530: Yan, Chen and Li 2014 primary paper presents general binary sequence constructions with low/optimal autocorrelation. Limitation: This does not establish optimality or current-record status for length 101.

### T076

- Status: **pending**
- Parameters: `{"L": 100, "sequence": "first 100 signs from the order-7 LFSR b_{i+7}=b_{i+3} xor b_i, seed (1,0,0,0,0,0,0); map 0→+1, 1→−1"}`
- Scalar: max_{k≠0}|Σ_i s_i s_{i+k mod L}| (minimize)
- Human baseline: A classical order-7 linear-feedback sequence, truncated to 100 signs, gives exact periodic PSL 20 (periodic correlations at shifts 1..99 are directly computable integers).
- Current record: Not exhaustively audited; do not claim current best.
- Open evidence: The former L=101 Legendre PSL=3 is optimal and closed. The replacement L=100 witness is a locally specified truncation with computed PSL 20; this audit did not locate a published human baseline or evidence that the exact length-100 optimization row is unsolved.
- Recomputed: **yes**
- Remaining: Find a published human length-100 baseline and row-specific optimum/status evidence before confirming suitability.
- Source: https://arxiv.org/abs/2104.10477
- Source checks:
  - https://arxiv.org/abs/2104.10477: Dimitrov–Baitcheva–Nikolov 2021 report low-sidelobe binary constructions, including sequence lengths 106–300. Limitation: The chosen L=100 witness is generated by the stated classical LFSR recurrence, not copied from their tables; no optimum claim for L=100.
  - https://arxiv.org/abs/2104.10477: Human low-sidelobe binary sequence literature, supporting the use of explicit LFSR-style human constructions. Limitation: The exact length-100 recurrence witness is stated and scored in this audit, not copied from that paper; it does not establish optimum status.

### T077

- Status: **confirmed_suitable**
- Parameters: `{"L": 64}`
- Scalar: max_{|z|=1}|P(z)|/sqrt(L) (minimize)
- Human baseline: Define P₀=Q₀=1 and Pₙ₊₁=Pₙ+z^(2^n)Qₙ, Qₙ₊₁=Pₙ−z^(2^n)Qₙ. Then P₆ has 64 coefficients in {±1}; the identity |P₆|²+|Q₆|²=128 yields the certified normalized upper bound ||P₆||∞/√64≤√2. This is an upper bound for the explicit witness, not its exact score or the minimum.
- Current record: No exact minimum or latest finite-length record claimed.
- Open evidence: The AlphaEvolve problem remains a construction challenge. Balister et al. prove flat Littlewood polynomials exist for every degree; the cited theorem does not settle the finite degree-63 minimum. The length-64 Rudin–Shapiro witness is an explicit feasible baseline.
- Recomputed: **no**
- Remaining: If an exact score is needed, compute the maximum modulus of this specific polynomial. This is not required for the reported certified upper bound.
- Source: https://annals.math.princeton.edu/wp-content/uploads/annals-v192-n3-p06-s.pdf
- Source: https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html
- Source checks:
  - https://annals.math.princeton.edu/wp-content/uploads/annals-v192-n3-p06-s.pdf: Proposition 4(a) gives |P_t(z)|²+|Q_t(z)|²=2^(t+1) on |z|=1; recursion defines the length-64 construction. Limitation: This gives a certified upper bound, not the exact supremum or finite-size optimum.
  - https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html: Original problem definition and fixed-length search framing. Limitation: Does not certify an optimum.

### T078

- Status: **pending**
- Parameters: `{"L": 63}`
- Scalar: min_{|z|=1}|P(z)|/sqrt(L) (maximize)
- Human baseline: Littlewood 的平坦多项式问题、Odlyzko (2018) 数值构造、Balister et al. 的 Flat Littlewood Polynomials 提供人类基线来源；具体 L 的系数和严格最小模尚须定位。
- Current record: Not required for this relaxed screen; no claim that this is the latest record.
- Open evidence: No primary-source check completed for a specific configuration; do not treat as suitable yet.
- Recomputed: **no**
- Remaining: Need a concrete open parameter, published numeric witness, and explicit check that the cited source does not prove optimality.
- Source: https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html
- Source: https://arxiv.org/abs/1907.09464
- Source checks:
  - https://arxiv.org/abs/1907.09464: Balister et al. prove existence of polynomials with a positive uniform lower modulus for all degrees. Limitation: This existence theorem does not provide a concrete coefficient vector and certified exact minimum modulus for length 63.

### T079

- Status: **confirmed_suitable**
- Parameters: `{"steps": 208, "support": ["-1/4", "1/4"], "nonnegative": true}`
- Scalar: minimize ||f*f||∞ for nonnegative f (minimize)
- Human baseline: 1.5097201507458786
- Current record: No latest record claimed; this is the verified historical witness score.
- Open evidence: Matolcsi–Vinuesa present this as a computational construction, not an optimality theorem; exact witness score 1.5097201507458786. Later human/AI results may improve it.
- Recomputed: **yes**
- Remaining: Confirm exact source equation/normalization and keep latest frontier separate.
- Source: https://arxiv.org/pdf/0907.1379
- Source checks:
  - https://arxiv.org/pdf/0907.1379: Appendix witness for T079; coefficients extracted and objective recomputed with exact rational arithmetic. Limitation: Rationalized printed decimal coefficients; not current record.

### T080

- Status: **confirmed_suitable**
- Parameters: `{"steps": 20, "support": ["-1/4", "1/4"], "nonnegative": true}`
- Scalar: maximize ||f*f||₂²/(||f*f||₁ ||f*f||∞) (maximize)
- Human baseline: 0.8892261730897966
- Current record: No latest record claimed; this is the verified historical witness score.
- Open evidence: Authors state they did not make extensive efforts to maximize and give this as a counterexample, not an optimum.
- Recomputed: **yes**
- Remaining: Keep the recomputed .8892261730897966, not the unrelated later .9015 catalog value.
- Source: https://arxiv.org/pdf/0907.1379
- Source checks:
  - https://arxiv.org/pdf/0907.1379: Appendix witness for T080; coefficients extracted and objective recomputed with exact rational arithmetic. Limitation: Rationalized printed decimal coefficients; not current record.

### T081

- Status: **confirmed_suitable**
- Parameters: `{"steps": 150, "support": ["-1/4", "1/4"], "nonnegative": false}`
- Scalar: minimize max_t |(f*f)(t)| (minimize)
- Human baseline: Signed n=150 witness has positive maximum 1.458105685768 and negative minimum −2.426895802097; under the task max-absolute objective its score is 2.426895802097. A separate nonnegative human witness scores 1.509720150746.
- Current record: No latest record claimed; this is the verified historical witness score.
- Open evidence: The source gives constructions only, no optimality proof. Critical correction: 1.4581 is a one-sided positive peak, not the maximum absolute convolution.
- Recomputed: **yes**
- Remaining: Freeze whether negative functions are allowed; if allowed, score max absolute value 2.426895802097 for this witness.
- Source: https://arxiv.org/pdf/0907.1379
- Source checks:
  - https://arxiv.org/pdf/0907.1379: Appendix witness for T081; coefficients extracted and objective recomputed with exact rational arithmetic. Limitation: This is the signed n=150 witness. Its max-absolute score is 2.426895802097; the positive one-sided maximum 1.458105685768 is not the task score.

### T082

- Status: **confirmed_suitable**
- Parameters: `{"steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1}`
- Scalar: minimize sup_t ∫ f(x)(1−f(x+t)) dx (support intersection) (minimize)
- Human baseline: Haugland (2016): symmetric 51-step function gives upper bound 0.3809268534330870 for the limiting constant.
- Current record: Not exhaustively audited; candidate screen does not claim this baseline is current.
- Open evidence: Haugland presents it as an upper bound; later bounds do not determine the constant.
- Recomputed: **yes**
- Remaining: Already recomputed in the local audit; retain the note that this is a rationalized version of the printed decimals.
- Source: https://arxiv.org/abs/1609.08000
- Source checks:
  - https://arxiv.org/html/1609.08000: Haugland 2016 source and 51-step upper-bound witness. Limitation: Coefficients in the prior recomputation are rationalized from the printed decimals; score is verified for that rationalized witness.
  - research/baseline_examples/recomputed_examples.json: Exact rational all-shift cross-correlation for the rationalized 51-bin witness. Limitation: Local repository artifact, not Haugland original machine file.

### T083

- Status: **confirmed_suitable**
- Parameters: `{"shift_interval": "[0,1]", "construction": "step-function example induced by the difference basis {0,1,4,6}", "normalization": "L1 mass 1"}`
- Scalar: min_{0<=t<=1} ∫f(x)f(x+t)dx / ||f||_1² (maximize)
- Human baseline: Barnard–Steinerberger/Kravitz difference-basis construction gives min_{0≤t≤1}∫f(x)f(x+t)dx=3/8 for the step-function example induced by the ruler {0,1,4,6}. This exceeds the older 0.37 example.
- Current record: No frontier claim; a 2026 exploratory source lists stronger AI/computational construction, which is outside a human-only baseline.
- Open evidence: The cited papers give explicit feasible constructions, not an exact sharp constant. Kravitz relates difference bases to this continuous objective. A later source lists a larger 2026 step-function value; do not claim 3/8 is current.
- Recomputed: **no**
- Remaining: Retrieve the exact step-function expression and verify its L1 normalization before freezing; exclude 2026 AI-derived construction from the human baseline column.
- Source: https://arxiv.org/abs/1903.08731
- Source: https://arxiv.org/abs/2004.06611
- Source checks:
  - https://arxiv.org/abs/1903.08731: Barnard–Steinerberger state the min-shift autocorrelation problem and its explicit difference-basis construction context. Limitation: Abstract gives the upper-bound formulation but not the exact ruler step-function expression.
  - https://arxiv.org/abs/2004.06611: Kravitz proves the dual link between generalized difference sets and nonnegative autocorrelation integrals. Limitation: Abstract does not display the {0,1,4,6} step-function calculation.

### T084

- Status: **confirmed_suitable**
- Parameters: `{"dimension": 1, "Fourier_transform": "Cohn–Gonçalves convention"}`
- Scalar: minimize A(f)A(f̂), an upper bound on the sharp constant (minimize)
- Human baseline: Gonçalves–Oliveira e Silva–Steinerberger (2016), Theorem 2 and §4.2: f=Σ_{n=0}^3 αₙH_{4n}(√(2π)x)e^(−πx²), with α₀=−113/100, α₁=1/25, α₂=1/3240, α₃=(−α₀−12α₁−1680α₂)/665280, is self-Fourier and gives A(f)A(f̂)≤0.353 (largest root ≈0.59354). The paper also proves 0.2025≤C and shows the upper bound is not sharp.
- Current record: A later Cohn–Gonçalves human upper bound 0.32831 is listed by the original problem page; this audit uses the fully retrieved 2016 explicit construction as baseline and makes no current-record claim.
- Open evidence: The 2016 primary theorem proves 0.2025≤C and proves 0.353 cannot be the sharp lower constant; therefore the exact sharp constant is strictly below the feasible upper bound and remains undetermined by that result. The later 0.32831 improves the human upper bound, but is likewise not the exact constant.
- Recomputed: **no**
- Remaining: For a stronger human baseline use Cohn–Gonçalves 0.32831 after locating and checking its full construction; current suitable baseline is the exact 2016 published example.
- Source: https://arxiv.org/html/1602.03366
- Source: https://arxiv.org/abs/1712.04438
- Source: https://raw.githubusercontent.com/google-deepmind/alphaevolve_repository_of_problems/main/problems/11.html
- Source checks:
  - https://arxiv.org/html/1602.03366: Theorem 2 states lower bound 0.2025 and upper example 0.353; §4.2 gives explicit Hermite coefficients, self-Fourier property and largest root ≈0.59354. Limitation: This is not the strongest known human upper bound and not an exact solution.
  - https://arxiv.org/abs/1712.04438: Cohn–Gonçalves primary source associated with later 0.32831 bound, as listed on problem page. Limitation: Full explicit construction was not retrieved in this pass.

### T085

- Status: **confirmed_suitable**
- Parameters: `{"dimension": 3, "bound_type": "Cohn–Elkies radial LP"}`
- Scalar: Normalized linear-programming upper bound C(d) (minimize)
- Human baseline: Cohn–Elkies (2003), Table 3, dimension 3: the radial LP gives center-density upper bound 0.18616 (packing density ≈0.7797). The FCC packing has density 0.7404804897. The published LP certificate uses a polynomial times Gaussian with m=5 forced roots; exact recipe is in Tables 3–4 and the paper says rational arithmetic and Sturm checks certify it.
- Current record: The d=3 packing optimum itself is FCC at density 0.7404804897; the Cohn–Elkies LP bound 0.7797 is an upper bound, not a packing density.
- Open evidence: Cohn–Elkies Table 3 provides a concrete d=3 LP feasible bound. The 3D packing is solved by Hales, but the LP bound is not sharp. Rupert Li (2025) proves the Cohn–Elkies LP cannot come close to the known d=3 packing density, so this row concerns optimizing the LP method, not solving packing.
- Recomputed: **no**
- Remaining: Do not present 0.7797 as the packing optimum. If the task needs a reproducible certificate, transcribe Table 4 d=3 roots and use the paper’s exact-rational/Sturm verification procedure.
- Source: https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html
- Source: https://arxiv.org/abs/math/0110009
- Source: https://arxiv.org/abs/1603.04246
- Source: https://arxiv.org/abs/1603.06518
- Source checks:
  - https://dash.harvard.edu/server/api/core/bitstreams/7312037c-5608-6bd4-e053-0100007fdf3b/content: Cohn–Elkies Tables 3–4: dimension 3 center-density upper bound 0.18616 and parameters for the certificate; paper says exact rational arithmetic and Sturm theorem certify signs. Limitation: The printed bound is an LP feasible upper bound and is not the exact optimal packing density.
  - https://www.sciencedirect.com/science/article/pii/S0001870824005590: Rupert Li (2025) gives dual bounds proving Cohn–Elkies LP cannot solve d=3 packing. Limitation: Does not determine the exact optimum value of the Cohn–Elkies LP.

### T086

- Status: **pending**
- Parameters: `{"j": 1, "m": 2, "p": 6, "q": 2, "r": 2, "theta": 0.6666666666666666, "dimension": 1}`
- Scalar: ||D^j u||_p / (||D^m u||_r^θ ||u||_q^(1−θ)) for the submitted u (maximize)
- Human baseline: No row-specific human witness and scalar value verified for this admissible exponent tuple. The 2025 primary paper discusses classical inequalities generally; the selected sech profile is a possible explicit test function, but its score has not been computed here.
- Current record: Not independently reconciled to a current authoritative source for this exact parameter choice.
- Open evidence: The former tuple (j=1,m=2,p=2,q=6,r=2,θ=1/4) violates the one-dimensional scaling relation and the condition j/m≤θ. It is invalid and removed. The replacement (1,2,6,2,2,2/3) satisfies 1/p=j+θ(1/r−m)+(1−θ)/q and θ≥j/m. No exact matching sharp-constant theorem was verified; keep pending.
- Recomputed: **no**
- Remaining: Check whether the admissible (p,q,r)=(6,2,2), θ=2/3 sharp constant is known, including Del Pino–Dolbeault families. If a sharp theorem settles this exact tuple, exclude it; otherwise retrieve a concrete human test function and score.
- Source: https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html
- Source: https://arxiv.org/abs/2511.02864
- Source: https://arxiv.org/abs/1611.00734
- Source checks:
  - https://arxiv.org/abs/2511.02864: Primary paper metadata and abstract confirm the paper studies mathematical construction problems. Limitation: Abstract does not state the row-specific exponents or sharp constant; specific page source is not rendered by the browser.
  - https://arxiv.org/abs/1611.00734: Primary paper reviews L2 Gagliardo–Nirenberg constants and maximizers for selected exponent families. Limitation: No verification yet that its sharp families include the replacement (6,2,2), θ=2/3 tuple.
  - https://raw.githubusercontent.com/google-deepmind/alphaevolve_repository_of_problems/main/problems/15.html: Saved source extract states the exact scale relation and theta constraint. Limitation: Its prior fixed tuple in this audit violated both; replacement tuple is valid but no sharp constant has been matched.

### T087

- Status: **pending**
- Parameters: `{"sphere_dimension": 2, "harmonic_degree": 6, "p": 4}`
- Scalar: ||u||_p/||u||_2 for the submitted spherical harmonic (maximize)
- Human baseline: A concrete test function is the degree-6 zonal harmonic u(x)=P₆(x₃) on S², where P₆(t)=(231t⁶−315t⁴+105t²−5)/16. Under normalized surface measure, ||u||₂²=1/13 and ||u||₄⁴=431667/26558675; these provide a feasible lower bound for the maximum ratio. This local integral calculation is not a published best-value claim.
- Current record: Not required for this relaxed screen; no claim that this is the latest record.
- Open evidence: The concrete harmonic baseline is available, but the fixed (dimension 2, degree 6, p=4) row has not been checked against the cited primary paper for an exact optimum or a newer human bound; status remains pending.
- Recomputed: **yes**
- Remaining: Check the primary harmonic extremal paper and calculate the exact ratio from the displayed moments; determine whether this finite row is already solved.
- Source: https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html
- Source: https://arxiv.org/abs/2511.02864
- Source checks:
  - https://arxiv.org/abs/2511.02864: The problem page identifies the spherical-harmonic extremal task; the AlphaEvolve paper is a later comparison source. Limitation: No exact human degree-6, p=4 coefficient vector or score was retrieved.

### T088

- Status: **confirmed_suitable**
- Parameters: `{"curve_length": "2π", "curve": "strictly convex closed oval"}`
- Scalar: λ0(Hγ) (minimize)
- Human baseline: The circle has κ≡1 on length 2π, so the operator is −d²/ds²+1 and its lowest periodic eigenvalue is exactly 1. Benguria–Loss (2004) use the circle as an equality case for the upper bound; later work reports a lower bound below 1.
- Current record: No current-record claim; cited literature leaves a gap between the lower bound and the circle upper bound.
- Open evidence: The circle gives C≤1. Linde (2015) is cited for a lower bound below 1; no equality/optimality theorem for all ovals was identified.
- Recomputed: **no**
- Remaining: Need a concrete open parameter, published numeric witness, and explicit check that the cited source does not prove optimality.
- Source: https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html
- Source: https://doi.org/10.1007/s00023-004-0186-8
- Source: https://arxiv.org/abs/2511.02864
- Source checks:
  - https://doi.org/10.1007/s00023-004-0186-8: Primary Benguria–Loss paper citation for the circle/equality family. Limitation: The tool did not expose the DOI page text; source-level details need full-text retrieval.
  - https://arxiv.org/abs/2511.02864: Primary AlphaEvolve paper as a later comparison source for the oval bounds. Limitation: AI result provenance must remain separate from human construction.

### T089

- Status: **confirmed_suitable**
- Parameters: `{"n": 29, "entries": "±1"}`
- Scalar: maximize |det A| (maximize)
- Human baseline: Solomon/Orrick construction: |det A|=320·7^12·2^28. Brent hosts compressed/full Gram matrix and 4,918 known H-classes.
- Current record: Not exhaustively audited; candidate screen does not claim this baseline is current.
- Open evidence: Brent explicitly calls the Gram matrix conjecturally D-optimal; no proof of global optimality is claimed. High risk: record may already be optimal.
- Recomputed: **no**
- Remaining: Candidate only, high-risk. Suitable only if the goal is to improve a feasible record; not a likely breakthrough.
- Source: https://maths-people.anu.edu.au/~brent/maxdet/order29/
- Source checks:
  - https://maths-people.anu.edu.au/~brent/maxdet/order29/: Solomon/Orrick construction: |det A|=320·7^12·2^28. Brent hosts compressed/full Gram matrix and 4,918 known H-classes. Limitation: Source page inspected; full witness not downloaded/recomputed unless stated.

### T090

- Status: **confirmed_suitable**
- Parameters: `{"dimension": 9, "lattice_class": "Bravais lattices"}`
- Scalar: Packing density (equivalently inverse covolume at fixed minimum distance) (maximize)
- Human baseline: Kallus (2013), Table 1: dimension-9 lattice Λ₉ has normalized cell volume 2⁹v=16√2. For radius-1/2 spheres this gives density Δ₉=(π^(9/2)/Γ(11/2))/(16√2). The paper reports de novo numerical rediscovery, not a proof of optimality.
- Current record: Kallus labels Λ₉ the densest known lattice and gives cell volume; this is not an exhaustive 2026 current-record audit.
- Open evidence: The primary paper states lattice optima are known through d=8 and d=24, and that d>8 enumeration becomes impractical. Its d=9 result is a numerical construction.
- Recomputed: **no**
- Remaining: Retrieve the Λ₉ Gram/generator matrix from the cited lattice catalogue before freezing a verifier witness; density formula follows from the published cell volume.
- Source: https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/
- Source: https://arxiv.org/abs/1603.04246
- Source: https://arxiv.org/abs/1603.06518
- Source checks:
  - https://arxiv.org/html/1305.1310v2: Full paper: identifies Λ₉, cell volume and densest-known status; states lattice optima known through dimensions 8 and 24. Limitation: The HTML table gives no generator matrix; the source itself does not claim proof of d=9 optimality.

### T092

- Status: **confirmed_suitable**
- Parameters: `{"degree": 8, "roots": "8th roots of unity", "weights": "one-hot convex weight at a root"}`
- Scalar: min_j |Σ_k l_k z_k−w_j| for the submitted polynomial and weights (maximize)
- Human baseline: For P(z)=z⁸−1, choose the convex combination equal to a root. Its nearest critical point is 0, at distance 1. Thus C(8)≥1; this is an explicit human lower-bound witness.
- Current record: Not independently reconciled to a current authoritative source for this exact parameter choice.
- Open evidence: The fixed row has a feasible lower-bound construction C(8)≥1. The universal upper bound C(8)≤1 was not verified; the source literature treats C(n)=1 as Schmeisser’s conjecture.
- Recomputed: **no**
- Remaining: Check whether a post-2026 proof settles C(8)≤1 before release; do not treat the conjectured value as a verified optimum.
- Source: https://raw.githubusercontent.com/google-deepmind/alphaevolve_repository_of_problems/main/problems/21.html
- Source: https://arxiv.org/abs/2601.16102
- Source checks:
  - https://raw.githubusercontent.com/google-deepmind/alphaevolve_repository_of_problems/main/problems/21.html: Saved task page gives the exact convex-combination problem and labels C(n)=1 as Schmeisser’s conjecture in the research catalog. Limitation: Page itself does not resolve the conjecture.
  - https://arxiv.org/abs/2601.16102: 2026 primary paper gives only a partial result toward Schmeisser’s conjecture, not a general resolution. Limitation: Does not state the exact n=8 constant.

### T093

- Status: **confirmed_suitable**
- Parameters: `{"degree": 5, "p": 1}`
- Scalar: h(P)=min_{P′(z)=0} min_{P(α)=0}|z−α| (maximize)
- Human baseline: P(z)=z⁴(z+5), obtained from the 2011 human example P=z(z−1)^(n−1) by translation and scaling. Its roots are −5 and 0 (multiplicity 4); its critical points are −4 and 0 (multiplicity 3). The nearest root to −4 is at distance 1, so h(P)=1.
- Current record: No current-record survey; this is a specific feasible human construction.
- Open evidence: The p=2 quadratic variance bound is solved by 2026 papers, so the prior p=2 configuration is closed. Replaced by p=1, degree 5. The 2011 source gives the family P=z(z−1)^(n−1), and reports only the cubic p=1 case as solved; the cited 2026 results concern p≥2. No exact degree-5 p=1 optimum was identified.
- Recomputed: **yes**
- Remaining: Check whether a degree-5 p=1 optimum or stronger human baseline is known; no current-best claim is made.
- Source: https://www.math.vanderbilt.edu/saffeb/texts/231.pdf
- Source: https://arxiv.org/abs/2610.02035
- Source: https://arxiv.org/abs/2610.12499
- Source checks:
  - https://www.math.vanderbilt.edu/saffeb/texts/231.pdf: Example 1 gives the human polynomial family P=z(z−1)^(n−1); p=1 discussion identifies the cubic case as solved. Limitation: Does not establish the degree-5 p=1 optimum.
  - https://arxiv.org/abs/2610.02035: Teng–Zhang (2026) prove the p=2 quadratic variance bound. Limitation: Applies to p≥2; does not solve p=1.
  - https://arxiv.org/abs/2610.12499: Bouthat–Fallat (2026) prove the quadratic variance bound. Limitation: Applies to p≥2; does not solve p=1.

### T094

- Status: **pending**
- Parameters: `{"n": 4, "m": 4, "matrix_dimension": 2, "norm": "operator norm"}`
- Scalar: [n^(−m) Σ_{j1,…,jm} ||A_j1⋯A_jm||] / [((n−m)!/n!) Σ_{distinct j1,…,jm} ||A_j1⋯A_jm||] (minimize)
- Human baseline: Take all A₁,…,A₄=I₂. Every length-4 product has norm 1. There are 4⁴ ordered terms in the numerator and 4! distinct terms in the denominator; with prefactors 4⁻⁴ and 0!/4!, respectively, both averages equal 1, so the quotient is 1.
- Current record: No record claim; concrete feasible construction only.
- Open evidence: The former m=2 row is solved by Israel–Krahmer–Ward for m≤3. The replacement m=4 identity-matrix construction gives feasible quotient 1, but no checked source establishes whether the n=m=4 optimum is known or open.
- Recomputed: **yes**
- Remaining: Locate public human construction/status evidence for n=m=4 and check whether quotient 1 is optimal or improved.
- Source: https://arxiv.org/abs/1411.0333
- Source checks:
  - https://arxiv.org/abs/1411.0333: Primary theorem covers products of up to three matrices, so it closes former m=2 row but not m=4. Limitation: Does not prove the m=4 row open.
  - https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html: Original matrix AM-GM objective and problem parameterization. Limitation: Does not establish a m=4 optimum.

### T095

- Status: **confirmed_suitable**
- Parameters: `{"degree": "unbounded", "class": "monic irreducible non-cyclotomic integer polynomials"}`
- Scalar: minimize Mahler measure M(P) (minimize)
- Human baseline: Lehmer (1933) polynomial x^10+x^9−x^7−x^6−x^5−x^4−x^3+x+1 has M≈1.176280818.
- Current record: Mossinghoff database (updated 2026-07-18) lists BestByDegree_200 and small-measure records; global minimum across unbounded degree remains open.
- Open evidence: Lehmer’s problem asks for minimum Mahler measure over unbounded degree. The 2026 Mossinghoff database reports minima by even degree only through 200, not a proof of the global minimum. The degree-10 row alone is excluded; the unbounded-degree problem remains the intended configuration.
- Recomputed: **no**
- Remaining: Confirmed as an unbounded-degree search problem; a finite search budget does not establish global optimality.
- Source: https://github.com/mossinghoff/Mahler-Measure-Database
- Source: https://doi.org/10.2307/1968172
- Source checks:
  - https://github.com/mossinghoff/Mahler-Measure-Database: Michael Mossinghoff repository README, updated 18 July 2026, defines BestByDegree_200 and lists BestMeasures/AllSmallMeasures datasets. Limitation: Data rows not yet downloaded; Lehmer polynomial exact coefficients from classical 1933 source.
  - https://doi.org/10.1080/10586458.2008.10128872: Parent supplied primary reference by Mossinghoff, Rhin, Wu for even degrees through 54. Limitation: This specific primary theorem not opened by this agent.

### T096

- Status: **confirmed_suitable**
- Parameters: `{"degree": "unbounded", "set": "[0,1]"}`
- Scalar: t_Z([0,1])=inf_{nonzero P∈Z[x]} ||P||_[0,1]^(1/deg P) (minimize)
- Human baseline: P(x)=x(1−x) has integer coefficients and ||P||_[0,1]=1/4, so ||P||^(1/2)=1/2. This is a feasible global upper bound, not the optimum. Pritsker reports global bounds about 0.4213–0.423; the exact constant remains unknown.
- Current record: Global constant is bounded in the cited literature; no claim that the feasible value 1/2 is best.
- Open evidence: Pritsker reports degree≤75 as resolved and gives global lower and upper bounds around 0.4213–0.423, leaving the unbounded-degree constant unresolved. The previous degree-at-most-10 configuration was therefore inappropriate.
- Recomputed: **yes**
- Remaining: Preserve the global interval as a reported bound and 1/2 as a simple feasible construction; verify exact values against the full paper before any record claim.
- Source: https://arxiv.org/abs/math/0101166
- Source: https://math.okstate.edu/people/igor/intcheb.pdf
- Source checks:
  - https://arxiv.org/abs/math/0101166: Pritsker’s primary paper reports solved exact constants for fixed degrees through 75 and gives bounds for the global integer Chebyshev constant on [0,1]. Limitation: The global constant is not identified exactly; the simple witness x(1−x) is not the best known upper bound.
  - https://math.okstate.edu/people/igor/intcheb.pdf: Additional primary exposition on integer Chebyshev constants and global bounds. Limitation: The exact global constant remains unknown.

### T097

- Status: **confirmed_suitable**
- Parameters: `{"target": "2^192−2^64−3 (NIST P-192 field inversion exponent)"}`
- Scalar: shortest addition-chain length l(n) (minimize)
- Human baseline: A public previous chain of length 203 (McLoughlin) and current public chain of length 202 (Brian Smith); both are explicit finite construction records.
- Current record: 202 steps (Clift page, chain downloadable).
- Open evidence: Clift’s page explicitly says none of the listed lengths are proved optimal. It reports the P-192 exponent length 202, versus previous 203.
- Recomputed: **no**
- Remaining: Record provenance carefully: chain is a published computational construction, not independently recomputed here; do not describe as human-only discovery.
- Source: https://additionchains.com/LargeChains.html
- Source: https://additionchains.com/
- Source checks:
  - https://additionchains.com/LargeChains.html: P-192 row, prior length 203, new length 202, downloadable chain, and explicit no-optimality statement. Limitation: Current 202 chain is computationally discovered; not independently replayed here. The primary page itself says not proved optimal.

### T098

- Status: **confirmed_suitable**
- Parameters: `{"target": "2^1000", "grammar": "1s combined by +, ×, parentheses only"}`
- Scalar: minimum number of ones ||n|| (minimize)
- Human baseline: Explicit expression (1+1)×...×(1+1) with 1000 factors gives upper bound ||2^1000||≤2000.
- Current record: No row-specific exact value retrieved.
- Open evidence: The powers-of-two conjecture asks whether ||2^k||=2k for all k. Integer-complexity literature lists it as open; the cited computational work only verifies bounded ranges, not k=1000.
- Recomputed: **no**
- Remaining: Check current primary literature for proof beyond the cited bounded range; preserve the upper bound as a construction, not exact score.
- Source: https://cs.uwaterloo.ca/~shallit/DC2015/iraids2.pdf
- Source: https://arxiv.org/abs/2111.00671
- Source checks:
  - https://cs.uwaterloo.ca/~shallit/DC2015/iraids2.pdf: Open problem statement ||2^n||=2n. Limitation: The PDF is an older source; recent proof-status audit remains needed.

### T099

- Status: **confirmed_suitable**
- Parameters: `{"k": 343, "objective": "minimum diameter admissible k-tuple"}`
- Scalar: minimize max(H)−min(H) (minimize)
- Human baseline: Thomas Engelsma (2013): k=343 admissible tuple of diameter 2340. The supplied local artifact checks 343 distinct entries, the diameter, and residue-class noncoverage for all 68 primes p≤343.
- Current record: No current-record claim. The source table row is unmarked optimal; rows through k=342 are marked optimal.
- Open evidence: MIT/MathBases source row at k=343 has no optimal marker; this is weaker than a proof that no later construction exists. Witness is independently validated locally.
- Recomputed: **yes**
- Remaining: Keep frontier status unclaimed. The artifact verifies admissibility and diameter, not minimality or whether later rows improve it.
- Source: https://mathbases.org/d/narrow-admissible-tuples
- Source checks:
  - https://mathbases.org/d/narrow-admissible-tuples: MathBases / prior MIT tuple database: k=343, diameter 2340, credited to Engelsma (2013); tuple is downloadable. Limitation: Source page inspected; full witness not downloaded/recomputed unless stated.
  - https://math.mit.edu/~primegaps/: Engelsma row k=343, diameter 2340; k≤342 marked optimal in the source data accessed by the lead reviewer. Limitation: A missing optimal marker is not a proof of non-optimality.
  - https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt: Downloaded tuple credited to Engelsma (2013), k=343, diameter 2340; parent audit independently checked 343 distinct values and residue noncoverage for each prime p≤343. Limitation: The tuple verifies feasibility only; database row is unmarked optimal and this is not proof that no smaller diameter exists.

### T100

- Status: **pending**
- Parameters: `{"N": 10001, "factor_count": 10001}`
- Scalar: maximize min_i a_i subject to product a_i=100! (maximize)
- Human baseline: The factorial N! has an explicit factorization into N positive integers: (N!,1,…,1), with N=10001 factors and minimum factor 1. This is a weak but valid human baseline under the stated positive-integer definition.
- Current record: No N=10001 value claimed.
- Open evidence: OEIS A034258 records exact values through N=10000; the checked source gives a(100)=29 and no N=10001 value. This gap alone is not proof of openness. No exact optimum proof for N=10001 was located.
- Recomputed: **yes**
- Remaining: Use the trivial factorization as an admissible baseline only if weak baselines are acceptable; a nontrivial public human witness and row-specific optimum status remain unverified.
- Source: https://oeis.org/A034258
- Source checks:
  - https://oeis.org/A034258: OEIS A034258 records a(100)=29; the linked 1..10000 table lists the row. Limitation: Source page inspected; full witness not downloaded/recomputed unless stated.
  - https://oeis.org/A034258: Exact-value table includes a(100)=29 and is cited through N≤10000. Limitation: Does not provide a value at N=10001 or prove that configuration open.
  - https://math.mit.edu/~drew/GuySelfridge.m: Catalog cites Sutherland’s public human search program. Limitation: Direct retrieval was unavailable in this audit; no N=10001 output validated.
  - https://oeis.org/A034258: Definition uses N positive factors whose product is N!; therefore (N!,1,…,1) is an immediate explicit feasible factorization for N=10001. Limitation: This yields only lower bound 1 and says nothing about the maximum or openness.

### N002

- Status: **confirmed_suitable**
- Parameters: `{"degree": "unbounded", "base_point": 0, "polynomials": "all complex polynomials P with P(0)=0 and P'(0)=1"}`
- Scalar: maximize min_{p′(ζ)=0}|p(ζ)−p(0)|/(|p′(0)||ζ|) (maximize)
- Human baseline: Jatar–Ng (2026) prove a human-authored construction with Smale mean-value constant M>1.1018 and give the global interval 1.1018<M≤4. A simple historical finite witness is P(z)=z^20−z, S(P)=0.95; it is a feasible witness but is weaker than the new global lower bound.
- Current record: Exact global value remains unknown in the checked 2026 paper; lower bound >1.1018 and upper bound 4.
- Open evidence: Jatar–Ng (2026, v2) explicitly states that Smale’s mean-value conjecture M=1 is false, proves M>1.1018 and retains 4 as the best known upper bound. The exact global extremal constant remains undetermined. Do not use Tao’s August 2026 note as evidence that M=1 is still open.
- Recomputed: **no**
- Remaining: Keep AI-assisted provenance attached to the 2026 >1.1018 result. If only human-only provenance is allowed, use the elementary z−z^20/20 family as a weaker feasible witness and label it clearly.
- Source: https://arxiv.org/abs/2610.21472
- Source: https://arxiv.org/abs/1512.02475
- Source checks:
  - https://arxiv.org/abs/2610.21472: Jatar–Ng v2 abstract: M>1.1018, M≤4, arbitrarily large degrees with S(P)>1.1018. Limitation: Does not identify the exact global value; proof development has disclosed AI assistance.
  - https://arxiv.org/html/2610.21472v2: Sections 1.1, 1.3 and 7: exact definition, old conjecture is false, upper bound remains 4, and exact B remains an open determination. Limitation: A concrete high-score polynomial is obtained through an existence construction; the task record does not include its coefficients.

### N004

- Status: **confirmed_suitable**
- Parameters: `{"dimension": 6, "covering": "lattice by congruent balls"}`
- Scalar: minimize lattice covering density Θ (minimize)
- Human baseline: Schürmann–Vallentin: a dimension-6 lattice covering of density 2.900024; dimension 6 is beyond the dimensions where exact optimum is known.
- Current record: Not exhaustively audited; candidate screen does not claim this baseline is current.
- Open evidence: Their work reports new best-known lattices in d=6; review source says the exact lattice optimum is only settled through d=5.
- Recomputed: **no**
- Remaining: Confirmed candidate; retrieve lattice basis and certify density if used.
- Source: https://app.icerm.brown.edu/materials/Slides/sp-s18-w3/Lattice_Coverings_%5D_Mathieu_Dutour_Sikiric%2C_Institut_Rudjer_Boskovic.pdf
- Source checks:
  - https://app.icerm.brown.edu/materials/Slides/sp-s18-w3/Lattice_Coverings_%5D_Mathieu_Dutour_Sikiric%2C_Institut_Rudjer_Boskovic.pdf: Schürmann–Vallentin: a dimension-6 lattice covering of density 2.900024; dimension 6 is beyond the dimensions where exact optimum is known. Limitation: Source page inspected; full witness not downloaded/recomputed unless stated.

### N005

- Status: **confirmed_suitable**
- Parameters: `{"dimension": 13, "lattice": "K12 tensor Z product lattice"}`
- Scalar: minimize normalized second moment G (minimize)
- Human baseline: Agrell–Allen (2023): explicit product lattice NSM 0.071034583; paper says it constructs improved quantizers in d=13.
- Current record: Agrell–Allen Table I: prior best 0.074873919; K12⊗Z product lattice 0.071034583; conjectured lower bound 0.068721956.
- Open evidence: The article gives best-known constructions and no optimality claim for d=13.
- Recomputed: **no**
- Remaining: Confirmed candidate; retrieve factor lattice generators to provide a machine-readable witness.
- Source: https://arxiv.org/abs/2202.09605
- Source checks:
  - https://arxiv.org/abs/2202.09605: Agrell–Allen Table I indexed full text, dimension 13 row: prior best 0.074873919; K12⊗Z product 0.071034583; lower bound 0.068721956. Limitation: Basis/artifact remains to be recovered.

### N006

- Status: **confirmed_suitable**
- Parameters: `{"field": "Q", "tensor": "3×3 matrix multiplication"}`
- Scalar: minimize exact tensor rank (minimize)
- Human baseline: Laderman (1976) gives an explicit rank-23 decomposition over Q; Bläser (2003) proves lower bound ≥19. A later AI-assisted Lean claim ≥21 is separately noted, not counted as human baseline.
- Current record: Not exhaustively audited; candidate screen does not claim this baseline is current.
- Open evidence: No exact rank theorem over Q in the inspected sources; interval at least [19,23] from classical human results. The 2026 F2 result does not settle Q.
- Recomputed: **no**
- Remaining: Confirmed candidate; preserve explicit field distinction and separate AI-assisted proof claims.
- Source: https://www.ams.org/journals/bull/1976-82-01/S0002-9904-1976-13988-2/S0002-9904-1976-13988-2.pdf
- Source checks:
  - https://www.ams.org/journals/bull/1976-82-01/S0002-9904-1976-13988-2/S0002-9904-1976-13988-2.pdf: Laderman (1976) gives an explicit rank-23 decomposition over Q; Bläser (2003) proves lower bound ≥19. A later AI-assisted Lean claim ≥21 is separately noted, not counted as human baseline. Limitation: Source page inspected; full witness not downloaded/recomputed unless stated.

### N007

- Status: **confirmed_suitable**
- Parameters: `{"field": "C", "tensor": "3×3 matrix multiplication"}`
- Scalar: minimize border rank (minimize)
- Human baseline: Smirnov rank-20 degeneration (as cited by Landsberg–Ottaviani); Conner–Harper–Landsberg prove lower bound ≥17.
- Current record: Not exhaustively audited; candidate screen does not claim this baseline is current.
- Open evidence: Primary 2019 paper explicitly states border rank(M3)≥17; reviewed source list gives construction upper bound 20.
- Recomputed: **no**
- Remaining: Confirmed candidate; attach explicit rank-20 degeneration before release.
- Source: https://arxiv.org/abs/1911.07981
- Source checks:
  - https://arxiv.org/abs/1911.07981: Conner–Harper–Landsberg (2019) prove border rank of 3×3 matrix multiplication is at least 17. Limitation: Upper construction 20 is cited in catalog; attach primary Smirnov construction before release.

### N008

- Status: **confirmed_suitable**
- Parameters: `{"rank": 23, "count": "all additions in ordinary coordinates; conversions included"}`
- Scalar: minimize scalar additions/subtractions (minimize)
- Human baseline: A rank-23 56-addition scheme has a public exact implementation; 51-addition alternative-basis kernel plus 5 conversion additions is reported in 2026. AI-assisted 55-addition claim kept separate.
- Current record: Not exhaustively audited; candidate screen does not claim this baseline is current.
- Open evidence: No proof of minimum addition count; published constructions are upper bounds. Basis/counting conventions must remain fixed.
- Recomputed: **no**
- Remaining: Confirmed candidate; freeze standard-coordinate cost model and identify provenance of each witness.
- Source: https://arxiv.org/abs/2604.27645
- Source checks:
  - https://arxiv.org/abs/2604.27645: A rank-23 56-addition scheme has a public exact implementation; 51-addition alternative-basis kernel plus 5 conversion additions is reported in 2026. AI-assisted 55-addition claim kept separate. Limitation: Source page inspected; full witness not downloaded/recomputed unless stated.

### N009

- Status: **confirmed_suitable**
- Parameters: `{"field": "C", "form": "generic 4×4 determinant", "power": 4}`
- Scalar: minimize number of fourth-power terms (minimize)
- Human baseline: Johns–Teitler (2020): explicit Waring decomposition upper bound d·d!=96 for d=4. Derksen–Teitler (2015) lower bound 50.
- Current record: Not exhaustively audited; candidate screen does not claim this baseline is current.
- Open evidence: Bounds [50,96] in cited literature; no exact rank claim.
- Recomputed: **no**
- Remaining: Confirmed candidate; retrieve decomposition formula and lower-bound reference.
- Source: https://arxiv.org/abs/2004.06158
- Source checks:
  - https://arxiv.org/abs/2004.06158: Johns–Teitler provide explicit power-sum decomposition with upper bound d·d!, yielding 96 for d=4. Limitation: Lower bound 50 is from a separate 2015 paper; not inspected in this pass.
