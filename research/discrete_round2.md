# Discrete construction benchmark research — round 2

Additional candidates requested by the main research pass. Rows are distinct named families, not parameter variants. Entries with `reject` are included to preserve the audit trail and flag natural-scalar/baseline problems. Human baselines are historical papers or databases; no AI result is counted as a human record.

**Inventory:** 21 candidates; 5 accept, 12 conditional, 4 reject.

## Candidate records

### schur-number — Schur number S(k) lower-bound coloring

- **Recommendation:** accept — Canonical extremal coloring task with explicit human witnesses, exact small values, and strong proof artifacts.
- **Definition:** For fixed k colors, construct a coloring of [N] with no monochromatic x+y=z; maximize N, the certified lower bound for S(k).
- **Solution / score:** Color assignment [N]→[k] with exact check of all x+y=z; scalar N. Scalar: largest colorable N (maximize).
- **Configuration:** {"colors": "k"}
- **Human baseline:** Heule (AAAI 2018) proved S(5)=160 using a DRAT-certified SAT computation; S(6)≥536 and S(7)≥1680 are cited constructions by Fredricksen–Sweet (2000). Schur numbers S(1..4)=1,4,13,44 are exact.
- **Verification:** Low for lower-bound coloring; proving exact value needs a large SAT/DRAT proof.
- **Risks:** Score a coloring's N only, not an exact S(k) claim absent an upper proof; weak Schur numbers are a separate convention and should be excluded/merged only by explicit scope.
- **Primary sources:** [https://ojs.aaai.org/index.php/AAAI/article/download/12209/12068](https://ojs.aaai.org/index.php/AAAI/article/download/12209/12068); [https://www.cs.utexas.edu/~marijn/Schur/](https://www.cs.utexas.edu/~marijn/Schur/)

### van-der-waerden-lower — van der Waerden number lower-bound coloring

- **Recommendation:** accept — Natural construction objective with published numerical records and cheap witness validation.
- **Definition:** For fixed r colors and AP length k, construct the longest r-coloring of [N] with no monochromatic k-term arithmetic progression.
- **Solution / score:** Coloring of [N]; scalar N. Scalar: largest AP-free coloring order N (maximize).
- **Configuration:** {"colors": "r", "progression_length": "k"}
- **Human baseline:** Marijn Heule's 2005 EJC survey/paper tables W(2,5)=178, W(2,6)=1132 and many best known lower-bound colorings; Berlekamp (1968) and later recurrence constructions provide explicit records.
- **Verification:** Low for a coloring witness by enumerating arithmetic progressions; upper/exact proof is costly.
- **Risks:** Closely related to Ramsey lower-bound construction but a distinct named AP-avoidance family; freeze coloring convention and don't label lower bounds as exact W(r,k).
- **Primary sources:** [https://www.cs.utexas.edu/~marijn/publications/waerden.pdf](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf); [https://arxiv.org/abs/1705.09673](https://arxiv.org/abs/1705.09673); [https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p64](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p64)

### erdos-discrepancy-finite — Longest finite sequence with discrepancy at most C

- **Recommendation:** accept — A named finite extremal version has a concrete human record and exact scalar witness.
- **Definition:** For a fixed discrepancy cap C, find the largest prefix length N of a ±1 sequence such that every homogeneous initial segment along every arithmetic progression has absolute sum at most C.
- **Solution / score:** Sign sequence of length N; exact scalar N. Scalar: sequence length N (maximize).
- **Configuration:** {"discrepancy_cap": "C"}
- **Human baseline:** Konev–Lisitsa (2015) reported a discrepancy-3 sequence of length 127,645, improving 17,000, with inductive construction rules; Tao (2015) proved the infinite Erdős discrepancy conjecture.
- **Verification:** Low for a supplied finite sequence; proving maximality requires exhaustive/combinatorial upper certificates.
- **Risks:** The unbounded infinite theorem itself is not a finite optimization task; freeze exact prefix discrepancy convention and evaluate witness length only.
- **Primary sources:** [https://arxiv.org/abs/1407.2510](https://arxiv.org/abs/1407.2510); [https://arxiv.org/abs/1509.05363](https://arxiv.org/abs/1509.05363)

### ruzsa-szemeredi — Ruzsa–Szemerédi (6,3) graph extremal number

- **Recommendation:** conditional — Canonical active extremal problem with natural scalar, pending verified instance-level numerical records.
- **Definition:** For fixed n, maximize the number of triples in a 3-uniform hypergraph on n vertices such that no six vertices contain three hyperedges (the Brown–Erdős–Sós (6,3) formulation).
- **Solution / score:** 3-uniform hyperedge list; objective number of hyperedges. Scalar: number of hyperedges (maximize).
- **Configuration:** {"vertices": "n"}
- **Human baseline:** Ruzsa–Szemerédi (1976/1978) proved the maximum size of a 3-uniform (6,3)-free system is o(n²); Behrend-type constructions give n² exp(−O(√log n)) lower bounds. These are asymptotic human bounds; no exact finite record table asserted.
- **Verification:** Medium for triangle incidence checks; extremality proof is difficult.
- **Risks:** Use the explicit hypergraph (6,3) definition: every three distinct edges span at least seven vertices. This avoids ambiguity with graph encodings where every edge belongs to a unique triangle.
- **Primary sources:** [https://www.cambridge.org/core/books/abs/surveys-in-combinatorics-2013/graph-removal-lemmas/09C09AB33F6DC2EC895C460F6A31A353](https://www.cambridge.org/core/books/abs/surveys-in-combinatorics-2013/graph-removal-lemmas/09C09AB33F6DC2EC895C460F6A31A353); [https://www.renyi.hu/~szemered/pub.html](https://www.renyi.hu/~szemered/pub.html)

### sum-product-growth — Finite-set sum–product growth minimization

- **Recommendation:** conditional — A real finite optimization scalar, but a standardized published finite benchmark frontier was not confirmed.
- **Definition:** For a fixed size m and a fixed ambient integer interval [B], find A⊂[B], |A|=m minimizing max(|A+A|,|A·A|), with operations in the integers.
- **Solution / score:** Finite integer set A; objective the larger of sumset/product-set cardinalities. Scalar: max(|A+A|,|A·A|) (minimize).
- **Configuration:** {"set_size": "m", "ambient_bound": "B"}
- **Human baseline:** Erdős–Szemerédi (1983) established a power-growth theorem for integer sets; later Solymosi and others improve exponents. No canonical exact finite-n construction table for this min-max objective was verified in this pass.
- **Verification:** Low for a finite set and exact integer operations; global optimum hard.
- **Risks:** Integer interval bound B affects the problem substantially and may be artificial; no verified human optimum table. Restrict to conditional exploratory instances only.
- **Primary sources:** [https://annals.math.princeton.edu/2003/157-3/p07](https://annals.math.princeton.edu/2003/157-3/p07); [https://arxiv.org/abs/math/0402285](https://arxiv.org/abs/math/0402285)

### bh-ruler-higher — Minimum diameter of a B_h set of integers, h≥3

- **Recommendation:** conditional — Natural generalization with human algebraic constructions; finite exact baselines need dedicated verification.
- **Definition:** For fixed m and h≥3, choose m integers with all h-term sums (repetition convention fixed) distinct, minimizing the diameter.
- **Solution / score:** Sorted integer set; objective maximum minus minimum. Scalar: diameter (minimize).
- **Configuration:** {"set_size": "m", "sum order": "h≥3", "repetitions": "fixed by benchmark"}
- **Human baseline:** Bose–Chowla (1962) give finite-field B_h constructions; modern additive-combinatorics papers provide bounds. The h=2 case is the Golomb/Sidon ruler task and is deliberately excluded here as a duplicate.
- **Verification:** Low for witness; exact optimum difficult.
- **Risks:** Must distinguish unordered multisets with repetitions from distinct-element sums and from modular B_h sets; h=2 merges with Golomb rulers.
- **Primary sources:** [https://doi.org/10.1007/BF02566968](https://doi.org/10.1007/BF02566968); [https://arxiv.org/abs/2104.12711](https://arxiv.org/abs/2104.12711)

### finite-kakeya — Minimum finite-field Kakeya set size

- **Recommendation:** conditional — Natural finite extremal objective with strong theory, but exact record data are currently thin.
- **Definition:** For fixed finite field F_q and dimension d, minimize |K| over K⊂F_q^d containing a full affine line in every direction.
- **Solution / score:** Point list or characteristic function; objective |K|. Scalar: number of points (minimize).
- **Configuration:** {"field_order": "q", "dimension": "d"}
- **Human baseline:** Dvir (2009) proved |K|≥c_d q^d by the polynomial method; explicit constructions are known. An October 2026 exposition reports an exact exhaustive result |K|=13 for F_3^3, but that source is secondary, so require primary-paper confirmation before adopting this numeric record.
- **Verification:** Low for candidate set; exact minimum needs exhaustive or mathematical lower bound.
- **Risks:** Small finite cases and field characteristic matter; separate proven minimum from construction upper bound; record 2026 claim as pending primary confirmation.
- **Primary sources:** [https://arxiv.org/abs/0803.2336](https://arxiv.org/abs/0803.2336); [https://arxiv.org/abs/1503.06639](https://arxiv.org/abs/1503.06639)

### arithmetic-kakeya — Arithmetic Kakeya covering-set size

- **Recommendation:** reject — No canonical finite scalar benchmark or record table verified.
- **Definition:** For a precisely fixed k-AP covering formulation, minimize the initial-segment count |A∩[N]| subject to A containing a translate of every required k-term arithmetic progression pattern/direction.
- **Solution / score:** Integer set with finite certificate for a specified range; score cardinality or growth exponent only if canonical formulation is chosen. Scalar: not yet canonical for finite instances (minimize).
- **Configuration:** {"progression_length": "k", "covering convention": "must be specified"}
- **Human baseline:** Katz–Tao introduced the arithmetic Kakeya conjecture; recent work on sparse k-AP covering sets (2026 preprint) disproves a conjecture for k≥6. No standard finite benchmark record is established here.
- **Verification:** Potentially high and dependent on finite truncation.
- **Risks:** As stated in literature this is an asymptotic conjecture, not one settled finite optimization problem; avoid inventing an arbitrary bound.
- **Primary sources:** [https://pmc.ncbi.nlm.nih.gov/articles/PMC6528801/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6528801/); [https://arxiv.org/abs/2609.02041](https://arxiv.org/abs/2609.02041)

### furstenberg-sarkozy — Largest square-difference-free subset of [N]

- **Recommendation:** conditional — Strong named extremal family and human constructions, but current upper-bound citation needs verification and finite record table.
- **Definition:** Maximize |A| for A⊂[N] with no distinct a,b∈A such that |a−b| is a perfect square.
- **Solution / score:** Integer set; objective cardinality. Scalar: number of elements (maximize).
- **Configuration:** {"interval_length": "N"}
- **Human baseline:** Ruzsa (1984) gave an explicit construction of square-difference-free sets; Green–Sawhney (preprint 2024, updated 2025) prove |A|≪N exp(−c√log N). These are asymptotic bounds, not exact finite-N maxima.
- **Verification:** Low for a finite set; proof of maximum difficult.
- **Risks:** Asymptotic rather than exact finite record frontier; parameters N give highly correlated instances.
- **Primary sources:** [https://doi.org/10.1007/BF02454169](https://doi.org/10.1007/BF02454169); [https://arxiv.org/abs/2411.17448](https://arxiv.org/abs/2411.17448)

### no-three-in-line — No-three-in-line maximum on an n×n grid

- **Recommendation:** conditional — Clear scalar and established construction tradition, but candidate records need more authoritative curation.
- **Definition:** Select as many lattice points as possible from [n]×[n] with no three collinear.
- **Solution / score:** Grid point list; objective cardinality. Scalar: number of selected points (maximize).
- **Configuration:** {"grid_order": "n"}
- **Human baseline:** Dudeney posed the problem; constructions of 2n points are known for many n, but the universal 2n conjecture remains open. Wolfram/House of Graphs style databases list configurations; exact finite maxima are only known for selected small n, so a primary record source must be frozen.
- **Verification:** Low for collinearity checks; optimum proof hard.
- **Risks:** Recent preprints and recreational databases may contain construction records without optimality proofs; label upper/lower status carefully.
- **Primary sources:** [https://mathworld.wolfram.com/No-Three-in-LineProblem.html](https://mathworld.wolfram.com/No-Three-in-LineProblem.html); [https://arxiv.org/abs/2209.01447](https://arxiv.org/abs/2209.01447)

### no-isosceles-grid — Maximum no-isosceles-triangle subset of a grid

- **Recommendation:** reject — Insufficient evidence of a canonical published optimization family and record baseline.
- **Definition:** Maximize points in an n×n integer grid subject to no three selected points forming an isosceles triangle (definition includes/excludes collinear triples explicitly).
- **Solution / score:** Point list; objective cardinality. Scalar: number of selected points (maximize).
- **Configuration:** {"grid_order": "n", "degenerate-triples": "fixed convention"}
- **Human baseline:** A primary literature source and maintained numerical record table were not verified in this pass; related integer-grid triangle counting papers do not establish the exact extremal problem's record series.
- **Verification:** Low for finite witness; optimum likely difficult.
- **Risks:** Could be a nonstandard problem formulation; no human baseline evidence yet.
- **Primary sources:** [https://mathweb.ucsd.edu/~asuk/solymosi.pdf](https://mathweb.ucsd.edu/~asuk/solymosi.pdf)

### happy-ending — Erdős–Szekeres happy-ending number f(k)

- **Recommendation:** accept — Named geometric extremal problem with clear scalar and well-documented historic constructions/proof boundary.
- **Definition:** Find the minimum N such that every N points in general position in the plane contain k points in convex position.
- **Solution / score:** For lower-bound witness, coordinates of N−1 points with no convex k-gon; score N−1. Exact f(k) only with matching upper proof. Scalar: largest point-set size avoiding a convex k-gon (maximize).
- **Configuration:** {"convex_subset_size": "k"}
- **Human baseline:** Erdős–Szekeres (1935) proved finiteness and conjectured f(k)=2^{k−2}+1; exact f(3)=3 through f(6)=17 are known, with Peters (2006) computer proof for f(6)=17. Suk (2017) gives f(k)=2^{k+o(k)}.
- **Verification:** Geometric general-position and convexity checks are low with exact coordinates; upper proof is difficult.
- **Risks:** A lower-bound point set is finite and checkable but does not prove f(k); coordinates may be algebraic and need exact predicates.
- **Primary sources:** [https://doi.org/10.1112/jlms/s1-10.1.14](https://doi.org/10.1112/jlms/s1-10.1.14); [https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0EC7876789232266D60439A4C00D86D9/S144618110000300Xa.pdf/computer_solution_to_the_17point_erdosszekeres_problem.pdf](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0EC7876789232266D60439A4C00D86D9/S144618110000300Xa.pdf/computer_solution_to_the_17point_erdosszekeres_problem.pdf); [https://arxiv.org/abs/1604.08657](https://arxiv.org/abs/1604.08657)

### unit-distance — Erdős maximum unit distances for n planar points

- **Recommendation:** conditional — Strong finite exact table through n=21, but a changing frontier and exact-coordinate validation are material.
- **Definition:** Maximize the number of unit-distance pairs among n distinct points in the Euclidean plane.
- **Solution / score:** Exact-coordinate point set; objective unit-distance pair count. Scalar: number of unit-distance pairs (maximize).
- **Configuration:** {"points": "n"}
- **Human baseline:** Alexeev, Mixon & Parshall (2024/2025) report that for n≤21 their upper bounds match best-known lower bounds and fully enumerate densest unit-distance graphs; exact values are thus recorded through 21. No claim about AI-generated or later constructions is used as human baseline.
- **Verification:** Witness edge count is checkable with exact algebraic coordinates; global maximum is hard beyond small n.
- **Risks:** Distinguish exact n≤21 values from open larger n and avoid scoring floating-point near-unit distances; freeze the 2024/2025 paper version and accompanying data.
- **Primary sources:** [https://arxiv.org/abs/2412.11914](https://arxiv.org/abs/2412.11914)

### crossing-kn — Crossing number cr(K_n)

- **Recommendation:** conditional — Natural scalar with long record history, but supplied witness is easy while exact scoring frontier is sparse.
- **Definition:** Minimize the number of edge crossings over all plane drawings of the complete graph K_n.
- **Solution / score:** Drawing or combinatorial rotation/certificate; objective crossing count. Scalar: number of crossings (minimize).
- **Configuration:** {"vertices": "n"}
- **Human baseline:** Guy's conjectured formula is attained by standard drawings and exact values are known only for small n; the general crossing number remains open. Crossing Number project resources survey published lower/upper records.
- **Verification:** High: validating a drawing is straightforward; proving minimality is hard.
- **Risks:** Must score candidate drawing upper bound, not claim optimum; topological drawings and rectilinear drawings are distinct tasks.
- **Primary sources:** [https://uwspace.uwaterloo.ca/items/9b70c74f-2866-459f-a663-7749b4be9bc9](https://uwspace.uwaterloo.ca/items/9b70c74f-2866-459f-a663-7749b4be9bc9); [https://www.crossingnumbers.org/](https://www.crossingnumbers.org/)

### rectilinear-crossing-kn — Rectilinear crossing number of K_n

- **Recommendation:** accept — Standard well-defined geometric optimization with published record configurations and scalar objective.
- **Definition:** Place n points in general position in the plane and minimize the number of crossings in the straight-line drawing of K_n.
- **Solution / score:** Exact coordinates or order type; objective number of crossing edge pairs. Scalar: number of crossings (minimize).
- **Configuration:** {"vertices": "n"}
- **Human baseline:** Exact values are known through small orders (K_9=36, K_10=62 and published tables extend further); Ábrego–Fernández-Merchant and collaborators maintain best-known bounds and constructions; all exact statuses must be frozen from the survey.
- **Verification:** Medium for exact coordinates/order type; proving minimum hard.
- **Risks:** Do not merge with topological crossing number; numerical optimization coordinates need exact orientation tests.
- **Primary sources:** [https://arxiv.org/abs/cs/0009023](https://arxiv.org/abs/cs/0009023); [https://www.csun.edu/~sf70713/publications/survey.pdf](https://www.csun.edu/~sf70713/publications/survey.pdf); [https://www.crossingnumbers.org/projects/crossingconstants/rectilinear.php](https://www.crossingnumbers.org/projects/crossingconstants/rectilinear.php)

### algebraic-connectivity — Maximum algebraic connectivity for fixed n,m

- **Recommendation:** reject — No verified human extremal record database for the proposed unrestricted configuration.
- **Definition:** Among simple graphs on n vertices and m edges, maximize the second-smallest Laplacian eigenvalue λ₂.
- **Solution / score:** Graph adjacency list; objective λ₂, represented by an exact algebraic number or certified interval. Scalar: second Laplacian eigenvalue λ₂ (maximize).
- **Configuration:** {"vertices": "n", "edges": "m"}
- **Human baseline:** Fiedler introduced algebraic connectivity (1973), and extremal results exist for restricted graph classes; no broad finite n,m record database or canonical exact baseline was verified here.
- **Verification:** Medium for numerical eigenvalue; exact comparison of algebraic eigenvalues can be expensive.
- **Risks:** The source currently supports the invariant, not the fixed-(n,m) extremal table; arbitrary finite optimization may be an algorithm benchmark rather than mathematical construction benchmark.
- **Primary sources:** [https://www.dml.cz/handle/10338.dmlcz/101168](https://www.dml.cz/handle/10338.dmlcz/101168)

### finite-group-sumfree — Maximum sum-free set in a specified finite abelian group

- **Recommendation:** conditional — Natural finite-group cardinality optimization and classical results, but overlaps existing sum-free family and many orders have direct formulas.
- **Definition:** For a given finite abelian group G, maximize |A| subject to no x,y,z∈A with x+y=z, with convention allowing x=y.
- **Solution / score:** Group element list; objective cardinality. Scalar: set cardinality (maximize).
- **Configuration:** {"group": "explicit finite abelian group G"}
- **Human baseline:** Diananda–Yap (1969) classified maximum sum-free set sizes for finite abelian groups; for cyclic groups of odd order the maximum is (|G|−1)/3, while even-order cases can attain |G|/2. Exact extremal structures are known in many cases.
- **Verification:** Low for witness; proving maximum uses group-specific theorems.
- **Risks:** Do not count separately from the first-round broad sum-free candidate; replace that entry with this canonical group formulation if accepted.
- **Primary sources:** [https://doi.org/10.3792/pja/1195520891](https://doi.org/10.3792/pja/1195520891); [https://doi.org/10.1112/jlms/s1-44.1.131](https://doi.org/10.1112/jlms/s1-44.1.131); [https://academic.oup.com/qjmath/article/75/3/1057/7732560](https://academic.oup.com/qjmath/article/75/3/1057/7732560)

### ruzsa-sum-difference — Finite-set sum-versus-difference extremal ratios (Ruzsa problems)

- **Recommendation:** reject — The referenced Ruzsa sum/difference results are distinct inequalities/theorem problems, not a single canonical scalar construction family.
- **Definition:** Ruzsa's papers study several distinct questions comparing |A+B|, |A−B|, and related sumsets under constraints such as |A+B|≤K|A|; each requires a separately stated finite extremal objective.
- **Solution / score:** Not specified as a single common witness because the cited papers pose multiple inequivalent questions. Scalar: no canonical shared scalar (varies).
- **Configuration:** {"sets": "A,B in a specified abelian group", "constraint": "paper-specific"}
- **Human baseline:** Gyarmati–Hennecart–Ruzsa (2009) bound |A−B| under a small-sumset condition; Bergelson–Ruzsa (2009) address density and difference-set containment. These are theorem questions, not one finite benchmark record series.
- **Verification:** Depends on reformulation.
- **Risks:** Do not invent 'Sum-difference I/II/III' labels or turn a theorem statement into a finite optimization task without checking original named questions.
- **Primary sources:** [https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf](https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf); [https://people.dm.unipi.it/dinasso/ULTRABIBLIO/Bergelson_Ruzsa%20-%20Sumsets%20in%20difference%20sets%20%282009%29.pdf](https://people.dm.unipi.it/dinasso/ULTRABIBLIO/Bergelson_Ruzsa%20-%20Sumsets%20in%20difference%20sets%20%282009%29.pdf)

### distinct-distances — Minimum distinct distances among n planar points

- **Recommendation:** conditional — Canonical geometric optimization with constructions and bounds, but no broad exact record table.
- **Definition:** Choose n distinct points in the plane minimizing the number of distinct pairwise Euclidean distances.
- **Solution / score:** Exact-coordinate point set; objective number of distinct distances. Scalar: number of distinct distances (minimize).
- **Configuration:** {"points": "n"}
- **Human baseline:** Erdős (1946) gave the square-lattice upper construction; Guth–Katz (2010) proved a lower bound Ω(n/log n). Exact values generally unknown; the lattice gives a concrete human candidate for each n.
- **Verification:** Medium for exact algebraic distance equality; proving optimum hard.
- **Risks:** Score a realized upper-bound count; distinguish this min-distance-count problem from maximum multiplicity of one unit distance.
- **Primary sources:** [https://arxiv.org/abs/1011.4105](https://arxiv.org/abs/1011.4105); [https://petruconstantinescu.github.io/part3_essay.pdf](https://petruconstantinescu.github.io/part3_essay.pdf)

### heilbronn — Heilbronn triangle problem in the unit square

- **Recommendation:** conditional — Very clear continuous-geometric scalar and known explicit configurations, but the current record table source is secondary; verify cited primary results per n before acceptance.
- **Definition:** Place n points in the unit square maximizing the minimum area of a triangle determined by any three points.
- **Solution / score:** Exact coordinates; scalar minimum triangle area. Scalar: minimum triangle area (maximize).
- **Configuration:** {"points": "n", "container": "unit square"}
- **Human baseline:** Chen–Zeng proved the optimal 7-point value after a computer-assisted subdivision; specialist tables collect best-known configurations for several n, including coordinates. The square, triangle and disk formulations are separate container choices, not separate tasks here.
- **Verification:** Low for exact coordinates; global optimum proof high beyond small n.
- **Risks:** Some online tables are community maintained; verify each baseline from cited paper and use exact arithmetic, not floating tolerance.
- **Primary sources:** [https://math.tejstead.com/heilbronn/](https://math.tejstead.com/heilbronn/); [https://oeis.org/A343851](https://oeis.org/A343851)

### erdos-rogers — Erdős–Rogers function f_{s,t}(n)

- **Recommendation:** conditional — A recognized graph extremal function with natural scalar, but poor witness-only evaluation and no curated finite database confirmed.
- **Definition:** For fixed 2≤s<t, maximize the independence number α(G) over n-vertex K_s-free graphs G.
- **Solution / score:** Graph witness and independent set; score α(G). Scalar: independence number (maximize).
- **Configuration:** {"vertices": "n", "forbidden_clique": "s", "independent_set_forbidden_size": "t (target alpha < t)"}
- **Human baseline:** Erdős–Rogers introduced the function; extensive probabilistic and explicit bounds are surveyed in recent graph Ramsey literature. Specific finite graph records need source-level validation before use.
- **Verification:** High: candidate independent set gives lower bound, but certifying α(G) and maximality is hard.
- **Risks:** Carefully define f_{s,t}(n) and distinguish exact α(G) from a supplied independent-set lower bound; may overlap Ramsey graph tasks at t fixed.
- **Primary sources:** [https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf)
