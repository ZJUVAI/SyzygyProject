# Discrete construction benchmark research

Candidate inventory for graph theory, hypergraphs, additive combinatorics, and combinatorial design. Parameters belong in each task configuration; rows are families, not parameter variants. A recommendation of `accept` means a plausible benchmark family, not final inclusion. Historical baselines below are human work; no AI result is substituted. `conditional` entries need instance-level source/baseline curation. `reject` entries document deduplication or scalar-objective exclusions.

**Inventory:** 45 candidates; 10 accept, 15 conditional, 20 reject.

## Candidate records

### graph-cage — (d,g)-cage order

- **Recommendation:** accept — Natural scalar objective, rich named record tables, and independently checkable graph witnesses.
- **Definition:** For fixed degree d and girth g, find the smallest order n of a d-regular graph of girth exactly g.
- **Solution / score:** Adjacency list/matrix of a d-regular graph with a verifiable girth certificate; objective is vertex count. Scalar: number of vertices n (minimize).
- **Configuration:** {"degree": "d", "girth": "g"}
- **Human baseline:** Exoo, Jajcay, Goedgebeur et al. (2025 preprint) improved eleven upper bounds; e.g. n(4,10)≤320. Exoo–Jajcay (2013) survey distinguishes known cages from upper-bound constructions; optimality is proved only for some parameter pairs.
- **Verification:** Medium for a supplied graph; high to prove global minimality.
- **Risks:** Report incumbent order separately from proven minimum; exact optimality certificates are often absent.
- **Primary sources:** [https://arxiv.org/abs/2511.07247](https://arxiv.org/abs/2511.07247); [https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS16](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS16)

### degree-diameter — Degree–diameter problem

- **Recommendation:** accept — A clear extremal objective and extensive human constructions; feasible to score witness size.
- **Definition:** For maximum degree d and diameter k, maximize the order of a simple graph.
- **Solution / score:** Graph adjacency list plus proof/check of maximum degree and diameter; objective vertex count. Scalar: number of vertices n (maximize).
- **Configuration:** {"maximum_degree": "d", "diameter": "k"}
- **Human baseline:** The large degree/diameter graph table (Miller, Širáň and contributors; updated tables) records best known orders and marks the few proven optimal cases; Moore bound is an upper bound, not an attained baseline.
- **Verification:** Medium for witness; exact optimum usually unknown.
- **Risks:** Must label best-known vs proven; table updates and graph conventions (regular vs maximum degree) need freezing.
- **Primary sources:** [https://doi.org/10.17632/d75dzbjd4k.3](https://doi.org/10.17632/d75dzbjd4k.3)

### classical-ramsey — Classical Ramsey number lower-bound construction

- **Recommendation:** conditional — Excellent human baseline and natural scalar, but restrict to modest s,t and require exact verifier/certificate.
- **Definition:** For fixed s,t, construct the largest N-vertex graph with neither an s-clique nor an independent t-set, equivalently improve the lower bound R(s,t)≥N+1.
- **Solution / score:** Graph adjacency list; independently verify forbidden-clique/independent-set conditions; scalar N. Scalar: number of vertices N (maximize).
- **Configuration:** {"clique_size": "s", "independent_set_size": "t"}
- **Human baseline:** Exoo et al. (1997) catalogued 656 nonisomorphic (5,5,42)-graphs, implying R(5,5)≥43; Radziszowski Dynamic Survey rev. 18 (2026) records 43≤R(5,5)≤46, with the upper bound by Angeltveit–McKay (2024).
- **Verification:** High; exact clique and independence checks scale exponentially, though certificates are finite and reproducible.
- **Risks:** A one-unit increase is meaningful but only if exact validation is performed; do not score heuristic estimates or claim exact Ramsey values from a lower-bound witness.
- **Primary sources:** [https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf); [https://users.cecs.anu.edu.au/~bdm/data/ramsey.html](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html); [https://arxiv.org/abs/2409.15709](https://arxiv.org/abs/2409.15709)

### generalized-ramsey — Graph Ramsey number R(G,H)

- **Recommendation:** conditional — Strong literature, but merge with classical Ramsey unless benchmark specifically fixes arbitrary graph pairs.
- **Definition:** Minimum N such that every red/blue coloring of K_N contains red G or blue H; candidates can instead give certified lower-bound colorings on N−1 vertices.
- **Solution / score:** Edge coloring of K_N−1; objective largest certified coloring order. Scalar: coloring order N−1 (maximize).
- **Configuration:** {"forbidden_graphs": "fixed finite graphs G,H"}
- **Human baseline:** Radziszowski Dynamic Survey DS1 (rev. 18, 2026) and Exoo construction tables contain published values and lower-bound colorings.
- **Verification:** High but finite for lower-bound witness; exact value requires separate upper-bound proof.
- **Risks:** Overlaps classical Ramsey task; keep only non-clique forbidden graphs if parameterized as a distinct task family. Exact score cannot be claimed from coloring alone.
- **Primary sources:** [https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf); [https://users.cecs.anu.edu.au/~bdm/data/ramsey.html](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)

### turán-clique — Turán number ex(n,K_r)

- **Recommendation:** conditional — Natural scalar and exact human baseline, but classic cases have closed-form solutions.
- **Definition:** Maximize edges in an n-vertex K_r-free graph.
- **Solution / score:** Simple graph adjacency list; objective edge count. Scalar: number of edges (maximize).
- **Configuration:** {"vertices": "n", "forbidden_clique": "r"}
- **Human baseline:** Turán's theorem (1941) exactly gives the balanced complete (r−1)-partite graph and edge count for all n,r; a calibration item with a formula, not a frontier challenge.
- **Verification:** Low for candidate graph; proving optimality is theorem-level but formula is known.
- **Risks:** Too formulaic for a discovery benchmark; use only calibration, not novelty leaderboard.
- **Primary sources:** [https://people.math.osu.edu/nguyen.1261/6501/Note-extremal.pdf](https://people.math.osu.edu/nguyen.1261/6501/Note-extremal.pdf)

### zaran-bipartite — Zarankiewicz number Z_{s,t}(m,n)

- **Recommendation:** accept — Clean extremal scalar, abundant constructions, and small instances admit exact machine checks.
- **Definition:** Maximize edges in a bipartite graph with part sizes m,n containing no K_{s,t}.
- **Solution / score:** Bipartite adjacency matrix; objective number of 1 entries. Scalar: number of edges (maximize).
- **Configuration:** {"part_sizes": "m,n", "forbidden_biclique": "s,t"}
- **Human baseline:** Published exact values and bounds are surveyed in the extremal graph literature; small square cases have SAT-verified tables (Mubayi et al. / 2022 SAT study corrects known table errors). Explicit finite-field constructions give human lower bounds.
- **Verification:** Medium for forbidden biclique and edge count; optimality high.
- **Risks:** Older tables contain errors; pin a source version and instance. General asymptotics remain open.
- **Primary sources:** [https://arxiv.org/abs/2203.02283](https://arxiv.org/abs/2203.02283); [https://arxiv.org/abs/2202.05507](https://arxiv.org/abs/2202.05507); [https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/BGKRSW96/bgkrsw96.pdf](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/BGKRSW96/bgkrsw96.pdf)

### turan-hypergraph — Hypergraph Turán number ex_r(n,F)

- **Recommendation:** accept — Canonical research problem with natural edge-count objective and published constructions/bounds.
- **Definition:** Maximize edges in an r-uniform n-vertex hypergraph avoiding a fixed forbidden r-graph F.
- **Solution / score:** List of r-subsets; objective edge count. Scalar: number of hyperedges (maximize).
- **Configuration:** {"uniformity": "r", "vertices": "n", "forbidden_hypergraph": "F"}
- **Human baseline:** Keevash's survey and the Erdős problems archive record open cases and constructions. The 3-uniform K4 problem has Turán's construction at density 5/9, but exact density remains open; finite n entries can have exact/conjectured distinctions.
- **Verification:** High; checking F-freeness is manageable for small n, global optimality is difficult.
- **Risks:** Do not blur finite exact values with asymptotic Turán density; choose frozen small n and explicit F.
- **Primary sources:** [https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf](https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf); [https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html)

### saturation — Graph saturation number sat(n,F)

- **Recommendation:** conditional — Natural minimization objective with established theory; curate a small frozen set of nontrivial F,n cases.
- **Definition:** Minimize edges in an n-vertex F-saturated graph: it is F-free, but adding any missing edge creates F.
- **Solution / score:** Graph adjacency list; objective edge count. Scalar: number of edges (minimize).
- **Configuration:** {"vertices": "n", "forbidden_graph": "F"}
- **Human baseline:** Bollobás (1965) initiated the problem; for cliques, classical constructions and recent papers give exact formulas for many ranges. Current papers state the standard definition and bounds.
- **Verification:** Medium for candidate; exact optimum often requires proof.
- **Risks:** Newer specific F parameter results must be checked against publication status; easy families have formulaic answers.
- **Primary sources:** [https://arxiv.org/abs/2605.07179](https://arxiv.org/abs/2605.07179)

### ramsey-graph-max-order — Maximum order of a Ramsey (s,t)-graph

- **Recommendation:** reject — Duplicate formulation of the same Ramsey objective; retain one canonical task.
- **Definition:** For fixed s,t, maximize n such that a graph on n vertices has clique number <s and independence number <t.
- **Solution / score:** Graph adjacency matrix; objective order n. Scalar: number of vertices (maximize).
- **Configuration:** {"clique_size": "s", "independence_size": "t"}
- **Human baseline:** McKay's ANU computational Ramsey database includes explicit graphs and describes the largest known Ramsey graphs; the optimum is R(s,t)−1.
- **Verification:** High for maximality; graph witness checks can be expensive.
- **Risks:** Equivalent to classical Ramsey lower-bound construction; merge into that row to avoid duplicate benchmark.
- **Primary sources:** [https://users.cecs.anu.edu.au/~bdm/data/ramsey.html](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html); [https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf)

### cage-nonregular — Small regular graph of given girth (cage variants)

- **Recommendation:** reject — Parameter/restriction variants of the cage task should be merged.
- **Definition:** Construct a small d-regular graph of girth at least g, possibly with extra restrictions such as bipartite or vertex-transitive.
- **Solution / score:** Graph; minimize order. Scalar: number of vertices (minimize).
- **Configuration:** {"degree": "d", "minimum_girth": "g", "optional_graph_restriction": "fixed restriction"}
- **Human baseline:** Exoo–Jajcay dynamic cage survey and House of Graphs record tables catalog constructions, with restrictions treated separately in papers.
- **Verification:** Medium.
- **Risks:** This is the cage family; do not count variants as separate tasks unless added restriction is canonical and independently studied.
- **Primary sources:** [https://www.combinatorics.org/files/Surveys/ds16/ds16v3-2013.pdf](https://www.combinatorics.org/files/Surveys/ds16/ds16v3-2013.pdf); [https://hog.grinvin.org/](https://hog.grinvin.org/)

### graph-girth-maxedges — Maximum edges under prescribed girth

- **Recommendation:** reject — Broad formulation lacks a verified standard human record table; cage records cover the stronger canonical family.
- **Definition:** For fixed n and girth threshold g, maximize edges in an n-vertex graph with girth at least g.
- **Solution / score:** Graph adjacency list; objective edge count. Scalar: number of edges (maximize).
- **Configuration:** {"vertices": "n", "minimum_girth": "g"}
- **Human baseline:** Erdős–Sachs (1963) established existence of regular graphs of prescribed degree and girth; the cage survey provides named extremal records, but exact max-edge records for this broader fixed-n formulation were not curated in this pass.
- **Verification:** Medium for girth and edge count; optimum difficult.
- **Risks:** A general problem family with sparse centralized records; source and exact instance baseline still need checking.
- **Primary sources:** [https://www.renyi.hu/~p_erdos/1963-16.pdf](https://www.renyi.hu/~p_erdos/1963-16.pdf); [https://doi.org/10.1112/jlms/s1-38.1.423](https://doi.org/10.1112/jlms/s1-38.1.423)

### independence-extremal — Maximum independence number under graph constraints

- **Recommendation:** reject — No single canonical family or practical human baseline; verification burden is high.
- **Definition:** Given a fixed graph class or forbidden subgraph family and order n, maximize alpha(G).
- **Solution / score:** Graph witness; objective independence number. Scalar: independence number (maximize).
- **Configuration:** {"vertices": "n", "graph_class_or_forbidden_family": "fixed class"}
- **Human baseline:** Many individual extremal results exist, but no unified, verified baseline database for arbitrary constraints was established in this survey pass.
- **Verification:** High: exact maximum independent set is NP-hard; validating claimed alpha needs a matching upper certificate.
- **Risks:** Too broad; do not score a heuristic alpha estimate as exact.
- **Primary sources:** [https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf)

### graph-saturation-general — Saturated graph construction for fixed F

- **Recommendation:** reject — Merge into canonical saturation-number task.
- **Definition:** Find an F-saturated graph with few edges on n vertices.
- **Solution / score:** Graph witness; objective edge count. Scalar: number of edges (minimize).
- **Configuration:** {"n": "n", "F": "fixed graph"}
- **Human baseline:** See sat(n,F) literature, but duplicates the saturation number task.
- **Verification:** Medium.
- **Risks:** Duplicate formulation.
- **Primary sources:** [https://arxiv.org/abs/2605.07179](https://arxiv.org/abs/2605.07179)

### covering-design — Covering number C(v,k,t)

- **Recommendation:** accept — One of the strongest candidates: standardized finite objects, natural scalar, and large human record corpus.
- **Definition:** Find the fewest k-subsets of a v-set such that every t-subset is included in at least one selected block.
- **Solution / score:** List of k-subsets; objective block count. Scalar: number of blocks (minimize).
- **Configuration:** {"v": "points", "k": "block size", "t": "covering strength"}
- **Human baseline:** La Jolla Combinatorics Repository (Dan Gordon; frozen 2026) stores tens of thousands of best-known covers and lower bounds; individual construction records identify contributors/methods.
- **Verification:** Low-medium for coverage; proving minimum needs lower bound.
- **Risks:** Repository baseline may be best-known rather than optimum; freeze data snapshot and preserve authorship metadata.
- **Primary sources:** [https://dmgordon.org/ljcr/](https://dmgordon.org/ljcr/); [https://ljcr.dmgordon.org/cover.html](https://ljcr.dmgordon.org/cover.html)

### covering-array — Covering array CAN(t,k,v)

- **Recommendation:** accept — Excellent benchmark corpus and easily verifiable scalar optimization.
- **Definition:** Minimize rows N of a k-column v-ary array so every t selected columns contain every v^t tuple at least once.
- **Solution / score:** N×k array over v symbols; objective N. Scalar: number of rows N (minimize).
- **Configuration:** {"strength": "t", "columns": "k", "levels": "v"}
- **Human baseline:** NIST Covering Array Library lists actual arrays for strengths 2–6 and 2–6 levels, plus best-known sizes to 20,000 columns (strength 2) and 10,000 (strengths 3–6); NIST and Colbourn records are human constructions/bounds.
- **Verification:** Low for explicit array; minimum proof varies.
- **Risks:** Keep uniform alphabet case separate from variable-strength/general mixed-level variants; NIST best-known size tables do not always include arrays.
- **Primary sources:** [https://csrc.nist.gov/Projects/Automated-Combinatorial-Testing-for-Software/Covering-Array-Library](https://csrc.nist.gov/Projects/Automated-Combinatorial-Testing-for-Software/Covering-Array-Library); [https://math.nist.gov/coveringarrays/coveringarray.html](https://math.nist.gov/coveringarrays/coveringarray.html)

### orthogonal-array — Orthogonal array minimum-run construction

- **Recommendation:** accept — Curated human constructions and simple exact validator; good if objective/configuration are fixed consistently.
- **Definition:** For fixed strength t, levels and columns, construct an orthogonal array with the fewest rows (or maximize columns for fixed rows), each t-column tuple appearing equally often.
- **Solution / score:** Array with explicit index lambda; objective rows or columns, with one direction fixed per instance. Scalar: number of rows N (fixed columns/levels/strength/index) (minimize).
- **Configuration:** {"strength": "t", "levels": "s or mixed-level vector", "columns": "k", "index": "lambda"}
- **Human baseline:** Neil Sloane's library contains 200+ explicit arrays; Eendebak–Schoen catalogue complete non-isomorphic arrays for selected small parameters. OA( N,k,s,t) must meet divisibility/Rao bounds.
- **Verification:** Low for explicit array; minimality moderate/high.
- **Risks:** Do not conflate OA existence, maximum columns, and minimum-run objectives; fix one scalar per instance. Strength-2 binary OAs are essentially Hadamard matrices.
- **Primary sources:** [https://neilsloane.com/oadir/index.html](https://neilsloane.com/oadir/index.html)

### steiner-system — Steiner system block construction S(t,k,v)

- **Recommendation:** reject — Fails scalar optimization requirement; can be included only as validation/calibration, not scored task.
- **Definition:** Construct k-subsets so each t-subset occurs in exactly one block; the number of blocks is forced by parameters when divisibility holds.
- **Solution / score:** Block list; scalar objective may be block count only if allowing a relaxed/partial design. Scalar: none for exact Steiner existence (block count is forced) (not applicable).
- **Configuration:** {"t": "strength", "k": "block size", "v": "points"}
- **Human baseline:** La Jolla repository links Steiner systems; classical systems (projective planes, Witt designs) have named constructions and authors.
- **Verification:** Low for incidence verification.
- **Risks:** Exact existence is boolean and has no optimization scalar; block count is fixed by counting.
- **Primary sources:** [https://ljcr.dmgordon.org/cover.html](https://ljcr.dmgordon.org/cover.html); [https://dmgordon.org/ljcr/](https://dmgordon.org/ljcr/)

### packing-design — Packing number D(v,k,t)

- **Recommendation:** conditional — Good scalar and verification, but human-record baseline needs further curation.
- **Definition:** Maximize the number of k-subsets on v points such that no t-subset is contained in more than one block.
- **Solution / score:** List of blocks; objective block count. Scalar: number of blocks (maximize).
- **Configuration:** {"v": "points", "k": "block size", "t": "packing strength"}
- **Human baseline:** La Jolla covering repository focuses on coverings, while classical packing bounds and constructions are published; candidate instance-level records require dedicated database/source review.
- **Verification:** Low for packing property.
- **Risks:** No unified current record table confirmed in this pass; may overlap partial Steiner designs.
- **Primary sources:** [https://dmgordon.org/ljcr/](https://dmgordon.org/ljcr/)

### social-golfer — Social golfer maximum schedule length

- **Recommendation:** conditional — Natural schedule objective and benchmark tradition, but require verified per-instance baseline.
- **Definition:** Partition players into groups of fixed size each round, avoiding any pair meeting twice; maximize number of rounds.
- **Solution / score:** Round-by-round partitions; objective number of rounds. Scalar: number of rounds (maximize).
- **Configuration:** {"players": "P", "group_size": "g", "groups_per_round": "fixed/implied"}
- **Human baseline:** CSPLib problem 010 defines the canonical 32 golfers in groups of four and its generalization; published constraint-programming literature reports solved/optimal schedules for small parameter sets, but benchmark records need per-instance capture.
- **Verification:** Low for pair uniqueness; maximality requires a bound/proof.
- **Risks:** Could degenerate into mere feasibility when target rounds fixed; use maximize rounds and instances with documented human optima.
- **Primary sources:** [https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/](https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/); [https://www.csplib.org/Problems/prob010/](https://www.csplib.org/Problems/prob010/)

### latin-mols — Maximum number of mutually orthogonal Latin squares

- **Recommendation:** accept — Canonical extremal design quantity, simple verifier, and substantive human theory.
- **Definition:** For order n, maximize the number of pairwise orthogonal Latin squares (MOLS).
- **Solution / score:** List of Latin squares; objective count. Scalar: number of MOLS (maximize).
- **Configuration:** {"order": "n"}
- **Human baseline:** Bruck–Ryser–Chowla gives nonexistence restrictions; complete values are known for several small orders, while the standard MOLS tables record constructions and bounds.
- **Verification:** Low for square/orthogonality checks; maximality often hard.
- **Risks:** Exact optimum open for some n; source table version and proof status must be frozen.
- **Primary sources:** [https://doi.org/10.4153/CJM-1949-009-2](https://doi.org/10.4153/CJM-1949-009-2)

### hadamard-order — Maximum Hadamard matrix order under a bound

- **Recommendation:** reject — Fixed-instance feasibility is boolean; maximizing order under an arbitrary cap is not a natural standalone optimization benchmark.
- **Definition:** For a fixed search bound M, find the largest order h≤M for which a ±1 matrix has mutually orthogonal rows.
- **Solution / score:** Hadamard matrix; scalar order h. Scalar: matrix order h (maximize).
- **Configuration:** {"order_bound": "M", "optional_structural_class": "e.g. circulant, fixed separately"}
- **Human baseline:** Sloane maintains a library of Hadamard matrices and known orders; Hadamard's determinant bound requires order 1,2 or divisible by 4 above 2, and many orders are constructed by Sylvester/Paley methods.
- **Verification:** Low for witness; proving no larger allowed order is number-theoretic or exhaustive.
- **Risks:** Avoid fixed-order existence boolean benchmark; choose maximize order under a fixed cap and compare with curated library.
- **Primary sources:** [https://neilsloane.com/hadamard/](https://neilsloane.com/hadamard/)

### projective-plane — Projective plane order search

- **Recommendation:** reject — Mostly existence and known algebraic construction; poor natural scalar task.
- **Definition:** For a fixed cap q≤Q, find the largest order q for which a projective plane exists.
- **Solution / score:** Incidence matrix; scalar order q. Scalar: plane order q (maximize).
- **Configuration:** {"order_cap": "Q"}
- **Human baseline:** Prime-power orders have finite-field constructions; Bruck–Ryser (1949) excludes some orders; Lam, Thiel & Swiercz (1989) computationally proved no plane of order 10 exists.
- **Verification:** Low for candidate incidence structure; nonexistence proof can be extremely expensive.
- **Risks:** Underlying task often asks existence at fixed q, a boolean; bounded maximize-q wrapper is artificial and dominated by known prime-power formula.
- **Primary sources:** [https://doi.org/10.4153/CJM-1949-009-2](https://doi.org/10.4153/CJM-1949-009-2); [https://doi.org/10.4153/CJM-1989-049-4](https://doi.org/10.4153/CJM-1989-049-4)

### golomb-ruler — Optimal Golomb ruler length

- **Recommendation:** accept — Ideal scalar objective, a standard benchmark and exceptionally clear historical human record.
- **Definition:** For m integer marks, place distinct marks so all positive pairwise differences are distinct and minimize the largest mark.
- **Solution / score:** Increasing integer mark list starting at 0; objective final mark. Scalar: ruler length (minimize).
- **Configuration:** {"marks": "m"}
- **Human baseline:** Shearer (1990) exhaustively proved optimal lengths 127,151,177 for m=14,15,16; distributed.net completed proof of optimality through m=28 (2022 records), and CSPLib has the standard benchmark. Distinguish proven optima from larger-m best known rulers.
- **Verification:** Low for ruler; optimality proof high for large m.
- **Risks:** Open sizes beyond proven range must be scored as incumbent length, not as proven optimum; preserve provenance and certificate status.
- **Primary sources:** [https://research.ibm.com/publications/some-new-optimum-golomb-rulers](https://research.ibm.com/publications/some-new-optimum-golomb-rulers); [https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob006/](https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob006/); [https://distributed.net/ogr/](https://distributed.net/ogr/)

### difference-triangle — Difference triangle sets

- **Recommendation:** conditional — A legitimate adjacent optimization family with published records, but merge one-row case into Golomb rulers.
- **Definition:** Construct several rows of marks with all within-row positive differences distinct globally; minimize maximum span under fixed row/mark counts.
- **Solution / score:** Rows of integer marks; objective maximum row span. Scalar: maximum span (minimize).
- **Configuration:** {"rows": "r", "marks_per_row": "m"}
- **Human baseline:** Published difference-triangle-set constructions and tabu search literature report best-known spans; Golomb rulers are the one-row special case.
- **Verification:** Low for a witness.
- **Risks:** Overlaps Golomb ruler at r=1; careful definition variants (all differences vs row-tagged) must be frozen.
- **Primary sources:** [https://doi.org/10.1016/j.cor.2004.11.002](https://doi.org/10.1016/j.cor.2004.11.002); [https://cs.uwaterloo.ca/~vanbeek/Publications/sillito.pdf](https://cs.uwaterloo.ca/~vanbeek/Publications/sillito.pdf)

### sidon-interval — Largest Sidon set in [n]

- **Recommendation:** conditional — Very natural scalar and classical constructions; source-level exact benchmark table needs checking.
- **Definition:** Find the largest subset of {1,…,n} whose pairwise sums of distinct elements are all different (equivalently distinct positive differences).
- **Solution / score:** Sorted integer set; objective cardinality. Scalar: set cardinality (maximize).
- **Configuration:** {"interval_length": "n"}
- **Human baseline:** Erdős–Turán (1941) prove the maximum Sidon-set size in [n] is asymptotic to √n; Bose–Chowla (1962) give finite-field constructions. Specific finite-n exact maxima are not asserted here; use a verified construction/bound table before scoring exactness.
- **Verification:** Low for witness; proof of maximum can be difficult.
- **Risks:** Terminology differs on allowing repeated summands; specify pairwise sums of distinct elements and distinct differences explicitly. Exact small-n baseline table still needs verification.
- **Primary sources:** [https://users.renyi.hu/~p_erdos/1944-02.pdf](https://users.renyi.hu/~p_erdos/1944-02.pdf); [https://doi.org/10.1007/BF02566968](https://doi.org/10.1007/BF02566968)

### cap-set — Maximum cap set in F_3^n

- **Recommendation:** accept — Canonical additive extremal problem, clear point-count objective, and unusually visible human construction frontier.
- **Definition:** Find a largest subset of the vector space F_3^n containing no affine line (three distinct points summing to zero).
- **Solution / score:** Point list in F_3^n; objective cardinality. Scalar: number of points (maximize).
- **Configuration:** {"dimension": "n"}
- **Human baseline:** Pellegrino (1970) proved maximum 20 for n=4. Kleinberg–Sawin–Speyer (2016) gave constructions and Ellenberg–Gijswijt (2017) exponential upper bound; human lower-bound records are published for higher n, with exact values limited.
- **Verification:** Low for witness and no-line property; proving optimality difficult.
- **Risks:** Modern record tables may have changed; distinguish exact small dimensions from best-known lower bounds.
- **Primary sources:** [https://doi.org/10.4007/annals.2017.185.1.8](https://doi.org/10.4007/annals.2017.185.1.8); [https://arxiv.org/abs/1605.09223](https://arxiv.org/abs/1605.09223)

### progression-free — Largest 3-term-progression-free subset of [n]

- **Recommendation:** conditional — Natural cardinality objective, but benchmark exact records need authoritative tables and manageable n.
- **Definition:** Find a largest subset of {1,…,n} containing no nontrivial 3-term arithmetic progression.
- **Solution / score:** Integer set; objective cardinality. Scalar: set cardinality (maximize).
- **Configuration:** {"interval_length": "n"}
- **Human baseline:** Behrend (1946) gave classical constructions; exact small-n values are known computationally and Roth's theorem gives qualitative upper bounds. Pin exact-value source/version for each n.
- **Verification:** Low for witness, exponential for maximality.
- **Risks:** Closely related to cap sets but distinct ambient group; avoid treating parameter variants as different tasks.
- **Primary sources:** [https://doi.org/10.1073/pnas.32.12.331](https://doi.org/10.1073/pnas.32.12.331)

### difference-basis — Minimum difference basis for [n]

- **Recommendation:** conditional — Natural minimum-cardinality task but needs definition and authoritative record table curation.
- **Definition:** Find a smallest set A of integers such that every integer 1,…,n is a difference of two elements of A.
- **Solution / score:** Sorted integer set; objective cardinality (or span if a different canonical version is chosen). Scalar: number of elements of A (minimize).
- **Configuration:** {"target_interval": "n", "ambient_domain": "integer interval, fixed convention"}
- **Human baseline:** Difference-basis literature has asymptotic bounds and specific constructions (Rédei–Rényi; Leech), but this pass did not verify an accessible modern exact-record table.
- **Verification:** Low for coverage; proving minimality difficult.
- **Risks:** Several inequivalent definitions (difference set vs difference basis, interval endpoint, signed differences); human baseline source requires additional research.
- **Primary sources:** No primary source confirmed in this pass.

### additive-basis — Minimum additive basis of order h for [n]

- **Recommendation:** reject — Insufficiently canonical and no verified human baseline.
- **Definition:** Find a smallest A⊂[0,m] or minimum largest element such that every target integer up to n is a sum of h elements of A (convention fixed).
- **Solution / score:** Integer set; objective cardinality or maximum element (choose one). Scalar: requires canonical convention (minimize).
- **Configuration:** {"order": "h", "target_range": "n", "sum convention": "repetitions allowed or not"}
- **Human baseline:** Classical additive-basis literature studies several nonequivalent variants; a specific finite database and baseline were not verified in this pass.
- **Verification:** Low-medium for witness; proof of optimality hard.
- **Risks:** Too many incompatible objectives/conventions; no source-backed fixed record table.
- **Primary sources:** No primary source confirmed in this pass.

### sum-free — Maximum sum-free subset of a finite group

- **Recommendation:** conditional — Useful calibration only for interval case; broader version lacks canonical benchmark instances.
- **Definition:** Maximize |A| in a fixed finite abelian group subject to no x,y,z∈A with x+y=z (convention fixed).
- **Solution / score:** Element list; objective cardinality. Scalar: set cardinality (maximize).
- **Configuration:** {"group": "fixed finite abelian group"}
- **Human baseline:** For integers [n], the maximum is floor((n+1)/2), giving an exact calibration; finite group extremal classifications are known in many cases.
- **Verification:** Low for witness, exact optimum varies.
- **Risks:** Integer interval is formulaic; broad finite-group versions need more specific literature and are not one task.
- **Primary sources:** [https://doi.org/10.3792/pja/1195520891](https://doi.org/10.3792/pja/1195520891); [https://doi.org/10.1112/jlms/s1-44.1.131](https://doi.org/10.1112/jlms/s1-44.1.131)

### sum-difference-set — Sum-difference sets in finite groups

- **Recommendation:** reject — No canonical objective or verifiable standard human baseline found.
- **Definition:** For a fixed finite group G and target coverage convention, find a small set A with A+A−A=G or maximize prescribed sum/difference coverage.
- **Solution / score:** Subset A; scalar size or uncovered count only if established optimization target. Scalar: not fixed across literature conventions (varies).
- **Configuration:** {"group": "G", "coverage convention": "must be specified"}
- **Human baseline:** Several related sum-difference problems occur in additive combinatorics, but no canonical single finite optimization record/database was verified here.
- **Verification:** Low for a fixed definition.
- **Risks:** Name covers inequivalent problems; would risk inventing a benchmark objective.
- **Primary sources:** No primary source confirmed in this pass.

### costas-array — Costas array maximal order

- **Recommendation:** reject — Fixed-instance feasibility is boolean; maximizing order under an arbitrary cap is not a natural standalone optimization benchmark.
- **Definition:** Find a largest order n with a permutation whose displacement vectors are all distinct (Costas array).
- **Solution / score:** Permutation; objective order n under a fixed search bound. Scalar: array order n (maximize).
- **Configuration:** {"order_bound": "N"}
- **Human baseline:** Costas arrays are tabulated by order and constructions (Welch, Golomb) are published; finite existence records are maintained by specialist databases.
- **Verification:** Low for witness; proving nonexistence at larger order is difficult.
- **Risks:** Fixed-order form is boolean; bounded maximize-order form may collapse to known constructions. Need a verified authoritative record table.
- **Primary sources:** [https://doi.org/10.1109/TIT.1974.1055329](https://doi.org/10.1109/TIT.1974.1055329); [https://doi.org/10.1109/TIT.1984.1056984](https://doi.org/10.1109/TIT.1984.1056984)

### difference-set — Cyclic difference set construction

- **Recommendation:** reject — No natural optimization scalar for fixed parameters.
- **Definition:** Find a k-subset of a cyclic group of order v whose nonzero differences cover each nonzero group element exactly lambda times.
- **Solution / score:** Residue set; no free scalar because v,k,lambda determine size. Scalar: none for fixed parameters (not applicable).
- **Configuration:** {"v": "group order", "k": "subset size", "lambda": "difference multiplicity"}
- **Human baseline:** La Jolla hosts difference-set data and classical Singer constructions provide examples.
- **Verification:** Low.
- **Risks:** Fixed-parameter existence is boolean; parameters determine the construction size.
- **Primary sources:** [https://dmgordon.org/ljcr/](https://dmgordon.org/ljcr/)

### weighing-matrix — Maximum order weighing matrix under bound

- **Recommendation:** reject — Fixed-instance feasibility is boolean; maximizing order under an arbitrary cap is not a natural standalone optimization benchmark.
- **Definition:** For a fixed order cap and weight ratio/structural class, find the largest order of a weighing matrix W with WWᵀ=kI.
- **Solution / score:** Matrix entries 0,±1; scalar order. Scalar: matrix order (maximize).
- **Configuration:** {"order_bound": "N", "weight": "k", "class": "general/circulant, fixed"}
- **Human baseline:** Dan Gordon's La Jolla data include circulant weighing matrices and record constructions.
- **Verification:** Low for witness; existence/nonexistence frontier varies.
- **Risks:** Different matrix classes and weights must be separated; database data scope needs review.
- **Primary sources:** [https://dmgordon.org/ljcr/](https://dmgordon.org/ljcr/)

### max-matching-hypergraph — Maximum matching-free hypergraph extremal number

- **Recommendation:** conditional — Natural extremal scalar, but needs a canonical instance table and definition pinning.
- **Definition:** Maximize edges in an r-uniform n-vertex hypergraph with matching number below fixed s.
- **Solution / score:** Hyperedge list; objective edge count. Scalar: number of hyperedges (maximize).
- **Configuration:** {"uniformity": "r", "vertices": "n", "matching_limit": "s"}
- **Human baseline:** Erdős matching conjecture and extensive exact results give canonical bounds; recent papers prove exact ranges, but there is no single table verified in this pass.
- **Verification:** Medium for matching number at small n; optimum proof hard.
- **Risks:** Be careful whether Berge matching or disjoint hyperedges; family has multiple conventions.
- **Primary sources:** [https://www.sciencedirect.com/science/article/pii/S0097316514000041](https://www.sciencedirect.com/science/article/pii/S0097316514000041); [https://arxiv.org/abs/2602.19230](https://arxiv.org/abs/2602.19230)

### hypergraph-ramsey — Hypergraph Ramsey lower-bound construction

- **Recommendation:** reject — Merge with Ramsey task and restrict if retained; poor standalone scalability.
- **Definition:** For fixed uniformity and target monochromatic hypergraphs, construct a large coloring avoiding both, maximizing vertex/order count.
- **Solution / score:** Coloring of complete uniform hypergraph; objective number of vertices. Scalar: number of vertices (maximize).
- **Configuration:** {"uniformity": "r", "colors": "q", "forbidden_hypergraphs": "fixed list"}
- **Human baseline:** Radziszowski's Dynamic Survey records classical hypergraph Ramsey values and bounds.
- **Verification:** Very high for larger instances; exhaustive edge coloring verification grows rapidly.
- **Risks:** Overlaps general Ramsey construction; high validation cost and sparse human records.
- **Primary sources:** [https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf](https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf)

### covering-code — Minimum covering code size K_q(n,R)

- **Recommendation:** conditional — Excellent finite scalar optimization, but baseline database must be sourced and frozen.
- **Definition:** Find the fewest q-ary length-n words whose Hamming balls of radius R cover the whole space.
- **Solution / score:** Codeword list; objective code size. Scalar: number of codewords (minimize).
- **Configuration:** {"alphabet": "q", "length": "n", "radius": "R"}
- **Human baseline:** Published covering-code tables (Hill, Heden and collaborators) record lower and upper bounds and constructions; an authoritative unified current database was not verified in this pass.
- **Verification:** Low for full coverage at small n; proof of minimum difficult.
- **Risks:** Source table needs primary-source verification; coding theory scope may overlap another benchmark category.
- **Primary sources:** [https://www.mathonline.dk/coding-theory/covering-codes/](https://www.mathonline.dk/coding-theory/covering-codes/); [https://doi.org/10.1007/978-1-4614-1684-2](https://doi.org/10.1007/978-1-4614-1684-2)

### max-clique-graph-instance — Maximum clique on standard named graph instances

- **Recommendation:** reject — Optimization is canonical but fails the intended construction-discovery flavor and exact upper-certificate burden.
- **Definition:** Find a maximum clique in a fixed published graph instance.
- **Solution / score:** Vertex set; objective clique cardinality. Scalar: clique size (maximize).
- **Configuration:** {"graph": "fixed named graph instance"}
- **Human baseline:** DIMACS challenge graph collection and exact solver literature contain known optimum values for instances.
- **Verification:** High; membership proves lower bound but maximum requires certificate.
- **Risks:** Generic algorithmic benchmark rather than mathematical construction discovery; graph names/instances are inputs, not a coherent theorem family.
- **Primary sources:** [https://dimacs.rutgers.edu/archive/Challenges/](https://dimacs.rutgers.edu/archive/Challenges/)

### max-independent-set-instance — Maximum independent set on standard named graph instances

- **Recommendation:** reject — Does not fit mathematical construction benchmark goal; duplicates optimization contest category.
- **Definition:** Find a maximum independent vertex set in a fixed graph from a published benchmark suite.
- **Solution / score:** Vertex set; objective cardinality. Scalar: independence number (maximize).
- **Configuration:** {"graph": "fixed named graph instance"}
- **Human baseline:** DIMACS challenge collection and exact graph algorithms provide incumbent and optimum records for selected instances.
- **Verification:** High for optimality certificate.
- **Risks:** Generic solver task, not a named mathematical construction family.
- **Primary sources:** [https://dimacs.rutgers.edu/archive/Challenges/](https://dimacs.rutgers.edu/archive/Challenges/)

### fractional-repetition-extremal — Extremal linear hypergraph with forbidden configuration

- **Recommendation:** conditional — Natural optimization with active research, though overlaps broad hypergraph Turán task.
- **Definition:** Maximize edges in a linear r-uniform hypergraph avoiding a fixed small configuration, e.g. a linear cycle.
- **Solution / score:** Hyperedge list; objective edge count. Scalar: number of hyperedges (maximize).
- **Configuration:** {"uniformity": "r", "vertices": "n", "forbidden_linear_configuration": "F"}
- **Human baseline:** Keevash's survey and published linear-cycle Turán results give exact large-n ranges and constructions for many r,F.
- **Verification:** Medium for F-free check.
- **Risks:** Broad family; choose a single standard F such as linear cycle and verify exact finite-n human records.
- **Primary sources:** [https://arxiv.org/abs/1302.2387](https://arxiv.org/abs/1302.2387); [https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf](https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf)

### max-partial-steiner — Maximum partial Steiner triple system

- **Recommendation:** reject — Parameter specialization of packing-design task.
- **Definition:** Choose as many triples on v points as possible with no pair repeated; equivalently packing number D(v,3,2).
- **Solution / score:** Triple list; objective number of triples. Scalar: number of triples (maximize).
- **Configuration:** {"points": "v"}
- **Human baseline:** Classical packing theory gives near-perfect packings and leave classifications; should be merged with the general packing-design family and source exact records per v.
- **Verification:** Low.
- **Risks:** Equivalent to packing design with t=2,k=3; do not count as separate benchmark.
- **Primary sources:** [https://ljcr.dmgordon.org/cover.html](https://ljcr.dmgordon.org/cover.html)

### maximal-arc — Largest cap/arc in finite projective plane

- **Recommendation:** conditional — Promising finite-geometry extremal objective but evidence/source curation incomplete.
- **Definition:** For a fixed finite projective plane, maximize a point set meeting each line in at most a prescribed number of points (arc/cap variants).
- **Solution / score:** Point set; cardinality objective. Scalar: number of points (maximize).
- **Configuration:** {"plane": "fixed plane/order", "line-intersection bound": "fixed"}
- **Human baseline:** Finite geometry literature and databases catalogue arcs/caps and complete classifications for small orders; no specific public primary database was verified in this pass.
- **Verification:** Low for witness; maximality high.
- **Risks:** Terminology and projective plane choice vary; needs specific named family and baseline records.
- **Primary sources:** [https://doi.org/10.1007/978-1-4614-1684-2](https://doi.org/10.1007/978-1-4614-1684-2)

### orthogonal-latin-square-existence — Orthogonal Latin square existence

- **Recommendation:** reject — Boolean existence task violates scalar-objective constraint.
- **Definition:** Find a pair of orthogonal Latin squares of fixed order n.
- **Solution / score:** Pair of squares; no free scalar. Scalar: none (not applicable).
- **Configuration:** {"order": "n"}
- **Human baseline:** Known constructions and nonexistence results are published; Euler's 36 officers problem is a named nonexistence example.
- **Verification:** Low for positive witness.
- **Risks:** Fixed-order feasibility has no scalar objective.
- **Primary sources:** [https://doi.org/10.1007/978-1-4614-1684-2](https://doi.org/10.1007/978-1-4614-1684-2)

### complete-mols-count — Complete MOLS count by order

- **Recommendation:** reject — Merge with maximum mutually orthogonal Latin squares.
- **Definition:** For each order n, report the maximum number N(n) of mutually orthogonal Latin squares.
- **Solution / score:** List of MOLS; objective count. Scalar: number of MOLS (maximize).
- **Configuration:** {"order": "n"}
- **Human baseline:** Same mathematical quantity as maximum MOLS, with standard constructions and Bruck–Ryser–Chowla restrictions.
- **Verification:** Low for witness, maximality hard.
- **Risks:** Duplicate naming of MOLS task.
- **Primary sources:** [https://doi.org/10.1090/S0002-9939-1950-0037974-5](https://doi.org/10.1090/S0002-9939-1950-0037974-5)

### anti-ramsey — Anti-Ramsey coloring number

- **Recommendation:** reject — Insufficiently canonical and weak baseline evidence for benchmark curation.
- **Definition:** For fixed graph H and host K_n, maximize distinct edge colors while requiring every H-copy to be rainbow-free (or the converse standard anti-Ramsey convention).
- **Solution / score:** Edge coloring; objective number of colors. Scalar: number of colors (maximize).
- **Configuration:** {"host_order": "n", "pattern": "H", "convention": "fixed anti-Ramsey definition"}
- **Human baseline:** Anti-Ramsey literature gives exact results for selected host/pattern families, but a unified record table and canonical convention were not verified.
- **Verification:** Medium for fixed finite coloring.
- **Risks:** Definition conventions vary; no verified broad human baseline.
- **Primary sources:** No primary source confirmed in this pass.
