# Discrete benchmark confirmation supplement (T061–T065, T068–T072)

Date: 2026-11-03

Supplementary audit; one record per assigned task; unresolved evidence remains pending.

Records: 10. Status count: confirmed_suitable=7, excluded_config=1, pending=2.

A `pending` status means the exact configuration or source-level evidence is still incomplete. A `confirmed_suitable` status means the public human construction and open interval meet the selection threshold; it does not mean the witness was independently replayed.

## T061

- **Parameters:** `{"k": 16, "t": 3, "v": 2}`
- **Scalar:** minimum row count CAN(3,16,2)
- **Direction:** minimize
- **Human baseline (value; author; year):** 17; Jose Torres-Jimenez, Idelfonso Izquierdo-Marquez, and collaborators; 2016. The non-isomorphic covering-array classification reports CAN(3,16,2)=17.
- **Current record / interval:** CAN(3,16,2)=17. Proved exact by exhaustive non-isomorphic covering-array classification.
- **Open evidence:** The primary 2016 classification paper reports CAN(3,16,2)=17. This configuration is solved and excluded.
- **Witness URL:** https://doi.org/10.1142/S1793830916500336
- **Primary sources:** <https://doi.org/10.1142/S1793830916500336>, <https://www.data2intelligence.de/ColbournTables/t3v2.html>
- **Checks performed:** The Colbourn-derived table lists a 17-row construction for 16 binary strength-three columns. The primary-paper abstract explicitly reports CAN(3,16,2)=17. Excluded this configuration because the exact minimum is published.
- **Status:** `excluded_config`
- **Remaining:** Replace with a larger CA cell only after verifying its construction and current lower bound.
- **Recomputed:** false

## T062

- **Parameters:** `{"N": 100, "index": 1, "q": 10, "t": 2}`
- **Scalar:** maximum number k of columns in OA(100,k,10,2), equivalently 2 plus the number of MOLS of order 10
- **Direction:** maximize
- **Human baseline (value; author; year):** 4; Ernest T. Parker; 1959. A published pair of orthogonal Latin squares of order 10 gives an OA(100,4,10,2).
- **Current record / interval:** 4 ≤ k ≤ 8. MOLS(10) is known to have at least two and at most six squares; equivalently k=2+N(10).
- **Open evidence:** This orthogonal-array cell is equivalent to T065: an OA(100,k,10,2) of index 1 corresponds to k−2 mutually orthogonal Latin squares of order 10 (for k≥2). The recorded k=4 construction and 4≤k≤8 gap therefore duplicate the MOLS(10) family rather than providing an independent benchmark. Do not count T062 as a separate confirmed family. A distinct OA target with strength at least 3 or index greater than 1 still needs a public construction and an open bound gap.
- **Witness URL:** https://www.pnas.org/doi/10.1073/pnas.45.6.859
- **Primary sources:** <https://www.pnas.org/doi/10.1073/pnas.45.6.859>, <https://cs.uwaterloo.ca/~cbright/reports/myrvold-mols.pdf>, <https://cs.uwaterloo.ca/~cbright/reports/delisle-mols.pdf>
- **Checks performed:** Verified Parker’s published order-10 pair and its index-one strength-two OA interpretation. Checked the published statement that N(10) is unknown, with interval 2 to 6 MOLS. Translated the interval to k=4 to 8 OA columns. Compared the OA(100,k,10,2), index-1 parameterization with the standard OA–MOLS correspondence: k columns correspond to k−2 MOLS of order 10. Identified full objective equivalence with T065.
- **Status:** `pending`
- **Remaining:** Choose an OA parameter cell not equivalent to T065, preferably strength at least 3 or index greater than 1; verify a public human construction and a nonzero published bound gap before promotion.
- **Recomputed:** false

## T063

- **Parameters:** `{"k": 5, "t": 2, "v": 22}`
- **Scalar:** maximum number of 5-subsets of a 22-set with no pair repeated, D(22,5,2)
- **Direction:** maximize
- **Human baseline (value; author; year):** 21; Finite-geometry construction: projective plane of order 4, restricted to 21 of the 22 points; 1938. The 21 lines of PG(2,4) are 5-subsets with every pair occurring once; on a 22-set, leave one point unused.
- **Current record / interval:** 21 ≤ D(22,5,2) ≤ 23 by the elementary pair count. A current exact-parameter specialist table was not verified; a stronger upper bound or exact result may exist.
- **Open evidence:** The projective-plane construction gives 21 blocks; counting pairs gives an upper bound floor(C(22,2)/C(5,2))=23. This is a gap, but current specialist bounds and exact status were not established, so this record remains pending.
- **Witness URL:** https://mathworld.wolfram.com/ProjectivePlane.html
- **Primary sources:** <https://mathworld.wolfram.com/ProjectivePlane.html>, <https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS18>
- **Checks performed:** Replaced the solved D(19,4,2)=25 configuration. Verified the order-4 projective plane has 21 points, 21 lines of size five, and every pair on one line. Computed the elementary upper bound 23 by counting pairs. Did not verify a current specialist table or rule out a stronger upper bound.
- **Status:** `pending`
- **Remaining:** Find a primary packing-number table or paper for D(22,5,2), verify current endpoints, and confirm the cell is not exact.
- **Recomputed:** false

## T064

- **Parameters:** `{"group_size": 5, "groups_per_round": 6, "players": 30}`
- **Scalar:** maximum number of rounds with no pair of players meeting twice
- **Direction:** maximize
- **Human baseline (value; author; year):** 6; Alice Miller, Ivaylo Valkov, and R. Julian R. Abel; 2025. Their table gives a six-round construction for 30 players in six groups of five, from a uniformly resolvable design.
- **Current record / interval:** 6 ≤ optimum ≤ 7. The primary table gives a construction at r=6 and the elementary per-player bound MAX=7.
- **Open evidence:** The 2025 primary paper lists 30 players, group size five, MAX=7 and a six-round construction. The bounds do not meet. It distinguishes optimal (no larger solution known) from maximal (proved impossible to improve).
- **Witness URL:** https://arxiv.org/html/2507.23376v2
- **Primary sources:** <https://arxiv.org/html/2507.23376v2>
- **Checks performed:** Verified the canonical 32-player, group-size-four instance is solved at 10 rounds and replaced it. Checked Table 8 for v=30, K=5: MAX=7 and URD({30,5,2}) construction with r=6. Checked the paper’s definitions distinguishing optimal and maximal schedules.
- **Status:** `confirmed_suitable`
- **Remaining:** Extract the URD({30,5,2}) block list from the cited construction and verify pair uniqueness.
- **Recomputed:** false

## T065

- **Parameters:** `{"order": 10}`
- **Scalar:** maximum number N(10) of pairwise orthogonal Latin squares of order 10
- **Direction:** maximize
- **Human baseline (value; author; year):** 2; Ernest T. Parker; 1959. Parker publishes a pair of orthogonal Latin squares of order 10, explicitly displayed in the paper.
- **Current record / interval:** 2 ≤ N(10) ≤ 6. Pair construction is known; an upper bound of 6 follows from Bruck's theorem. Whether a triple exists remains unresolved in the cited literature.
- **Open evidence:** The Waterloo-hosted primary report on MOLS states the order-10 maximum is unknown; the cited classical construction gives at least two, and Bruck's bound gives at most six.
- **Witness URL:** https://cs.uwaterloo.ca/~cbright/reports/delisle-mols.pdf
- **Primary sources:** <https://www.pnas.org/doi/10.1073/pnas.45.6.859>, <https://cs.uwaterloo.ca/~cbright/reports/myrvold-mols.pdf>
- **Checks performed:** Reviewed the primary MOLS reports for the explicit pair and the current interval. Confirmed the objective is a single integer and the available interval is nontrivial; did not retype or independently verify the Latin squares.
- **Status:** `confirmed_suitable`
- **Remaining:** Retrieve and independently check the published pair before solver benchmarking.
- **Recomputed:** false

## T068

- **Parameters:** `{"d": 6, "n": 18, "w": 5}`
- **Scalar:** maximum size A(18,6,5) of a binary constant-weight code
- **Direction:** maximize
- **Human baseline (value; author; year):** 69; Hui Kheng Aw, Yeow Meng Chee, and Alan C. H. Ling; 2003. Their paper constructs a binary constant-weight code with length 18, distance 6, weight 5, and 69 codewords.
- **Current record / interval:** 69 ≤ A(18,6,5) ≤ 72. Brouwer's specialist table gives lower bound 69 and upper bound 72.
- **Open evidence:** Brouwer's table identifies the 69-code construction as ACL (2003) and gives upper bound 72; it states the table entries are lower and upper bounds and distinguishes exact values.
- **Witness URL:** https://combinatorialpress.com/ars-articles/volume-067-ars-articles/six-new-constant-weight-binary-codes/
- **Primary sources:** <https://aeb.win.tue.nl/codes/Andw.html>, <https://combinatorialpress.com/ars-articles/volume-067-ars-articles/six-new-constant-weight-binary-codes/>
- **Checks performed:** Checked the exact table cell and source legend: 69 lower bound, 72 upper bound, ACL author/year. Verified the table defines A(n,d,w) and notes that single values denote known exact values; this cell has a gap. Did not retrieve or replay the code words.
- **Status:** `confirmed_suitable`
- **Remaining:** Fetch the paper's construction and independently check weight and pairwise distances.
- **Recomputed:** false

## T069

- **Parameters:** `{"d": 4, "k": 4, "n": 8, "q": 2}`
- **Scalar:** maximum size A_2(8,4;4) of a constant-dimension subspace code
- **Direction:** maximize
- **Human baseline (value; author; year):** 4801; Daniel Heinlein, Michael Kiermaier, Sascha Kurz, and Alfred Wassermann (construction cited as [39] in the survey); 2017. A published automorphism-prescription construction gives an (8,4;4)_2 code of 4801 subspaces; a further public construction adds one codeword, giving at least 4802.
- **Current record / interval:** 4801 ≤ A_2(8,4;4) ≤ 6477. The Bayreuth specialist table (2019) lists the exact cell as the interval 4801–6477; the same source explains the table stores lower and upper bounds when the value is not known exactly.
- **Open evidence:** The Bayreuth table lists A_2(8,4;4) as 4801–6477, a strict gap. Its survey describes the 4801 construction and a later extension to 4802. The construction baseline is public, while the optimum remains undetermined in the cited table.
- **Witness URL:** https://subspacecodes.uni-bayreuth.de/table/2/8/4/4/
- **Primary sources:** <https://epub.uni-bayreuth.de/4571/1/tables_subspace_codes.pdf>, <https://epub.uni-bayreuth.de/7398/1/chap_subspace_codes_arxiv.pdf>, <https://subspacecodes.uni-bayreuth.de/table/2/8/4/4/>
- **Checks performed:** Read the Bayreuth specialist table PDF at its binary n=8, k=4, d=4 cell: 4801–6477. Read the survey discussion of the cell and its 4801 construction / extension to 4802. Did not independently validate the subspace code.
- **Status:** `confirmed_suitable`
- **Remaining:** Before solver use, obtain the public construction and independently validate its subspaces and pairwise distances.
- **Recomputed:** false

## T070

- **Parameters:** `{"R": 1, "n": 27}`
- **Scalar:** minimum size K₂(27,1) of a binary length-27 radius-one covering code
- **Direction:** minimize
- **Human baseline (value; author; year):** 67108864; Richard W. Hamming; 1950. Puncturing four coordinates from the binary [31,26,3] Hamming code preserves radius at most one and gives a length-27 code of size 2^26.
- **Current record / interval:** 4,793,495 ≤ K₂(27,1) ≤ 67,108,864. Habsieger’s improved lower bound and the punctured Hamming-code construction give a finite gap.
- **Open evidence:** Habsieger proved K(27,1)≥4,793,495. Puncturing a perfect binary Hamming code gives a feasible length-27 radius-one code of size 2^26. The cited sources do not state that these bounds coincide.
- **Witness URL:** https://fpsac-archive.github.io/FPSAC95/ARTICLES/25.HABSIEGER.pdf
- **Primary sources:** <https://fpsac-archive.github.io/FPSAC95/ARTICLES/25.HABSIEGER.pdf>, <https://old.sztaki.hu/~keri/codes/index.htm>
- **Checks performed:** Replaced the small length-10 radius-two candidate with length 27, radius one. Verified Habsieger’s lower bound K(27,1)≥4,793,495. Derived the 2^26 feasible upper bound by puncturing the [31,26,3] perfect Hamming code; puncturing preserves covering radius at most one. Did not retrieve or replay a parity-check matrix.
- **Status:** `confirmed_suitable`
- **Remaining:** Retrieve a public Hamming parity-check matrix and validate the punctured code’s covering radius and size.
- **Recomputed:** false

## T071

- **Parameters:** `{"d": 13, "n": 16}`
- **Scalar:** maximum size M(16,13) of a permutation code in S16 with Hamming distance at least 13
- **Direction:** maximize
- **Human baseline (value; author; year):** 1266; Derek H. Smith and Roberto Montemanni; 2012. Their table reports a 1266-word code constructed by iterative clique building on cycles of length 16.
- **Current record / interval:** 1266 ≤ M(16,13) ≤ 43,680. Primary table lists the constructed lower endpoint and an upper bound.
- **Open evidence:** The primary table lists lower bound 1266 and upper bound 43,680; it labels these separately and makes no exact-value claim for the gap.
- **Witness URL:** https://doi.org/10.1007/s10623-011-9551-8
- **Primary sources:** <https://doi.org/10.1007/s10623-011-9551-8>, <https://iris.unimo.it/handle/11380/1176210>
- **Checks performed:** Checked Table 3 for n=16,d=13: lower bound 1266 and upper bound 43,680. Checked the table legend: constructed codes are lower bounds and upper bounds are cited separately. Did not retrieve or replay the permutation list.
- **Status:** `confirmed_suitable`
- **Remaining:** Retrieve the code source and verify pairwise Hamming distances before solver use.
- **Recomputed:** false

## T072

- **Parameters:** `{"n": 31, "q": 2, "t": 1}`
- **Scalar:** maximum size of a binary length-31 code correcting one deletion
- **Direction:** maximize
- **Human baseline (value; author; year):** 67108864; R. R. Varshamov and G. M. Tenengolts; 1965. A VT checksum class modulo n+1 gives a single-deletion-correcting code; at n=31 its classes have size 2^26.
- **Current record / interval:** 67,108,864 ≤ A_del(31,1) ≤ 71,582,788. Lower endpoint is a length-31 VT class; upper endpoint is floor((2^31−2)/30) from the explicit non-asymptotic bound of Kulkarni and Kiyavash (2013). The paper identifies determining the largest single-deletion code as open and reports exact optimality only through n≤10.
- **Open evidence:** The primary 2013 paper states that determining the largest single-deletion code is an open problem, reports exact optimality through lengths n≤10, and gives the general upper bound floor((2^n−2)/(n−1)) for binary codes. At n=31 this is 71,582,788, strictly above the VT construction size 67,108,864. The resulting published-source interval is nonzero.
- **Witness URL:** https://doi.org/10.1007/s10623-023-01342-1
- **Primary sources:** <https://publish.illinois.edu/kiyavash/files/2015/06/Kulkarni_it_trans_2013.pdf>, <https://doi.org/10.1007/s10623-023-01342-1>
- **Checks performed:** Verified the primary paper calls determination of the maximum single-deletion code an open problem and gives the binary upper bound (2^n−2)/(n−1). Evaluated the bound at n=31: floor((2^31−2)/30)=71,582,788. Counted all 32 checksum classes of sum(i*x_i) mod 32 by exact integer dynamic programming; each class has 67,108,864 words. Checked the later primary paper for the stated VT optimality range; n=31 is beyond proved exact cases.
- **Status:** `confirmed_suitable`
- **Remaining:** Before solver use, retrieve a compact public VT witness description and verify the deletion-correction property with a certificate or independent checker.
- **Recomputed:** false
