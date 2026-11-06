# Discrete benchmark confirmation records

Date: 2026-11-03

Records: 44

## N001

### parameters

```json
{
  "q": 7,
  "power": 5
}
```

### scalar

```json
"independence number α(C_7^⊠5)"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 367,
  "author": "Sven Polak and Alexander Schrijver",
  "year": 2019,
  "description": "Their paper constructs an independent set of size 367 in the fifth strong power of C7."
}
```

### current_record

```json
{
  "value": "367–401",
  "scope": "Published interval for this finite power; a separate 2026 project explicitly reports no 368-set and no proof that one cannot exist."
}
```

### open_evidence

```json
"The 2019 paper gives a lower bound 367; current evidence does not establish the exact independence number."
```

### witness_url

```json
"https://arxiv.org/html/1808.07438"
```

### primary_sources

```json
[
  "https://arxiv.org/html/1808.07438",
  "https://www.sciencedirect.com/science/article/pii/S0020019018302291",
  "https://github.com/molind/c7-five"
]
```

### checks_performed

```json
[
  "Opened primary arXiv paper and verified size 367 and parameter; checked current project status distinguishing no known 368 construction from no optimality proof.",
  "Parent independently replayed all 67,161 unordered pairs from the retrieved appendix list; zero conflicts; witness saved at research/baseline_examples/shannon_C7_power5_367.json."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"No remaining witness check; optimality remains open."
```

## N010

### parameters

```json
{
  "chromatic_number": 4,
  "girth_at_least": 6
}
```

### scalar

```json
"minimum vertex count n_6(4)"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 66,
  "author": "Geoffrey Exoo and Jan Goedgebeur",
  "year": 2019,
  "description": "Their paper gives a 66-vertex 4-chromatic graph of girth 6."
}
```

### current_record

```json
{
  "value": "29–64",
  "scope": "Rampone 2026 reports lower bound 29 and an explicit 64-vertex upper-bound witness."
}
```

### open_evidence

```json
"The 2026 primary paper states 29 ≤ n_6(4) ≤ 64 and provides no equality claim."
```

### witness_url

```json
"https://doi.org/10.5281/zenodo.21861488"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/1901.04881",
  "https://arxiv.org/abs/2608.23652",
  "https://doi.org/10.5281/zenodo.21861488"
]
```

### checks_performed

```json
[
  "Opened 2026 arXiv paper; verified 64-vertex witness, lower bound 29, and linked archived code/data plus formal non-3-colorability certificate."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"For benchmark use, fetch the 64-vertex edge list and rerun girth and chromaticity certificate checks."
```

## N011

### parameters

```json
{
  "rows": 5,
  "columns": 10,
  "symbols": 3,
  "strength": 3
}
```

### scalar

```json
"minimum row count N for PHF(N;10,3,3)"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 5,
  "author": "Robert A. Walker II and Charles J. Colbourn",
  "year": 2007,
  "description": "Published construction PHF(5;10,3,3)."
}
```

### current_record

```json
{
  "value": 5,
  "scope": "This PHF(5;10,3,3) configuration is optimal by the four-row, at-most-nine-columns bound."
}
```

### open_evidence

```json
"A 5-row PHF(5;10,3,3) construction exists, while four rows can distinguish at most nine columns; therefore the row-count objective is optimal at 5 for this configuration."
```

### witness_url

```json
"https://doi.org/10.1515/JMC.2007.008"
```

### primary_sources

```json
[
  "https://doi.org/10.1515/JMC.2007.008",
  "https://www.phftables.com/"
]
```

### checks_performed

```json
[
  "Opened publisher metadata and abstract; confirmed authors, year, problem definition, explicit constructions, and best-known-size tables.",
  "Excluded because 5 is attained and the four-row at-most-9-columns bound proves no 4-row family can cover 10 columns."
]
```

### status

```json
"excluded_config"
```

### recomputed

```json
false
```

### remaining

```json
"Choose a larger parameter set with a published human construction whose minimum row count is not proved; inspect the table and replay one witness."
```

## N011

### parameters

```json
{
  "columns": 100,
  "symbols": 3,
  "strength": 3
}
```

### scalar

```json
"minimum row count N for PHF(N;100,3,3)"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "The 161700-row complete triple-indexed construction was derived during this audit; no public human source for this specific baseline was located. It must not be treated as a published human baseline."
}
```

### current_record

```json
{
  "value": "161700 rows by an audit-derived construction",
  "scope": "A direct feasible construction, not a sourced public human baseline or a record."
}
```

### open_evidence

```json
"The four-row bound gives at least five rows, but this wide interval does not establish that the finite 100-column instance is unsolved. Walker–Colbourn verifies the PHF subject and general construction context, but the audit did not find a public human source for the 161700-row triple-indexed construction or a source that settles the exact optimum at these parameters."
```

### witness_url

```json
"https://doi.org/10.1515/JMC.2007.008"
```

### primary_sources

```json
[
  "https://doi.org/10.1515/JMC.2007.008"
]
```

### checks_performed

```json
[
  "Opened Walker–Colbourn’s primary article record and verified its subject is perfect hash families, constructions, and existence.",
  "Derived the elementary construction locally: one row per 3-subset, assigning three distinct symbols to that subset; counted C(100,3)=161700 rows. This derivation is not a public-human citation.",
  "The four-row bound gives at least five rows for 100 columns, but does not settle whether a smaller construction exists."
]
```

### status

```json
"pending"
```

### recomputed

```json
true
```

### remaining

```json
"Find a publicly documented human construction for a sufficiently large PHF(·;100,3,3), and a primary source establishing that the selected finite configuration is not already optimal; otherwise replace this parameter set."
```

## N012

### parameters

```json
{
  "defectives": 4,
  "columns": 400
}
```

### scalar

```json
"minimum number of rows in a 4-disjunct binary matrix with 400 columns"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 121,
  "author": "William H. Kautz and Roy C. Singleton",
  "year": 1964,
  "description": "Take a Reed–Solomon [11,3,9] code over F_11 and apply the Kautz–Singleton one-hot encoding. It yields a 121-row binary 4-disjunct matrix with 1331 columns; retaining any 400 columns gives a 121×400 construction. Since 11>4(3−1)=8, four other codewords cannot cover all 11 positions where a target codeword differs."
}
```

### current_record

```json
{
  "value": "at most 121 rows",
  "scope": "Kautz–Singleton encoded Reed–Solomon construction, restricted to 400 columns; not an exact minimum."
}
```

### open_evidence

```json
"The construction gives a feasible 121-row matrix. The source presents code-based constructions rather than an optimality proof for 4-disjunct matrices with 400 columns; no exact minimum is claimed."
```

### witness_url

```json
"https://doi.org/10.1109/TIT.1964.1053689"
```

### primary_sources

```json
[
  "https://doi.org/10.1109/TIT.1964.1053689",
  "https://archive.computerhistory.org/resources/access/text/2019/11/102780478-05-08-acc.pdf"
]
```

### checks_performed

```json
[
  "Opened the Kautz–Singleton primary article record and its accessible archival scan; verified the q-ary code to binary one-hot construction and its connection to Reed–Solomon codes.",
  "Used the [11,3,9] Reed–Solomon parameters: 11 symbols per codeword, 1331 codewords; one-hot expansion has 11×11=121 rows.",
  "Checked 4-disjunctness: any other codeword agrees with a target in at most 2 positions, so four competitors can cover at most 8 of its 11 one-hot positions. Restricting to 400 columns preserves the property."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"Compare the 121-row construction with current lower bounds or improve it; the fixed 400-column optimum is not claimed."
```

## N013

### parameters

```json
{
  "stamps": 25,
  "max_stamps_per_sum": 2
}
```

### scalar

```json
"maximum consecutive range n_2(25) representable using at most two stamps"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 212,
  "author": "Historical published unrestricted two-stamp basis record for k=24; adding one denomination preserves range",
  "year": 2015,
  "description": "Kohonen states unrestricted n_2(k) is known through k=24; the A001212 sequence gives n_2(24)=212. Add a 25th denomination to obtain a valid 25-stamp baseline of at least 212."
}
```

### current_record

```json
{
  "value": "at least 212; n_2(25) not established in cited sources",
  "scope": "Extending the 24-denomination human witness to k=25 is feasible; the unrestricted k=25 optimum is not reported as known."
}
```

### open_evidence

```json
"Kohonen’s survey distinguishes unrestricted two-stamp values and reports them known only through k=24; this configuration has no exact value in that source."
```

### witness_url

```json
"https://arxiv.org/abs/1503.03416"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/1503.03416",
  "https://oeis.org/A001212"
]
```

### checks_performed

```json
[
  "Opened Kohonen’s primary arXiv record; verified its scope is restricted bases, which are distinct from this unrestricted task.",
  "Opened OEIS A001212; it defines unrestricted n2(k) as the largest consecutive range and lists n2(24)=212. Adding a distinct 25th denomination to a 24-denomination witness preserves all sums through 212, yielding a feasible 25-denomination baseline.",
  "The cited unrestricted literature states values are known through k=24; no exact k=25 value is claimed."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Obtain the k=24 denomination list and add a distinct denomination if a concrete witness file is needed; check for post-2015 improvements to unrestricted k=25."
```

## T035

### parameters

```json
{
  "degree": 4,
  "girth": 10
}
```

### scalar

```json
"minimum number of vertices n(4,10)"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 320,
  "author": "Geoffrey Exoo, Jan Goedgebeur, Jorik Jooken, Louis Stubbe, Tibo Van den Eede",
  "year": 2026,
  "description": "Published preprint v2 reports a 4-regular girth-10 graph on 320 vertices."
}
```

### current_record

```json
{
  "value": 320,
  "scope": "best known upper bound reported by cited paper; paper gives lower bound 243, so optimality is unresolved"
}
```

### open_evidence

```json
"The primary paper reports 243 ≤ n(4,10) ≤ 320; it does not claim equality."
```

### witness_url

```json
"https://arxiv.org/abs/2511.07247"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/2511.07247"
]
```

### checks_performed

```json
[
  "Opened arXiv abstract and verified authors, v2 date, parameter, 320 upper bound, 243 lower bound."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve the graph file and independently verify regularity and girth before using it as a replayed benchmark."
```

## T036

### parameters

```json
{
  "maximum_degree": 4,
  "diameter": 3
}
```

### scalar

```json
"largest order of a simple graph with maximum degree at most 3 and diameter at most 4"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 41,
  "author": "Degree-Diameter Table for Graphs (UPC; attribution needs retrieval)",
  "year": null,
  "description": "The maintained table reports a 41-vertex graph for maximum degree 4 and diameter 3."
}
```

### current_record

```json
{
  "value": "41 vertices",
  "scope": "Published construction; maximum order is not proved for this parameter."
}
```

### open_evidence

```json
"The degree-diameter table separates known constructions from proved optima; no exact-optimality result for (4,3) was located in this audit."
```

### witness_url

```json
"https://web.mat.upc.edu/francesc.comellas/delta-d/taula_delta_d.html"
```

### primary_sources

```json
[
  "https://web.mat.upc.edu/francesc.comellas/delta-d/taula_delta_d.html",
  "https://udspace.udel.edu/server/api/core/bitstreams/45f012e8-720c-47be-9507-63aacc42aa87/content"
]
```

### checks_performed

```json
[
  "Opened the UPC degree–diameter table; verified its caption says entries are largest known graphs and boldface alone denotes optimal entries. The (maximum degree 4, diameter 3) cell reports 41 and is not marked bold.",
  "The Moore bound is 53, so 41 is a feasible published baseline and the optimum is not certified by the table."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve the underlying 41-vertex graph citation/list and independently validate it if desired; the table already supports this as a known non-optimality-certified benchmark."
```

## T037

### parameters

```json
{
  "left_part": 100,
  "right_part": 100,
  "forbidden_biclique": "K2,2"
}
```

### scalar

```json
"maximum number of edges in a K2,2-free bipartite graph with parts 100 and 100"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 910,
  "author": "James Singer",
  "year": 1938,
  "description": "The incidence graph of PG(2,9) has 91 points and 91 lines, 10 incidences per line, hence 910 edges; it is K2,2-free. Add nine isolates to each side to obtain a 100×100 construction."
}
```

### current_record

```json
{
  "value": "at least 910 edges",
  "scope": "Singer projective-plane incidence construction padded to fixed dimensions; feasible lower bound, not claimed as record."
}
```

### open_evidence

```json
"The finite-plane construction supplies a feasible baseline. General exact Z(2,2;m,n) values are not known for arbitrary dimensions; no source located in this pass proves the 100×100 value optimal. The configuration should be treated as open pending exact-table confirmation."
```

### witness_url

```json
"https://doi.org/10.1090/S0002-9947-1938-1501951-4"
```

### primary_sources

```json
[
  "https://doi.org/10.1090/S0002-9947-1938-1501951-4",
  "https://arxiv.org/abs/2203.02283"
]
```

### checks_performed

```json
[
  "Opened Singer’s 1938 primary paper record, which establishes the cyclic projective-plane incidence construction for prime-power order. For order 9, each of 91 lines has 10 points, giving 910 incidences.",
  "Recomputed the baseline edge count 91×10=910; a projective plane has each point pair on exactly one line, so the incidence graph contains no K2,2. Padding by nine isolated vertices per side gives the stated 100×100 instance.",
  "Reviewed the primary-source survey record for the Zarankiewicz family; it describes exact values only for specific slices and does not certify the 100×100 value."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"A full adjacency list can be generated from the standard finite-field model if the benchmark requires replay; the configuration-specific maximum remains unproved in the inspected sources."
```

## T038

### parameters

```json
{
  "n": 40,
  "forbidden_graphs": [
    "C4"
  ]
}
```

### scalar

```json
"ex(40,C4), maximum edges in a 40-vertex C4-free graph"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 127,
  "author": "Narjess Afzaly and Brendan McKay extremal-graph catalogue",
  "year": 2026,
  "description": "The maintained catalogue gives 127 edges and an explicit sparse6 graph record."
}
```

### current_record

```json
{
  "value": "at least 127",
  "scope": "The table marks values with ≥ when it reports a construction but has not proved no better graph exists."
}
```

### open_evidence

```json
"The page legend states that rows with ≥ on both edge and graph counts are lower-bound constructions only; n=40 is in that category."
```

### witness_url

```json
"https://users.cecs.anu.edu.au/~bdm/data/extremal.html"
```

### primary_sources

```json
[
  "https://users.cecs.anu.edu.au/~bdm/data/extremal.html"
]
```

### checks_performed

```json
[
  "Opened catalogue; verified definition, legend for construction-only rows, and C4-free n=40 lower-bound row with 127 edges."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Download sparse6 witness and independently check C4-freeness and edge count."
```

## T039

### parameters

```json
{
  "vertices": 20,
  "forbidden_graph": "C6"
}
```

### scalar

```json
"minimum number of edges in a C6-saturated graph on 20 vertices"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 27,
  "author": "Y. Chen, J. H. Kim, and collaborators (2021)",
  "year": 2021,
  "description": "The published construction theorem gives sat(n,C6)≤(4n+1)/3 for n≥9; at n=20 this yields an integer upper bound of 27 edges."
}
```

### current_record

```json
{
  "value": "25–27 edges",
  "scope": "Published bounds 4n/3−2 ≤ sat(n,C6) ≤ (4n+1)/3 imply this interval at n=20."
}
```

### open_evidence

```json
"The primary 2021 paper states nonmatching lower and upper bounds for all n≥9; at n=20, the lower bound is 24⅔, hence at least 25, while the upper bound is at most 27. The interval does not prove optimality."
```

### witness_url

```json
"https://arxiv.org/abs/2108.03910"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/2108.03910",
  "https://doi.org/10.37236/1055"
]
```

### checks_performed

```json
[
  "Opened the primary Lan–Shi–Wang–Zhang paper and verified its abstract states 4n/3−2 ≤ sat(n,C6) ≤ (4n+1)/3 for all n≥9, with the upper bound proved by construction.",
  "At n=20, integer bounds give 25≤sat(20,C6)≤27. The construction theorem is a public human baseline; no matching exact value is claimed."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"If desired, expand the paper’s parameterized construction into an explicit 20-vertex graph and replay saturation; the published theorem already gives the verified 27-edge feasible upper bound and nonmatching lower bound."
```

## T040

### parameters

```json
{
  "clique": 5,
  "independent_set": 5
}
```

### scalar

```json
"maximum order of a graph with no K5 and no independent 5-set"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 42,
  "author": "Geoffrey Exoo et al.",
  "year": 1997,
  "description": "A (5,5)-good graph on 42 vertices; this implies R(5,5)≥43."
}
```

### current_record

```json
{
  "value": "42 vertices; 43 ≤ R(5,5) ≤ 46",
  "scope": "The scored construction is graph order, so the construction baseline is 42; Ramsey lower bound is one larger."
}
```

### open_evidence

```json
"The cited current bounds differ; no exact value is claimed."
```

### witness_url

```json
"https://users.cecs.anu.edu.au/~bdm/data/ramsey.html"
```

### primary_sources

```json
[
  "https://users.cecs.anu.edu.au/~bdm/data/ramsey.html",
  "https://arxiv.org/abs/2409.15709"
]
```

### checks_performed

```json
[
  "Opened Angeltveit–McKay paper and verified R(5,5)≤46; cross-checked survey source for Exoo lower bound 43 and witness database."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve one 42-vertex adjacency list from the cited source and replay clique and independent-set checks."
```

## T041

### parameters

```json
{
  "uniformity": 3,
  "n": 100,
  "forbidden_hypergraph": "K4^3"
}
```

### scalar

```json
"maximum number of triples in a 3-uniform 100-vertex hypergraph containing no K4^3"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 90915,
  "author": "Paul Turán (1941) construction",
  "year": 1941,
  "description": "Partition into A,B,C of sizes 34,33,33. Include all triples meeting all three parts, plus triples with two vertices in A and one in B, two in B and one in C, and two in C and one in A. Count: 34·33·33 + C(34,2)·33 + C(33,2)·33 + C(33,2)·34 = 90,915."
}
```

### current_record

```json
{
  "value": "at least 90,915",
  "scope": "Classical K4^3-free construction at n=100; no exact finite optimum claimed."
}
```

### open_evidence

```json
"The exact Turán number t3(100,4) is not known; Turán’s formula is a conjecture for the extremal value. The cited Erdős problems page states the conjecture, so this finite value is an open benchmark instance."
```

### witness_url

```json
"https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html"
```

### primary_sources

```json
[
  "https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/ExactHypergraphTuranT3n4.html",
  "https://people.maths.ox.ac.uk/keevash/papers/turan-survey.pdf"
]
```

### checks_performed

```json
[
  "Opened the Erdős Problems primary-topic page; it identifies Turán’s 1941 conjecture for t3(n,4), whose exact extremal formula remains open.",
  "Checked the standard construction definition: all transversal triples and cyclic two-in-one-part/one-in-next-part triples. A K4^3 cannot occur: if four vertices occupy all three parts, the two-part class pattern misses at least one of the four triples; if only two parts are occupied, the cyclic rule includes triples in at most one direction, also leaving a triple absent.",
  "Recomputed the four edge counts as 37,026 + 18,513 + 17,424 + 17,952 = 90,915."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"A standalone generator can emit the 90,915 triples for replay; the known exact-extremum question remains open."
```

## T042

### parameters

```json
{
  "vertices": 100,
  "forbidden_clique": 3,
  "target_independence_number": 40
}
```

### scalar

```json
"minimum independence number α(G) among triangle-free graphs G on 100 vertices"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 40,
  "author": "Standard balanced blow-up of C5 (Ramsey construction)",
  "year": null,
  "description": "Replace each vertex of C5 by an independent class of 20 vertices, and join consecutive classes completely. The graph is triangle-free. An independent set can meet at most two nonadjacent classes, so α=40."
}
```

### current_record

```json
{
  "value": "at most 40",
  "scope": "Human C5 blow-up construction; the graph and α certificate are described structurally."
}
```

### open_evidence

```json
"The off-diagonal Ramsey problem R(3,k) is unresolved in this range; the blow-up supplies a feasible value 40, not an exact minimum over all 100-vertex triangle-free graphs."
```

### witness_url

```json
"https://www.cambridge.org/core/services/aop-cambridge-core/content/view/1EF0092CCBAA03082E59A756E5ECEF01/9781009344333c1_1-43.pdf/basic-graph-theory.pdf"
```

### primary_sources

```json
[
  "https://repository.rit.edu/article/640/",
  "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/1EF0092CCBAA03082E59A756E5ECEF01/9781009344333c1_1-43.pdf/basic-graph-theory.pdf"
]
```

### checks_performed

```json
[
  "Inspected a published graph-theory text section on triangle-free graphs; it states that the t-blow-up C5(t) is triangle-free and has 5t vertices.",
  "For t=20, the blow-up has 100 vertices. Any independent set uses at most two nonconsecutive classes, and taking two such classes gives 40; hence α=40 exactly.",
  "The finite Ramsey source confirms this objective is the Erdős–Rogers/R(3,k) family; no exact optimum at n=100 is claimed."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"If needed, write the five-class adjacency rule as an explicit graph certificate; investigate stronger published Ramsey graphs for n=100."
```

## T043

### parameters

```json
{
  "vertices": 100,
  "edges": 3000
}
```

### scalar

```json
"minimum triangle count among simple graphs with 100 vertices and 3000 edges"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 25000,
  "author": "Explicit bipartite perturbation of the balanced complete bipartite graph",
  "year": null,
  "description": "Take K50,50, then add all 500 edges of K20,25 inside one side. This gives 3000 edges. Each added edge has exactly the 50 vertices on the other side as common neighbors, so the graph has 25,000 triangles."
}
```

### current_record

```json
{
  "value": "at most 25000 triangles",
  "scope": "Explicit finite construction; no exact minimum is claimed."
}
```

### open_evidence

```json
"The inspected exact-results paper by Liu, Pikhurko, and Staden gives exact solutions for all sufficiently large graphs in a specified density range, but its abstract does not give a threshold that certifies n=100. No inspected primary source settles this particular finite pair (100,3000)."
```

### witness_url

```json
"https://arxiv.org/abs/1712.00633"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/1712.00633",
  "https://people.cs.uchicago.edu/~razborov/files/triangles.pdf"
]
```

### checks_performed

```json
[
  "Opened the primary Liu–Pikhurko–Staden paper record; checked that its stated result concerns sufficiently large graphs and cannot be applied to n=100 without a threshold.",
  "Recomputed the construction: K50,50 has 2500 edges and no triangles; adding K20,25 contributes 500 edges and 500×50=25000 triangles."
]
```

### status

```json
"pending"
```

### recomputed

```json
true
```

### remaining

```json
"Find a primary source or exact finite computation that establishes the status of the exact minimum for (n,m)=(100,3000); retain the explicit 25000-triangle construction as the human baseline."
```

## T044

### parameters

```json
{
  "marks": 29
}
```

### scalar

```json
"minimum ruler length"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 623,
  "author": "M. D. Atkinson and A. Hassenklover",
  "year": 1984,
  "description": "The shortest-known 29-mark ruler is reported with length 623, using a projective-plane construction with parameter 29."
}
```

### current_record

```json
{
  "value": "at most 623",
  "scope": "Published construction upper bound; optimal lengths are proved only through 28 marks."
}
```

### open_evidence

```json
"The 29-mark optimum is not known; length 623 is a construction bound, not a theorem of optimality."
```

### witness_url

```json
"https://cube20.org/golomb/"
```

### primary_sources

```json
[
  "https://cube20.org/golomb/",
  "https://web.archive.org/web/20060110160821/http://www.research.ibm.com/people/s/shearer/grtab.html",
  "https://doi.org/10.1090/S0002-9947-1938-1501951-4"
]
```

### checks_performed

```json
[
  "Inspected the maintained Golomb construction table/source search entry: it lists 29 marks, length 623, Atkinson–Hassenklover 1984, and projective-plane finite-field construction parameter 29.",
  "Cross-checked the current proof frontier: optimality is proved through 28 marks, so the 29-mark configuration remains open; the 623 ruler is a feasible human baseline, not a proven optimum."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve or regenerate the published finite-field mark list and replay its pairwise differences for an independent certificate; this is optional for admitting the public baseline."
```

## T045

### parameters

```json
{
  "h": 3,
  "cardinality": 9,
  "ambient_interval": [
    1,
    729
  ]
}
```

### scalar

```json
"minimum diameter (maximum minus minimum element) of a B_3 set"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": "diameter at most 728",
  "author": "Raj Chandra Bose and Sarvadaman Chowla",
  "year": 1962,
  "description": "The Bose–Chowla theorem gives a 9-element B3 construction in an interval of diameter at most 728 for the q=9 prime-power parameter; this is a feasible upper bound, not an exact minimum."
}
```

### current_record

```json
{
  "value": "at most 728",
  "scope": "Nine-element B3 set in [1,729] by Bose–Chowla; the order of the elements gives nine distinct marks."
}
```

### open_evidence

```json
"Bose–Chowla gives a feasible upper bound for the fixed 9-element B3 instance. The cited theorem does not prove optimality, and no exact finite minimum was established in this source check."
```

### witness_url

```json
"https://doi.org/10.1007/BF02566968"
```

### primary_sources

```json
[
  "https://doi.org/10.1007/BF02566968",
  "https://doi.org/10.1007/s00493-023-00061-4"
]
```

### checks_performed

```json
[
  "Opened the primary Bose–Chowla paper record and later exposition of Theorem 12; the theorem gives a B_h subset of [q^h] of size q when q is one more than a prime power.",
  "For q=9 and h=3, this gives 9 marks in [729], hence diameter at most 728. This is an upper bound, not an exact score."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Verify the exact minimum diameter for 9-element B3 sets from a primary finite-results source; keep the construction bound separate from the optimum."
```

## T046

### parameters

```json
{
  "rows": 7,
  "marks_per_row": 6
}
```

### scalar

```json
"minimum scope m"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": "at most 112",
  "author": "Published difference-triangle-set construction (attribution/table row pending)",
  "year": null,
  "description": "The candidate inventory points to a (7,5) DTS with scope at most 112; each of 7 rows has 6 marks and all 105 positive within-row differences are distinct."
}
```

### current_record

```json
{
  "value": "at most 112",
  "scope": "Construction bound; minimum scope for this parameter is open per recent literature."
}
```

### open_evidence

```json
"The recent primary paper states that minimum scopes are open for general parameters. The exact source attribution and construction table cell for scope 112 at (7,5) were not verified in primary full text, so this record remains pending."
```

### witness_url

```json
"https://arxiv.org/abs/0712.2553"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/0712.2553",
  "https://doi.org/10.1002/jcd.22009"
]
```

### checks_performed

```json
[
  "Opened Chee–Colbourn’s primary construction-paper record and the recent primary journal abstract; verified the DTS setting and that general minimum-scope questions remain open.",
  "A secondary source reports a (7,5) construction with scope at most 112, but the corresponding primary table row and actual marks were not checked; no exact witness claim is made."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Verify a primary source that explicitly gives the (7,5) scope-112 construction and confirms the fixed instance is not settled; then record the seven rows or keep pending."
```

## T047

### parameters

```json
{
  "field": 3,
  "dimension": 8
}
```

### scalar

```json
"maximum size of a cap set in F_3^8"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 496,
  "author": "Edel construction (as cited by Romera-Paredes et al.)",
  "year": 2004,
  "description": "The Nature paper records 496 as the previous best known cap in F_3^8; FunSearch later raised the construction to 512."
}
```

### current_record

```json
{
  "value": "at least 512",
  "scope": "FunSearch 2023 published construction; 512 is a lower bound, not a proved maximum."
}
```

### open_evidence

```json
"The 512-point published construction does not prove the maximum size of a cap in F_3^8."
```

### witness_url

```json
"https://www.nature.com/articles/s41586-023-06924-6"
```

### primary_sources

```json
[
  "https://www.nature.com/articles/s41586-023-06924-6",
  "https://github.com/google-deepmind/funsearch"
]
```

### checks_performed

```json
[
  "Retained the reconstructible 256-point binary cube as a simple witness. Located the FunSearch paper and repository for the stronger 512-point construction; witness not yet replayed.",
  "Nature paper’s figure and text identify 496 as the previous best-known F_3^8 construction and give the explicit 512-cap as a later lower bound."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve the published 512-point set and check its cap property; confirm no later construction or proof changed the frontier."
```

## T048

### parameters

```json
{
  "interval": [
    1,
    729
  ]
}
```

### scalar

```json
"maximum cardinality of a subset with no nontrivial 3-term arithmetic progression"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 64,
  "author": "Salem–Spencer construction",
  "year": 1942,
  "description": "The 64 integers 1 plus each base-3 number of length 6 whose digits are 0 or 1 form a 3-AP-free subset of [1,729]."
}
```

### current_record

```json
{
  "value": "at least 64",
  "scope": "Explicit human construction; no exact maximum claim."
}
```

### open_evidence

```json
"Roth’s theorem implies the maximum is sublinear asymptotically, but does not give this finite maximum; no exact result for N=729 was located."
```

### witness_url

```json
"https://arxiv.org/abs/2406.12290"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/2406.12290"
]
```

### checks_performed

```json
[
  "Opened the 1942 Salem–Spencer primary PNAS article and confirmed its definition of progression-free sets.",
  "Checked the finite ternary construction: 64 base-3 words of length six with digits 0/1 map to [0,728]; no carries occur in x+z=2y, and coordinate equality forces a trivial progression. Translate by 1 to lie in [1,729]."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Check a current primary exact-value table for r3(729) if an explicit configuration-level open-status citation is needed; no exact optimum is claimed."
```

## T049

### parameters

```json
{
  "covered_interval": [
    1,
    214
  ],
  "mark_interval": [
    0,
    225
  ]
}
```

### scalar

```json
"minimum cardinality of a difference basis"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 30,
  "author": "Rédei–Rényi difference-basis problem; explicit elementary interval/multiples construction",
  "year": 1949,
  "description": "For m=15, A={0,1,...,15}∪{15,30,...,225} has 30 marks and every integer 1≤n≤225 is a difference of two marks, hence covers [1,214]."
}
```

### current_record

```json
{
  "value": "at most 30",
  "scope": "Explicit construction; this is not asserted to be minimum."
}
```

### open_evidence

```json
"Exact difference-basis minima have been tabulated only through limited finite ranges; exact status at coverage 214 has not been verified here."
```

### witness_url

```json
"https://www.mathnet.ru/eng/sm5985"
```

### primary_sources

```json
[
  "https://www.mathnet.ru/eng/sm5985",
  "https://www.math.cmu.edu/~mtait/DifferenceBases.pdf"
]
```

### checks_performed

```json
[
  "Opened the primary Rédei–Rényi 1949 record; verified the paper is exactly about representing 1,…,N by differences and establishes the classical interval difference-basis problem.",
  "Independently checked the stated 30-mark construction algebraically: A={0,…,15}∪{15,30,…,225}; multiples cover multiples of 15 and (q+1)·15−(15−r) covers 15q+r for 1≤r≤14.",
  "The A005434 URL previously attached was unrelated (binary-word autocorrelations) and has been removed."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"The chosen 30-mark witness is feasible; no exact optimum is claimed. Retrieve an explicit historical attribution for this exact elementary set if needed."
```

## T051

### parameters

```json
{
  "colors": 6
}
```

### scalar

```json
"maximum N for a k-coloring of [N] with no monochromatic x+y=z (Schur number lower-bound task)"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 536,
  "author": "H. Fredricksen and M. M. Sweet",
  "year": 2000,
  "description": "Published six-color partition of [536] into sum-free sets."
}
```

### current_record

```json
{
  "value": 537,
  "scope": "Chen, Zhu, and Long 2026 give a six-color partition of [537]; this is a current lower bound, not an exact Schur number."
}
```

### open_evidence

```json
"The paper gives a 537-element coloring but no upper bound proving S(6)=537."
```

### witness_url

```json
"https://arxiv.org/abs/2610.31362"
```

### primary_sources

```json
[
  "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r13",
  "https://arxiv.org/abs/2610.31362"
]
```

### checks_performed

```json
[
  "Opened 2026 arXiv source; verified it explicitly improves Fredricksen–Sweet (2000) from 536 to 537 and provides supplementary partition files."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve historical and 2026 colorings; replay the sum-free property and record human/AI provenance separately."
```

## T052

### parameters

```json
{
  "colors": 2,
  "progression_length": 7
}
```

### scalar

```json
"maximum N for a 2-coloring of [N] with no monochromatic 7-term arithmetic progression"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 3703,
  "author": "Rabung and Lotts",
  "year": 2012,
  "description": "Cyclic zipper/power-residue construction gives W(2,7)>3703."
}
```

### current_record

```json
{
  "value": "W(2,7)>3703",
  "scope": "Published lower bound from the 2012 construction; exact value unknown."
}
```

### open_evidence

```json
"Current source table says W(2,7) is open and lists the 3703 record; no exact value is known."
```

### witness_url

```json
"https://doi.org/10.37236/3248"
```

### primary_sources

```json
[
  "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v19i2p35",
  "https://arxiv.org/abs/2608.20824"
]
```

### checks_performed

```json
[
  "Opened the 2005 paper table to verify exact W(2,6) is solved and later checked a current lower-bound table reporting W(2,7)>3703; checked 2026 paper for general lower-bound theorem, which does not settle W(2,7)."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve the 3703 coloring/certificate from the 2012 paper or archive; current exact value remains unknown."
```

## T053

### parameters

```json
{
  "discrepancy_cap": 3
}
```

### scalar

```json
"maximum sequence length N with discrepancy at most 3"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 127645,
  "author": "Boris Konev and Alexei Lisitsa (SAT-generated finite construction, published and human-verifiable)",
  "year": 2015,
  "description": "Their published work provides a finite discrepancy-3 sign sequence of length 127,645. Their exact optimality theorem applies only to multiplicative/completely multiplicative sequences; this general homogeneous-progression instance is a feasible lower-bound baseline, not an optimum."
}
```

### current_record

```json
{
  "value": "at least 127645 terms",
  "scope": "Published finite discrepancy-3 sequence; exact general maximum remains open."
}
```

### open_evidence

```json
"The primary Konev–Lisitsa source distinguishes unrestricted discrepancy sequences from multiplicative sequences and reports unrestricted sequences longer than 130,000 in a later construction. The exact 127,645 bound is proved only for completely multiplicative sequences, so it does not solve the unrestricted finite task."
```

### witness_url

```json
"https://arxiv.org/abs/1407.2510"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/1407.2510",
  "https://doi.org/10.4230/LIPIcs.CP.2014.32"
]
```

### checks_performed

```json
[
  "Opened the primary Konev–Lisitsa arXiv paper and verified the 127,645 exact maximum is stated for multiplicative/completely multiplicative sequences only.",
  "Opened a later primary discrepancy paper/report; it states ordinary discrepancy-3 sequences can exceed 130,000, confirming that 127,645 is merely a historical feasible baseline for the unrestricted family."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Replace 127,645 with the strongest published ordinary-sequence witness if a stronger human baseline is useful; verify no exact maximum is known for the selected homogeneous-progression configuration."
```

## T054

### parameters

```json
{
  "interval_length": 1000
}
```

### scalar

```json
"maximum cardinality of A⊆{1,…,1000} with no positive square difference"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 105,
  "author": "Imre Z. Ruzsa",
  "year": 1984,
  "description": "Ruzsa’s explicit modular construction uses R={0,15,21,27,42,48,59} modulo 65 (equivalently residues (0,0),(0,2),(1,8),(2,1),(2,3),(3,9),(4,7) modulo 5 and 13). For N=1000 take {1+r+65s : r∈R, 0≤s≤14}; it has 105 positive elements, lies in [1,1000], and has no positive square difference."
}
```

### current_record

```json
{
  "value": "at least 105 elements",
  "scope": "Explicit finite construction instantiated from Ruzsa’s theorem; it does not claim the exact maximum."
}
```

### open_evidence

```json
"Ruzsa’s primary paper provides the modular-residue construction and an asymptotic lower construction. The Green–Sawhney result is an asymptotic upper bound, not an exact maximum for N=1000. The finite optimum at N=1000 was not found in the inspected sources."
```

### witness_url

```json
"https://doi.org/10.1007/BF02454169"
```

### primary_sources

```json
[
  "https://doi.org/10.1007/BF02454169",
  "https://arxiv.org/abs/2411.17448"
]
```

### checks_performed

```json
[
  "Opened the full-text transcript of Ruzsa’s 1984 primary paper and checked the square-difference-free definition, construction proof, and listed residue pairs modulo 5 and 13.",
  "Combined the CRT residues to obtain R={0,15,21,27,42,48,59}; instantiated 15 choices of the unrestricted base-65 digit, giving 7×15=105 elements from 1 through 970. The source proof establishes that positive differences are not squares.",
  "Opened Green–Sawhney’s primary preprint record; it gives an asymptotic upper bound, not the exact finite maximum at 1000.",
  "Enumerated all 5,460 unordered pairs in the instantiated 105-element set; every positive difference was non-square (0 square-difference violations)."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"If desired, independently enumerate the 105-element set and compare with any finite upper bounds; the primary construction and cardinality suffice for this baseline."
```

## T055

### parameters

```json
{
  "cardinality": 100,
  "ambient_set": "integers [1,1000]"
}
```

### scalar

```json
"minimum max(|A+A|,|A·A|) among 100-element subsets A⊆[1,1000]"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 2906,
  "author": "Arithmetic progression A={1,2,…,100}; classical finite sum-product example",
  "year": 2003,
  "description": "For A={1,…,100}, |A+A|=199 and |A·A|=2,906, so max(|A+A|,|A·A|)=2,906."
}
```

### current_record

```json
{
  "value": "at most 2,906",
  "scope": "Explicit human arithmetic-progression construction; product-set size is the scalar."
}
```

### open_evidence

```json
"Chang’s primary paper formulates and studies sum-product growth for integer sets, but does not give an exact minimum for 100-element subsets of [1,1000]. The fixed finite optimum is not claimed solved."
```

### witness_url

```json
"https://annals.math.princeton.edu/2003/157-3/p07"
```

### primary_sources

```json
[
  "https://annals.math.princeton.edu/2003/157-3/p07",
  "https://doi.org/10.4007/annals.2003.157.939"
]
```

### checks_performed

```json
[
  "Opened Chang’s primary Annals paper and verified the finite-set sum/product definitions and its focus on lower bounds rather than bounded-interval exact optima.",
  "Enumerated pair sums and products of A={1,…,100}; |A+A|=199 and |A·A|=2,906."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"A finite exact-minimum table check may be added later; this record is a human upper-bound baseline, not an optimum claim."
```

## T056

### parameters

```json
{
  "field_order": 5,
  "dimension": 3
}
```

### scalar

```json
"minimum number of points in a Kakeya set in F_5^3"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": "at most 67",
  "author": "Swastik Kopparty, Vsevolod F. Lev, Shubhangi Saraf, and Madhu Sudan",
  "year": 2010,
  "description": "Theorem 6 of their paper states that for odd q there exists a rank-1 Kakeya set with |K|<2(1+1/(q−1))((q+1)/2)^n. At q=5,n=3 the bound is |K|<67.5, so integrality gives a feasible construction of at most 67 points. This is an upper bound, not an exact score or a claim of optimality."
}
```

### current_record

```json
{
  "value": "at most 67 points",
  "scope": "Theorem 6 construction upper bound; no exact minimum is claimed."
}
```

### open_evidence

```json
"The cited construction theorem gives a feasible set of at most 67 points for this finite field and dimension. It does not assert optimality. The exact minimum for (q,n)=(5,3) was not established in the inspected source check."
```

### witness_url

```json
"https://arxiv.org/abs/1003.3736"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/1003.3736",
  "https://epubs.siam.org/doi/10.1137/100783704"
]
```

### checks_performed

```json
[
  "Opened the primary Kopparty–Lev–Saraf–Sudan paper; verified authors and 2010 preprint date, and inspected Theorem 6 and its explicit construction (Theorems 7–8 give the construction details).",
  "Substituted q=5,n=3 into Theorem 6: 2×(1+1/4)×3^3=67.5; because cardinality is integer, the theorem guarantees at most 67 points. This bound is not an exact optimum.",
  "Checked the cited Dvir–Kopparty–Saraf–Sudan paper separately; it gives a lower-bound result and is not the source of the construction upper bound used here."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"If needed, reconstruct an explicit set from the construction in Theorems 7–8 and compare it with finite lower bounds; the cited theorem only supplies an upper bound."
```

## T057

### parameters

```json
{
  "max_cardinality": 512,
  "integer_interval": [
    -1000000,
    1000000
  ]
}
```

### scalar

```json
"log(|A+A|/|A|) / log(|A-A|/|A|)"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 1.0597930945472454,
  "author": "Pigarev–Freiman construction, reproduced by Martin–O’Bryant",
  "year": 2006,
  "description": "17-element set {0,1,2,4,5,9,12,13,14,16,17,21,24,25,26,28,29}; exact counts |A+A|=59 and |A-A|=55."
}
```

### current_record

```json
{
  "value": 1.0597930945472454,
  "scope": "This is the historical finite witness score; later papers report stronger values and theorem-level bounds."
}
```

### open_evidence

```json
"The configuration is a finite capped search, not a claim that the witness is globally optimal; current scope score needs a date-frozen finite record."
```

### witness_url

```json
"https://personal.math.ubc.ca/~gerg/papers/downloads/MSHMSTD.pdf"
```

### primary_sources

```json
[
  "https://arxiv.org/abs/math/0608131",
  "https://arxiv.org/abs/2607.27199"
]
```

### checks_performed

```json
[
  "Reused the existing recomputation in research/baseline_examples/recomputed_examples.json: 17 marks, sumset 59, difference set 55, score 1.0597930945472454.",
  "Checked sumdiff_audit.md distinction between finite score and later global exponent claim."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"Add a dated finite-record snapshot for the chosen caps; do not label the historical witness as current best."
```

## T058

### parameters

```json
{
  "cardinality_cap": 100,
  "integer_interval": [
    0,
    1000000
  ]
}
```

### scalar

```json
"maximum log(|A−A|)/log(|A+A|) over finite A⊆[0,1000000], 2≤|A|≤100"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 1.0872911358762911,
  "author": "François Hennecart, Gilles Robert, Alexander Yudin (simplex construction)",
  "year": 1999,
  "description": "Take the integer simplex Δ²₂={(x,y)∈Z²:x,y≥0,x+y≤2} and Freiman-embed by φ(x,y)=x+5y. This gives A={0,1,2,5,6,10}, with |A+A|=15, |A−A|=19 and score log(19)/log(15)=1.0872911358762911."
}
```

### current_record

```json
{
  "value": "at least 1.0872911358762911",
  "scope": "Finite human simplex witness in the configured interval; no optimum claim."
}
```

### open_evidence

```json
"The Hennecart–Robert–Yudin paper gives the simplex construction family and asymptotic exponent. This six-point finite member is an explicit Freiman embedding; the maximum over the fixed search budget is not established by the source or this audit."
```

### witness_url

```json
"https://www.numdam.org/item/AST_1999__258__173_0.pdf"
```

### primary_sources

```json
[
  "https://www.numdam.org/item/AST_1999__258__173_0.pdf",
  "https://www.numdam.org/item/AST_1999__258__173_0/",
  "https://arxiv.org/abs/2511.02864"
]
```

### checks_performed

```json
[
  "Opened the 1999 primary HRY paper PDF; it defines lattice simplex A(m,L)={x∈Z^m:x_i≥0,Σx_i≤L}, gives the number of sums and differences, and describes projection to integer sets preserving those cardinalities.",
  "Specialized to m=2,L=2, obtaining six vectors; the base-5 map φ(x,y)=x+5y is injective on both sum and difference vectors because coordinate ranges are at most 4 and 2, respectively.",
  "Mapped set is {0,1,2,5,6,10}; exact pair enumeration gives |A+A|=15 and |A−A|=19; score=log(19)/log(15)=1.0872911358762911."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"No coordinate exceeds 10 and |A|=6, so the witness fits the stated caps. The best score under the full finite budget remains unknown."
```

## T059

### parameters

```json
{
  "cardinality_cap": 128,
  "integer_interval": [
    0,
    1000000
  ]
}
```

### scalar

```json
"1 + log(|U-U|/|U+U|) / log(2 max(U)+1)"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 1.107802056693651,
  "author": "Gyarmati, Hennecart, and Ruzsa",
  "year": 2007,
  "description": "U={0,1,3,6,13,17,21}; |U+U|=26, |U-U|=39, q=43."
}
```

### current_record

```json
{
  "value": 1.107802056693651,
  "scope": "Published finite certificate; computational search claimed optimal among eligible |U|≤11 in its stated search domain."
}
```

### open_evidence

```json
"The published seven-element witness is a valid baseline, but this configuration permits up to 128 elements and max U up to 1,000,000. The paper’s small-cardinality search does not settle this enlarged finite budget; later global-constant claims are kept separate from the finite maximum."
```

### witness_url

```json
"https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf"
```

### primary_sources

```json
[
  "https://doi.org/10.7169/facm/1229618749",
  "https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf"
]
```

### checks_performed

```json
[
  "Reused the exact witness and recomputation in baseline_examples/recomputed_examples.json. Verified max U=21, sumset 26, difference set 39, and 39<43."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
true
```

### remaining

```json
"Recompute the seven-element score only if desired; search the enlarged budget is open. Keep the published size≤11 optimality statement from being applied to this larger configuration."
```

## T060

### parameters

```json
{
  "v": 24,
  "k": 14,
  "t": 4
}
```

### scalar

```json
"minimum number of blocks C(24,14,4)"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 23,
  "author": "La Jolla Covering Repository contributor record (attribution requires row lookup)",
  "year": null,
  "description": "The currently cited repository/research tracker gives a 23-block construction; the public lower bound is 20."
}
```

### current_record

```json
{
  "value": "20–23",
  "scope": "Lean repository says C(24,14,4) ≥ 20; best known covering has 23 blocks."
}
```

### open_evidence

```json
"The cited public source reports a nonzero interval 20–23; no optimality proof for 23 is stated."
```

### witness_url

```json
"https://dmgordon.org/ljcr/"
```

### primary_sources

```json
[
  "https://github.com/jamesyc/covering",
  "https://dmgordon.org/ljcr/",
  "https://ljcr.dmgordon.org/cover.html"
]
```

### checks_performed

```json
[
  "Opened public Lean repository; verified parameters, lower bound 20, and listed best known construction size 23."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Identify the exact 23-block row and contributor in the covering repository; verify coverage if this is released."
```

## T060

### parameters

```json
{
  "v": 25,
  "k": 15,
  "t": 5
}
```

### scalar

```json
"minimum number of blocks C(25,15,5)"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": 42,
  "author": "La Jolla Covering Repository (original attribution not yet extracted)",
  "year": null,
  "description": "The public project README identifies 42 as the known construction size."
}
```

### current_record

```json
{
  "value": "34–42",
  "scope": "The Lean repository proves a lower bound 34 from C(24,14,4)≥20 and reports a 42-block known covering."
}
```

### open_evidence

```json
"The project states that the 41-block question is unresolved; this configuration is not proved optimal."
```

### witness_url

```json
"https://github.com/jamesyc/covering"
```

### primary_sources

```json
[
  "https://github.com/jamesyc/covering",
  "https://dmgordon.org/ljcr/"
]
```

### checks_performed

```json
[
  "Opened repository README; verified C(25,15,5), lower bound 34, known cover size 42, and unresolved 41-block question."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve the repository row and block list; retain this as a reported human construction until its attribution and coverage are checked."
```

## T061

### parameters

```json
{
  "N": "pending_configuration",
  "o": "pending_configuration",
  " ": "pending_configuration",
  "a": "pending_configuration",
  "d": "pending_configuration",
  "m": "pending_configuration",
  "i": "pending_configuration",
  "t": "pending_configuration",
  "e": "pending_configuration",
  "v": "pending_configuration",
  "2": "pending_configuration",
  "c": "pending_configuration",
  "n": "pending_configuration",
  "f": "pending_configuration",
  "g": "pending_configuration",
  "u": "pending_configuration",
  "r": "pending_configuration",
  ".": "pending_configuration",
  "S": "pending_configuration",
  "s": "pending_configuration",
  "y": "pending_configuration",
  "-": "pending_configuration",
  "l": "pending_configuration",
  ";": "pending_configuration",
  "1": "pending_configuration",
  "b": "pending_configuration",
  "x": "pending_configuration"
}
```

### scalar

```json
"number of rows N"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "NIST Covering Array Library lists actual arrays for strengths 2–6 and 2–6 levels, plus best-known sizes to 20,000 columns (strength 2) and 10,000 (strengths 3–6); NIST and Colbourn records are human constructions/bounds."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://csrc.nist.gov/Projects/Automated-Combinatorial-Testing-for-Software/Covering-Array-Library",
  "https://math.nist.gov/coveringarrays/coveringarray.html"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T062

### parameters

```json
{
  "t": "pending_configuration",
  "q": "pending_configuration",
  "k": "pending_configuration"
}
```

### scalar

```json
"number of rows N; λ=N/q^t is variable"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "Neil Sloane's library contains 200+ explicit arrays; Eendebak–Schoen catalogue complete non-isomorphic arrays for selected small parameters. OA( N,k,s,t) must meet divisibility/Rao bounds."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://neilsloane.com/oadir/index.html"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T063

### parameters

```json
{
  "v": "pending_configuration",
  "k": "pending_configuration",
  "t": "pending_configuration"
}
```

### scalar

```json
"number of blocks"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "La Jolla covering repository focuses on coverings, while classical packing bounds and constructions are published; candidate instance-level records require dedicated database/source review."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://dmgordon.org/ljcr/"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T064

### parameters

```json
{
  "players": "pending_configuration",
  "group_size": "pending_configuration",
  "groups_per_round": "pending_configuration"
}
```

### scalar

```json
"number of rounds"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "CSPLib problem 010 defines the canonical 32 golfers in groups of four and its generalization; published constraint-programming literature reports solved/optimal schedules for small parameter sets, but benchmark records need per-instance capture."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://csplib.github.io/csplib-PR-builds/PR-21/Problems/prob010/",
  "https://www.csplib.org/Problems/prob010/"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T065

### parameters

```json
{
  "order": "pending_configuration"
}
```

### scalar

```json
"number of MOLS"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "Bruck–Ryser–Chowla gives nonexistence restrictions; complete values are known for several small orders, while the standard MOLS tables record constructions and bounds."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://doi.org/10.1016/0012-365X(74)90148-4",
  "https://www.dcs.gla.ac.uk/~pat/cpM/jchoco/latinSquares/papers/10%5B1%5D.1.1.49.7739.pdf"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T066

### parameters

```json
{
  "n": 68,
  "k": 15,
  "q": 2
}
```

### scalar

```json
"maximum minimum Hamming distance d of a binary linear [68,15] code"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 24,
  "author": "Markus Grassl / Magma BKLC construction table",
  "year": 2001,
  "description": "Table gives a [68,15,24] code and its construction chain, including a [68,18,24] parent code and a subcode."
}
```

### current_record

```json
{
  "value": "24 ≤ d_max ≤ 26",
  "scope": "Grassl table reports lower bound 24 and upper bound 26."
}
```

### open_evidence

```json
"The published database separates lower and upper bounds, so the exact optimum is not established by that record."
```

### witness_url

```json
"https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2"
```

### primary_sources

```json
[
  "https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2"
]
```

### checks_performed

```json
[
  "Opened the exact parameter page; verified bounds 24 and 26 and visible construction chain."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Reconstruct/download a generator matrix and calculate its weight distribution before replay status."
```

## T067

### parameters

```json
{
  "n": 17,
  "distance": 6
}
```

### scalar

```json
"maximum code size A(17,6)"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": 258,
  "author": "Moshe Milshtein",
  "year": 2019,
  "description": "Brouwer table lists the lower bound 258 for binary length 17, distance 6."
}
```

### current_record

```json
{
  "value": "258–340",
  "scope": "Brouwer table gives lower and upper bounds."
}
```

### open_evidence

```json
"The maintained table gives a gap from 258 to 340 and does not mark the entry optimal."
```

### witness_url

```json
"https://aeb.win.tue.nl/codes/binary-1.html"
```

### primary_sources

```json
[
  "https://aeb.win.tue.nl/codes/binary-1.html"
]
```

### checks_performed

```json
[
  "Opened Brouwer table and verified row n=17, d=6 has bounds 258–340."
]
```

### status

```json
"confirmed_suitable"
```

### recomputed

```json
false
```

### remaining

```json
"Retrieve Milshtein’s explicit construction or codeword list; check for any newer construction before freezing a score."
```

## T068

### parameters

```json
{
  "n": "pending_configuration",
  "d": "pending_configuration",
  "w": "pending_configuration"
}
```

### scalar

```json
"Code size |C|"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "Brouwer, Shearer, Sloane and Smith (1990) compiled bounds; many later explicit constructions and improved bounds. Pin row and construction before benchmark inclusion; human baseline, no AI assumed."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://aeb.win.tue.nl/codes/Andw.html"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T069

### parameters

```json
{
  "q": "pending_configuration",
  "n": "pending_configuration",
  "k": "pending_configuration",
  "d": "pending_configuration"
}
```

### scalar

```json
"Code size |C|"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "Heinlein, Kiermaier, Kurz and Wassermann (2016, updated 2019) maintain Tables of Subspace Codes; the paper explicitly describes best lower/upper bounds and constructions. Fix an exact table row for score/construction."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://arxiv.org/abs/1601.02864",
  "https://subspacecodes.uni-bayreuth.de/"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T070

### parameters

```json
{
  "n": "pending_configuration",
  "R": "pending_configuration"
}
```

### scalar

```json
"Code size |C|"
```

### direction

```json
"minimize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "Cohen, Honkala, Litsyn and Lobstein (1997) survey and tabulate covering codes; select a small open/nontrivial instance and recover explicit construction."
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://neilsloane.com/doc/CR.html"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T071

### parameters

```json
{
  "n": "pending_configuration",
  "d": "pending_configuration"
}
```

### scalar

```json
"number of codewords"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "Bereg et al. (2019) Partition and Extension 给出显式人类构造与数值表；Ding–Fu–Kløve–Wei (2002)、Gao et al. (2008) 等经典构造可复现。需固定具体表格行。"
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://arxiv.org/abs/1804.08252",
  "https://arxiv.org/abs/0801.3987"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```

## T072

### parameters

```json
{
  "q": "pending_configuration",
  "n": "pending_configuration",
  "t": "pending_configuration"
}
```

### scalar

```json
"number of codewords"
```

### direction

```json
"maximize"
```

### human_baseline

```json
{
  "value": null,
  "author": null,
  "year": null,
  "description": "Varshamov–Tenengolts (1965) / Levenshtein (1966) 的二元单删除码有明确同余公式；按给定 n 枚举其码字可以得到可重算历史人类baseline。"
}
```

### current_record

```json
{
  "value": null,
  "scope": "No numerical configuration-specific record has been verified in this audit."
}
```

### open_evidence

```json
"No concrete configuration-specific optimality status has been verified. Do not treat this family as admitted yet."
```

### witness_url

```json
null
```

### primary_sources

```json
[
  "https://arxiv.org/abs/math/0207197",
  "https://neilsloane.com/doc/dijen.pdf"
]
```

### checks_performed

```json
[
  "Read the candidate-family definition and cited source list; did not verify a concrete configuration or witness."
]
```

### status

```json
"pending"
```

### recomputed

```json
false
```

### remaining

```json
"Select a concrete parameter set. Open and inspect a primary source for a human construction, verify its scalar value and witness, then check whether the configuration remains unsolved."
```
