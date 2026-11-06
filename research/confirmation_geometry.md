# Geometry benchmark configuration confirmation

Date: 2026-11-03. Scope: T001–T034 excluding deleted T018, plus N003.

Confirmed suitable: 29 (T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011, T012, T013, T014, T015, T016, T019, T023, T024, T025, T026, T027, T028, T029, T030, T031, T032, T033, N003). Recomputed: 0. Pending: 4 (T017, T021, T022, T034). Excluded: 1 (T020).

Confirmed suitable means a specific mathematical parameter or a fixed public challenge corpus has a human feasible construction and source evidence that does not prove the selected optimization configuration optimal. These are source confirmations, not independent recomputations. Competition scores are heuristic results, not optimality certificates.

## Excluded configurations

- **T020:** MDTP2014a public benchmark set (210 instances, 10–70 points). 2025 exact-algorithm paper reports provably optimal MDT solutions for public benchmark instances up to 30,000 points; this legacy set falls within the solved size range. No replacement open instance selected.

## T001

**Parameters:** n=26, unit square

**Scalar:** maximum common radius in unit square (equivalently minimum container side for unit disks)

**Direction:** maximize

**Human baseline:** {"value": "Nurmela–Östergård circle packing, common radius 0.096362339010", "author": "Kari J. Nurmela and Patric R. J. Östergård", "year": "1999"}

**Current record:** Current best-known radius 0.096362339010 (table row; coordinates download exposed).

**Open evidence:** Record is listed as best known, not bold; Packomania states bold radius means proven optimal.

**Witness URL:** https://www.packomania.com/csqv/csqv26-old1.html

**Primary sources:** ["https://packomania.com/csq/", "https://www.packomania.com/csqv/csqv26-old1.html"]

**Checks performed:** Confirmed suitable; source record and coordinate location checked. Witness has not been retrieved or recomputed.

**Status:** confirmed_suitable

**Remaining:** Retrieve the linked construction, independently recompute its scalar and feasibility, and freeze the source/version.

## T002

**Parameters:** n=26 unit squares in a square

**Scalar:** minimum enclosing-square side s(n)

**Direction:** minimize

**Human baseline:** {"value": "Friedman unit-square packing, side (7+3√2)/2 = 5.62132034355964", "author": "Erich Friedman", "year": "1997"}

**Current record:** Verified upper construction and verified lower bound are reported; optimum remains open.

**Open evidence:** Squares Project marks n=26 open; verified interval 5.545 ≤ s(26) ≤ 5.62132034356.

**Witness URL:** https://squaremath.org/cases/26.html

**Primary sources:** ["https://squaremath.org/cases/26.html", "https://erich-friedman.github.io/papers/squares/squares.html"]

**Checks performed:** Confirmed suitable; source reports open status and verified bounds. Witness has not been retrieved or recomputed.

**Status:** confirmed_suitable

**Remaining:** Retrieve the linked construction, independently recompute its scalar and feasibility, and freeze the source/version.

## T003

**Parameters:** n=4 unit equilateral triangles; arbitrary orientations; enclosing square minimized

**Scalar:** minimum enclosing-square side s(4)

**Direction:** minimize

**Human baseline:** {"value": "s(4)=1+1/√3 ≈ 1.577350269; public construction shown on Friedman’s maintained packing page", "author": "Erich Friedman", "year": "1996"}

**Current record:** s(4)=1+1/√3 ≈ 1.577350269, listed as found by Friedman; the page describes smallest known packings and gives a construction image.

**Open evidence:** On the maintained page n=4 is marked Found by Friedman (1996), while proved cases have a separate “Proved by” attribution. The n=4 entry has no proof attribution; this is evidence of a best-known construction, not a formal proof that no proof exists elsewhere.

**Witness URL:** https://erich-friedman.github.io/packing/triinsqu/

**Primary sources:** ["https://erich-friedman.github.io/packing/triinsqu/"]

**Checks performed:** Read the n=4 entry, objective definition, baseline value and attribution on the maintained source. The source distinguishes found from proved entries. Construction coordinates have not been extracted or recomputed.

**Status:** confirmed_suitable

**Remaining:** Extract the construction from the linked image or source file, then verify containment and side length; search for an independent proof before release.

## T004

**Parameters:** CG:SHOP 2024 instance random_cf3_x21f5def_200; fixed official item and container data; translations only

**Scalar:** maximize total value of selected packed items

**Direction:** maximize

**Human baseline:** {"value": "Shadoks solution packs items of total value 12,593/12,593 (competition normalized score 1); public solution JSON and visualizer are linked.", "author": "Guilherme D. da Fonseca and Yan Gerard (Shadoks)", "year": "2024"}

**Current record:** Shadoks solution for random_cf3_x21f5def_200 has value 12,593; score 1 means it matches the best submitted value under contest scoring, not a mathematical optimality certificate.

**Open evidence:** The official challenge defines its score against the best submitted solution. The team paper describes heuristic/ILP starts plus local search and does not claim a global certificate for this instance. Treat as source-level open candidate; check for later exact proof before release.

**Witness URL:** https://pageperso.lis-lab.fr/guilherme.fonseca/cgshop24view/HTML_SOLUTIONS/random_cf3_x21f5def_200.html

**Primary sources:** ["https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2024/", "https://arxiv.org/abs/2403.20123", "https://pageperso.lis-lab.fr/guilherme.fonseca/cgshop24view/HTML_SOLUTIONS/random_cf3_x21f5def_200.html"]

**Checks performed:** Read official task definition and Shadoks viewer entry for the exact instance, baseline value and score. The witness JSON was not downloaded or independently validated.

**Status:** confirmed_suitable

**Remaining:** Download the solution JSON and input, independently validate packing and score, and check for a later optimality certificate.

## T005

**Parameters:** n=26 variable-radius circles in unit square

**Scalar:** maximize sum_i r_i

**Direction:** maximize

**Human baseline:** {"value": "0.096362339010 radius for each of 26 equal circles; total sum 2.505420814260, a feasible human baseline.", "author": "Nurmela–Östergård, 1999", "year": "1999"}

**Current record:** 0.096362339010 radius for each of 26 equal circles; total sum 2.505420814260, a feasible human baseline.

**Open evidence:** Current strongest listed sum 2.635983084919; Packomania says bold values alone indicate proven optima. This source reports n=26 non-bold.

**Witness URL:** https://packomania.com/csqv/csqv.html

**Primary sources:** ["https://packomania.com/csq/", "https://packomania.com/csqv/csqv.html"]

**Checks performed:** Packomania csqv page specifies unit-square free-radius sum objective, exposes coordinate archive, marks solved instances by boldface; n=26 record unbolded. Equal-circle construction is public in Packomania csq; its sum is 26×r. No coordinate recheck.

**Status:** confirmed_suitable

**Remaining:** Retrieve equal-circle coordinate witness and verify containment/non-overlap and sum; freeze current frontier separately.

## T006

**Parameters:** 11 pairwise interior-disjoint squares, any orientation, inside unit square

**Scalar:** maximize sum of side lengths

**Direction:** maximize

**Human baseline:** {"value": "For n=k²+2 with k=3, explicit construction has total side length at least 3+1/4=3.25.", "author": "Sylvia Halász, 1984", "year": "1984"}

**Current record:** For n=k²+2 with k=3, explicit construction has total side length at least 3+1/4=3.25.

**Open evidence:** Erdős–Campbell–Staton equality is conjectural; no proof of optimality at n=11 found.

**Witness URL:** https://www.sciencedirect.com/science/article/pii/0097316584900244

**Primary sources:** ["https://www.sciencedirect.com/science/article/pii/0097316584900244"]

**Checks performed:** Read Halász paper abstract and the cited exact construction formula; later literature labels equality conjectural.

**Status:** confirmed_suitable

**Remaining:** Retrieve/reconstruct the 11-square layout and verify exact non-overlap and side sum.

## T007

**Parameters:** n=21 unit disks cover a circular target; maximize target radius

**Scalar:** maximum radius of a circular target covered by 21 unit circles

**Direction:** maximize

**Human baseline:** {"value": "target radius 3.804+; public construction diagram is listed", "author": "Jeremy Tan", "year": "2018"}

**Current record:** Friedman’s maintained table lists radius 3.804+ for n=21, found by Jeremy Tan in 2018.

**Open evidence:** The same page explicitly marks n=11–20 as proved (including 2026 attributions for 11–20). The n=21 entry is listed as found and has no proof attribution. This supports an unproved-record candidate but is not an exhaustive literature search.

**Witness URL:** https://erich-friedman.github.io/packing/circovcir/

**Primary sources:** ["https://erich-friedman.github.io/packing/circovcir/"]

**Checks performed:** Read the page definition and n=21 record; checked the adjacent n=11–20 proof labels to avoid selecting one of the newly solved cases. Coordinates not extracted or recomputed.

**Status:** confirmed_suitable

**Remaining:** Retrieve construction and exact parameters from the page image; verify the coverage radius and check for later proof before release.

## T008

**Parameters:** 8 unit squares may overlap while covering a target square

**Scalar:** maximize target-square side length

**Direction:** maximize

**Human baseline:** {"value": "Target square area 3+2√2, so side √(3+2√2)=1+√2; source provides a construction diagram.", "author": "Trevor Green, September 2000", "year": "2000"}

**Current record:** Target square area 3+2√2, so side √(3+2√2)=1+√2; source provides a construction diagram.

**Open evidence:** Friedman–Paterson state optimality is known only for n=2,3,5,10 and square n; n=8 is open.

**Witness URL:** https://erich-friedman.github.io/packing/squcosqu/

**Primary sources:** ["https://erich-friedman.github.io/papers/covering/covering.html", "https://erich-friedman.github.io/packing/squcosqu/"]

**Checks performed:** Read n=8 construction value/author and paper’s explicit list of solved n.

**Status:** confirmed_suitable

**Remaining:** Recover the figure coordinates and verify that eight unit squares cover the stated target.

## T009

**Parameters:** 15 points on S²

**Scalar:** maximize minimum pairwise angular separation

**Direction:** maximize

**Human baseline:** {"value": "cosine of minimum angular separation 0.592605902925 (table gives construction and downloadable coordinate data).", "author": "Henry Cohn maintained spherical-code table", "year": "see note"}

**Current record:** cosine of minimum angular separation 0.592605902925 (table gives construction and downloadable coordinate data).

**Open evidence:** Cohn states starred entries are known optimal; N=15 entry is unstarred.

**Witness URL:** https://spherical-codes.org/

**Primary sources:** ["https://spherical-codes.org/"]

**Checks performed:** Read table legend and N=15 row; public dataset coordinates are linked. This confirms a construction and non-optimality status, not a recomputation.

**Status:** confirmed_suitable

**Remaining:** Retrieve coordinate data and independently recompute minimum pairwise angle.

## T010

**Parameters:** N=100 charges on unit sphere; Coulomb exponent s=1

**Scalar:** minimize sum_{i<j} 1/||x_i-x_j||

**Direction:** minimize

**Human baseline:** {"value": "Energy 4448.3506343; point group T; xyz coordinate link present.", "author": "D. J. Wales and S. Ulker", "year": "see note"}

**Current record:** Energy 4448.3506343; point group T; xyz coordinate link present.

**Open evidence:** The database calls the entries lowest minima located and describes basin-hopping results; no global proof is claimed.

**Witness URL:** https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html

**Primary sources:** ["https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html"]

**Checks performed:** Read N=100 energy and coordinate link, authors/year and update note. The record is a located minimum, not a certified global optimum.

**Status:** confirmed_suitable

**Remaining:** Retrieve xyz coordinates and independently recompute Coulomb energy.

## T011

**Parameters:** 3D equal-weight spherical 9-design; N=48 points

**Scalar:** minimize N for fixed strength t=9

**Direction:** minimize

**Human baseline:** {"value": "N=48, t=9 design (V1 algebraic existence entry in their table; construction coordinates in the 3D library).", "author": "R. H. Hardin and N. J. A. Sloane", "year": "see note"}

**Current record:** N=48, t=9 design (V1 algebraic existence entry in their table; construction coordinates in the 3D library).

**Open evidence:** Hardin–Sloane describe tau(N) as conjectured and their numerical table as putatively optimal; no minimum-N theorem for t=9 is claimed.

**Witness URL:** https://neilsloane.com/sphdesigns/index.html

**Primary sources:** ["https://neilsloane.com/sphdesigns/index.html"]

**Checks performed:** Read definition, N=48 row, conjectural status statement and public library link.

**Status:** confirmed_suitable

**Remaining:** Retrieve listed coordinates and verify equal-weight moment conditions through degree 9.

## T012

**Parameters:** 10 vertices on S² in R³

**Scalar:** maximize convex-hull volume

**Direction:** maximize

**Human baseline:** {"value": "Putatively optimal listed volume 2.218711131545; public arrangement library linked.", "author": "R. H. Hardin, N. J. A. Sloane, W. D. Smith", "year": "see note"}

**Current record:** Putatively optimal listed volume 2.218711131545; public arrangement library linked.

**Open evidence:** The maintained source labels these arrangements putatively optimal. The 2026 exact result is for N=9, not this N=10 configuration.

**Witness URL:** https://neilsloane.com/maxvolumes/index.html

**Primary sources:** ["https://neilsloane.com/maxvolumes/index.html"]

**Checks performed:** Read source scope, putative-optimal label, N=10 value and coordinate-library link.

**Status:** confirmed_suitable

**Remaining:** Retrieve coordinate file and independently calculate convex-hull volume.

## T013

**Parameters:** N=9 points in a free convex region; normalize convex-hull area to 1

**Scalar:** maximize minimum area of a triangle formed by any three points, divided by convex-hull area

**Direction:** maximize

**Human baseline:** {"value": "A=0.0640647523079416…; public coordinate link and verifier are provided", "author": "David Cantrell", "year": "2007"}

**Current record:** The maintained table lists A=0.0640647523079416… as a record for N=9 and links coordinates.

**Open evidence:** The source states optimality has been established for n≤8. Its n=9 entry is marked “record,” not “proven,” and names Cantrell’s 2007 construction. This is configuration-level frontier evidence; it does not rule out an unlisted proof.

**Witness URL:** https://math.tejstead.com/heilbronn/convex/

**Primary sources:** ["https://math.tejstead.com/heilbronn/convex/"]

**Checks performed:** Read source definition and N=9 entry; confirmed the page states n≤8 solved and labels n=9 as record with coordinates. Witness has not been retrieved or recomputed.

**Status:** confirmed_suitable

**Remaining:** Download N=9 coordinates, independently recompute normalized minimum triangle area, and check for a later proof before release.

## T014

**Parameters:** n=11 points in unit square

**Scalar:** minimum area over all point triples

**Direction:** maximize

**Human baseline:** {"value": "minimum triangle area 1/27 for 11 points", "author": "Michael Goldberg", "year": "1972"}

**Current record:** Best-known record 1/27; source marks it record and provides coordinate download.

**Open evidence:** Tej Stead lists n≥11 as best-known, not proven optimal; coordinate link is provided.

**Witness URL:** https://math.tejstead.com/heilbronn/square/

**Primary sources:** ["https://math.tejstead.com/heilbronn/square/"]

**Checks performed:** Confirmed suitable; primary-maintainer page checked. Witness has not been retrieved or recomputed.

**Status:** confirmed_suitable

**Remaining:** Retrieve the linked construction, independently recompute its scalar and feasibility, and freeze the source/version.

## T015

**Parameters:** 9 distinct planar points

**Scalar:** minimize maximum pairwise distance / minimum pairwise distance

**Direction:** minimize

**Human baseline:** {"value": "Published construction has squared ratio 6.600+ and is shown in the public configuration gallery.", "author": "David Cantrell, February 2009", "year": "2009"}

**Current record:** Published construction has squared ratio 6.600+ and is shown in the public configuration gallery.

**Open evidence:** Friedman gallery marks solved small cases (through n=8) with proof statements; n=9 is listed as smallest known only.

**Witness URL:** https://erich-friedman.github.io/packing/maxmin/

**Primary sources:** ["https://erich-friedman.github.io/packing/maxmin/"]

**Checks performed:** Read n=9 record and proof status for earlier n; public construction image is present.

**Status:** confirmed_suitable

**Remaining:** Retrieve/reconstruct n=9 coordinates and recalculate the distance ratio.

## T016

**Parameters:** convex 14-gon of diameter at most 1

**Scalar:** maximize polygon area

**Direction:** maximize

**Human baseline:** {"value": "Regular 14-gon is explicit with area (14/8)sin(2π/14); Bingane–Mossinghoff give additional feasible constructions for every even n≥14.", "author": "Regular 14-gon baseline (classical construction); improved family by Bingane and Mossinghoff", "year": "see note"}

**Current record:** Regular 14-gon is explicit with area (14/8)sin(2π/14); Bingane–Mossinghoff give additional feasible constructions for every even n≥14.

**Open evidence:** The 2026 paper states maximal area is unknown for even n≥14; uses an explicit construction family and lower bounds.

**Witness URL:** https://arxiv.org/abs/2204.04547

**Primary sources:** ["https://arxiv.org/abs/2204.04547"]

**Checks performed:** Read abstract/introduction: even n≥14 open; regular polygon baseline and explicit human construction family described.

**Status:** confirmed_suitable

**Remaining:** Select the strongest coordinate construction for n=14 and recompute area/diameter.

## T017

**Parameters:** N=100 distinct points in the Euclidean plane; 10×10 integer square lattice construction

**Scalar:** minimize the number D(100) of distinct positive pairwise distances

**Direction:** minimize

**Human baseline:** {"value": "A 10×10 square lattice gives 50 distinct positive distances: the values sqrt(a²+b²) for 0≤a,b≤9, excluding (0,0). This is a feasible upper bound for D(100), not a claim of optimality.", "author": "Paul Erdős", "year": "1946"}

**Current record:** The square-grid construction is a public human feasible baseline. No exact value for D(100) was verified in this audit.

**Open evidence:** The grid gives an upper bound D(100)≤50. Guth–Katz and follow-up primary papers establish asymptotic lower bounds but do not settle D(100). The cited literature does not state a finite N=100 value or a matching lower bound. This audit therefore does not claim an exact N=100 optimum is open based only on the asymptotic gap.

**Witness URL:** https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p02-p.pdf

**Primary sources:** ["https://annals.math.princeton.edu/wp-content/uploads/annals-v181-n1-p02-p.pdf"]

**Checks performed:** Independently enumerated the 50 distinct squared distances a²+b² for 0≤a,b≤9. Read the primary Guth–Katz paper for its general lower-bound result; it does not give a matching N=100 certificate.

**Status:** pending

**Remaining:** Find a primary finite-case source that explicitly records the best lower and upper bounds for D(100), and preserve a cited human grid construction. Keep pending until an instance-level gap is sourced.

## T019

**Parameters:** k=7; general-position planar point set with N=32 points; exhibit a set with no convex 7-gon

**Scalar:** maximize N for a planar point set in general position that contains no convex 7-gon

**Direction:** maximize

**Human baseline:** {"value": "The Erdős–Szekeres recursive construction gives 2^(7−2)=32 points with no convex 7-gon. This is a feasible construction, not a proof that 32 is maximal.", "author": "Paul Erdős and George Szekeres", "year": "1935"}

**Current record:** The classical recursion provides a 32-point witness with no convex 7-gon.

**Open evidence:** The 1935 paper gives the recursive construction family; exact forcing values are known through k=6 in later primary literature, while the k=7 case remains an open problem in current references checked. The construction itself is a baseline and does not establish an upper bound of 32.

**Witness URL:** https://www.numdam.org/item/CM_1935__2__463_0/

**Primary sources:** ["https://www.numdam.org/item/CM_1935__2__463_0/", "https://arxiv.org/abs/1604.08657"]

**Checks performed:** Used the Erdős–Szekeres recursion at k=7 to get a 32-point no-convex-7-gon construction; checked current reference reports of known exact values through k=6. The explicit point coordinates were not reconstructed.

**Status:** confirmed_suitable

**Remaining:** Record a concrete representation of the recursive 32-point witness and verify the current exact status of k=7 against the latest primary literature before release.

## T020

**Parameters:** Excluded configuration: the public MDTP2014a benchmark set (210 point sets, 10–70 points); no replacement open configuration audited

**Scalar:** minimum, over triangulations, of maximum pairwise graph-distance / Euclidean-distance ratio

**Direction:** minimize

**Human baseline:** {"value": "The MDTP benchmark results are reported as provably optimal for the instances covered by the 2025 exact-algorithm paper.", "author": "Sándor P. Fekete, Phillip Keldenich, Michael Perk", "year": "2025"}

**Current record:** The exact-algorithm paper reports optimal solutions for public MDT benchmark instances up to 30,000 points; the legacy 10–70 point MDTP benchmark set is therefore not suitable as an open discovery configuration.

**Open evidence:** This is an exclusion: published exact solutions establish optimality on the benchmark family under review. No alternative configuration outside those solved instances was selected.

**Witness URL:** https://doi.org/10.20382/jocg.v17i2a1

**Primary sources:** ["https://doi.org/10.20382/jocg.v17i2a1", "https://www.ic.unicamp.br/~cid/Problem-instances/Dilation/MDTP/index.html"]

**Checks performed:** Read the paper abstract and benchmark-library description; confirmed the legacy set contains 210 instances with 10–70 points and the paper reports provably optimal benchmark solutions through much larger sizes. Individual result files were not replayed.

**Status:** excluded

**Remaining:** None for these solved benchmark instances. A future candidate must use a specific point set not covered by the exact-solution results and establish an open gap.

## T021

**Parameters:** No fixed point set selected; candidate family is minimum-weight triangulation of a finite planar point set, with hull edges and no Steiner points

**Scalar:** minimum total Euclidean length of triangulation edges

**Direction:** minimize

**Human baseline:** {"value": "Primary computational papers provide public point-set benchmark instances and feasible triangulations; no particular instance score has been selected in this record.", "author": "Brandt et al.", "year": "2018"}

**Current record:** No configuration-level baseline score was confirmed in this audit.

**Open evidence:** The problem is NP-hard in general, but that fact does not establish that a particular benchmark instance is unsolved. The cited large-scale paper solves many instances to optimality. No suitable open instance was identified.

**Witness URL:** https://arxiv.org/abs/1802.06415

**Primary sources:** ["https://arxiv.org/abs/1802.06415", "https://arxiv.org/abs/cs/0601002"]

**Checks performed:** Checked the cited paper scope: it reports provably optimal solutions for many benchmark classes. No per-instance frontier or witness was checked.

**Status:** pending

**Remaining:** Select a public point set absent from solved-result tables; record an explicit human triangulation and score, and document a valid lower bound showing a nonzero gap.

## T022

**Parameters:** CG:SHOP 2020 minimum convex partition instance uniform-0010000-1 (10,000 points); official rules and exact input file

**Scalar:** minimize number of bounded convex faces in a convex partition of the point-set hull

**Direction:** minimize

**Human baseline:** {"value": "Official best_solutions.zip contains a feasible partition edge set for uniform-0010000-1 (submitted 2020-02-21); face count not independently derived in this audit.", "author": "CG:SHOP 2020 participating teams", "year": "2020"}

**Current record:** A public feasible solution is present for uniform-0010000-1. The lower bound and exact face count were not extracted.

**Open evidence:** Cambazard–Catusse report 100-point data sets are easily solved to optimality and provide lower bounds up to 300 points. This 10,000-point official challenge instance is outside that stated exact range; that size distinction alone is not a proof of an unresolved gap. Keep pending until an instance-level lower/upper gap is recorded.

**Witness URL:** https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2020/

**Primary sources:** ["https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2020/", "https://pagesperso.g-scop.grenoble-inp.fr/~cambazah/convexpartition/minconvex.html"]

**Checks performed:** Downloaded the official public best_solutions.zip and confirmed a solution JSON for uniform-0010000-1 exists. Read the exact-method page stating 100-point data sets are solved and lower bounds computed up to 300. Did not replay the solution or extract its face count.

**Status:** pending

**Remaining:** Retrieve the matching input, validate the solution and count faces, and obtain a primary lower bound for uniform-0010000-1 to show whether a strict gap remains.

## T023

**Parameters:** CG:SHOP 2023 instance maze_2534_250_05_01 (505-hole maze polygon; official challenge instance)

**Scalar:** minimize number of convex polygons in a feasible cover of the region

**Direction:** minimize

**Human baseline:** {"value": "Public team solution list includes a 433-piece cover (solution label merge_autor, dated 2023-01-28).", "author": "CG:SHOP 2023 solution entry; viewer authors Rayis Berkat, Ian Bertin, Ulysse Holzinger, Julien Jamme (visualization); original solver attribution not verified", "year": "2023"}

**Current record:** The public Shadoks viewer solution list for maze_2534_250_05_01 records a 433-piece solution. This is a feasible value, not an optimum certificate.

**Open evidence:** The challenge paper scores each entry against the best submitted solution and states that this is a best-found baseline. The source does not report a proof of optimality for this named instance. The paper also reports heuristic cover construction; a later exact certificate was not searched exhaustively.

**Witness URL:** https://pageperso.lis-lab.fr/guilherme.fonseca/cgshop23view/src/html/listSoluces/listmaze_2534_250_05_01.html

**Primary sources:** ["https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/", "https://www.cgt-journal.org/index.php/cgt/article/download/115/74/737", "https://pageperso.lis-lab.fr/guilherme.fonseca/cgshop23view/src/html/listSoluces/listmaze_2534_250_05_01.html"]

**Checks performed:** Checked the challenge paper: 206 instances; scoring uses best submitted piece count, not an optimum certificate. Opened the maintained team viewer’s solution list and read data-nb=433 for the named instance. Original solver attribution not confirmed; solution not independently replayed.

**Status:** confirmed_suitable

**Remaining:** Retrieve and validate the 433-piece solution and input; verify the original solver byline and check for any later optimality certificate.

## T024

**Parameters:** CG:SHOP 2022 instance vispecn13806 (13,806 segments)

**Scalar:** minimum number of noncrossing classes partitioning all input segments

**Direction:** minimize

**Human baseline:** {"value": "Shadoks feasible coloring uses 218 classes; the largest reported clique lower bound is 177. These are distinct upper and lower bounds.", "author": "Crombez, da Fonseca, Gerard, Gonzalez-Lorenzo (Shadoks)", "year": "2022"}

**Current record:** For vispecn13806 the challenge paper reports best coloring 218 and largest found clique 177.

**Open evidence:** A primary 2023 paper reports that only 23 of 225 Shadoks colorings were proved optimal by matching clique size. Its table lists vispecn13806 with clique 177 and best coloring 218, so this instance is outside the explicitly certified subset in that source and has a documented 41-class bound gap. This is an open-frontier candidate, not a proof that no later certificate exists.

**Witness URL:** https://arxiv.org/abs/2203.07444

**Primary sources:** ["https://arxiv.org/abs/2203.07444", "https://arxiv.org/abs/2303.09632"]

**Checks performed:** Read official task definition and the primary 2023 table for vispecn13806; compared its feasible coloring 218 with clique lower bound 177 and the paper’s statement that 23/225 cases were proved optimal.

**Status:** confirmed_suitable

**Remaining:** Retrieve the official instance and Shadoks coloring for independent validation; check for any later certificate beyond the 2023 source.

## T025

**Parameters:** CG:SHOP 2025 instance simple-polygon_100_cb23308c

**Scalar:** minimize number of Steiner points in a constrained non-obtuse triangulation

**Direction:** minimize

**Human baseline:** {"value": "Winning implementation’s paper shows a feasible solution with 43 Steiner points.", "author": "Mikkel Abrahamsen, Florestan Brunck, Jacobus Conradi, Benedikt Kolbe, André Nusser", "year": "2025"}

**Current record:** The primary winning-team paper illustrates instance simple-polygon_100_cb23308c with 43 Steiner points.

**Open evidence:** The winning method is a local-search heuristic and the challenge paper gives no optimality certificate for this instance. This is a feasible baseline, not proof that 43 is minimal; a later instance-specific proof was not checked.

**Witness URL:** https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.79/LIPIcs.SoCG.2025.79.html

**Primary sources:** ["https://arxiv.org/abs/2504.04412", "https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.79/LIPIcs.SoCG.2025.79.html"]

**Checks performed:** Read the challenge definition and winning implementation paper; confirmed the exact figure caption and 43-point solution. Did not retrieve/recompute the triangulation.

**Status:** confirmed_suitable

**Remaining:** Retrieve the named instance and solution, verify every angle and constraint, and check for a later exact certificate.

## T026

**Parameters:** FHKPS instance figure4a-0000013-2; minimize-area simple polygonization of its fixed input point set

**Scalar:** minimum polygon area

**Direction:** minimize

**Human baseline:** {"value": "Primal feasible area 103562; dual lower bound 103557.9 (reported by the public benchmark results table).", "author": "Natanael Ramos, Pedro J. de Rezende, Cid C. de Souza and collaborators", "year": "2021"}

**Current record:** FHKPS-I-MI-results.csv reports primal 103562 and dual 103557.9 for figure4a-0000013-2; the bounds differ by 4.1.

**Open evidence:** The maintained benchmark reports separate primal and dual bounds for this fixed instance, with a strict gap. Its solution archive contains per-instance polygonizations. This records a computational bound gap, not a proof that a later paper has not closed it.

**Witness URL:** https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Polygon/

**Primary sources:** ["https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Polygon/", "https://doi.org/10.1145/3504000"]

**Checks performed:** Fetched the primary results CSV and confirmed the exact row; confirmed the benchmark page says each row has primal/dual bounds and matching solution files. Did not independently replay the polygon or objective.

**Status:** confirmed_suitable

**Remaining:** Retrieve the named input and solution from the official archives, validate simplicity and area, and check for later proof closure.

## T027

**Parameters:** FHKPS instance figure6-0000012-4; maximize-area simple polygonization of its fixed input point set

**Scalar:** maximum polygon area

**Direction:** maximize

**Human baseline:** {"value": "Primal feasible area 451240.5; dual upper bound 451265.9583 (reported by the public benchmark results table).", "author": "Natanael Ramos, Pedro J. de Rezende, Cid C. de Souza and collaborators", "year": "2021"}

**Current record:** FHKPS-I-MA-results.csv reports primal 451240.5 and dual 451265.9583 for figure6-0000012-4; the bounds differ by 25.4583.

**Open evidence:** The maintained benchmark reports separate primal and dual bounds for this fixed instance, with a strict gap. Its solution archive contains per-instance polygonizations. This records a computational bound gap, not a proof that a later paper has not closed it.

**Witness URL:** https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Polygon/

**Primary sources:** ["https://www.ic.unicamp.br/~cid/Problem-instances/Area-Optimal-Simple-Polygon/", "https://doi.org/10.1145/3504000"]

**Checks performed:** Fetched the primary results CSV and confirmed the exact row; confirmed the benchmark page says each row has primal/dual bounds and matching solution files. Did not independently replay the polygon or objective.

**Status:** confirmed_suitable

**Remaining:** Retrieve the named input and solution from the official archives, validate simplicity and area, and check for later proof closure.

## T028

**Parameters:** complete graph K_28 in straight-line drawing; 28 points in general position

**Scalar:** minimize number of crossing edge pairs

**Direction:** minimize

**Human baseline:** {"value": "Aichholzer construction gives an upper bound of 7234 crossings for K_28; a lower bound of 7233 is the other endpoint of the published interval.", "author": "Aichholzer construction record; bounds summarized by Abrego, Fernández-Merchant, and Salazar", "year": "2009"}

**Current record:** For rectilinear K_28, the published bounds are 7233 ≤ cr(K_28) ≤ 7234; the construction witness is the upper bound 7234.

**Open evidence:** The cited survey reports the one-crossing gap 7233–7234; 7233 is a lower bound, not the construction score. Thus the baseline is a feasible construction with 7234 crossings, and the exact optimum is unresolved in that source.

**Witness URL:** https://www.csun.edu/~sf70713/publications/survey.pdf

**Primary sources:** ["https://www.csun.edu/~sf70713/publications/survey.pdf"]

**Checks performed:** Corrected bound direction: feasible construction is the upper bound 7234; 7233 is the lower bound. The K_28 witness has not been retrieved or recounted.

**Status:** confirmed_suitable

**Remaining:** Retrieve the K_28 drawing/order type and verify its crossing count of 7234; check for any later exact result.

## T029

**Parameters:** n=25 planar points

**Scalar:** number of unit-distance pairs

**Direction:** maximize

**Human baseline:** {"value": "72 unit-distance edges for 25 points", "author": "Peter Engel, Owen Hammond-Lee, Yiheng Su, Dániel Varga, Pál Zsámboki", "year": "2025"}

**Current record:** Known construction lower bound 72; catalog audit reports 72≤u(25)≤73, but the certificate ledger was not replayed in this pass.

**Open evidence:** Paper states u(n) unknown for 15<n≤30; catalogues published densest graphs, with public code/database.

**Witness URL:** https://arxiv.org/abs/2406.15317

**Primary sources:** ["https://arxiv.org/abs/2406.15317", "https://artwaste.land/strata/every-edge-but-one/"]

**Checks performed:** Confirmed suitable, with frontier evidence pending independent replay. Witness/certificate not retrieved or recomputed.

**Status:** confirmed_suitable

**Remaining:** Replay the current upper-bound certificate and retrieve/recompute a human construction.

## T030

**Parameters:** 17 distinct planar points; count distinct lines containing exactly 3 points

**Scalar:** maximize number of 3-rich lines

**Direction:** maximize

**Human baseline:** {"value": "For p=17, cubic-curve construction yields at least 40 triple lines.", "author": "Stefan A. Burr, Branko Grünbaum, N. J. A. Sloane", "year": "see note"}

**Current record:** For p=17, cubic-curve construction yields at least 40 triple lines.

**Open evidence:** Their table gives lower bound 40 and upper bound 42; the table does not mark this case exact.

**Witness URL:** https://neilsloane.com/doc/Me34.pdf

**Primary sources:** ["https://neilsloane.com/doc/Me34.pdf"]

**Checks performed:** Read 1974 paper: construction theorem applies p>13 and table row p=17 reports 40 to 42.

**Status:** confirmed_suitable

**Remaining:** Recover the p=17 cubic-curve point parameters and count all 3-rich lines exactly.

## T031

**Parameters:** 94×94 lattice grid; n=94=2p with p=47 prime

**Scalar:** maximize selected lattice points subject to no three collinear

**Direction:** maximize

**Human baseline:** {"value": "Modular-hyperbola construction gives 3(p−1)=138 points at n=94.", "author": "R. R. Hall, T. H. Jackson, A. Sudbery, K. Wild", "year": "see note"}

**Current record:** Modular-hyperbola construction gives 3(p−1)=138 points at n=94.

**Open evidence:** General maximum is not proved for this n; current open-problem source states tightness of 2n only through n=70 and records the classical asymptotic construction.

**Witness URL:** https://doi.org/10.1016/0097-3165(75)90043-6

**Primary sources:** ["https://doi.org/10.1016/0097-3165(75)90043-6"]

**Checks performed:** Read primary paper metadata/abstract and current open-problem page; the published construction family is cited for n/2 prime. No point set replayed.

**Status:** confirmed_suitable

**Remaining:** Retrieve the exact p=47 construction and verify no collinear triples.

## T032

**Parameters:** simple perfect squared square, order 55

**Scalar:** primitive outer-square side length

**Direction:** minimize

**Human baseline:** {"value": "primitive side 740 for a simple perfect squared square of order 55", "author": "Bernard Moss", "year": "2020"}

**Current record:** Smallest known outer side 740; no optimality proof stated.

**Open evidence:** Squaring.net calls 740 the smallest known order-55 SPSS; it does not claim a minimum proof. Bouwkamp-code and table-code downloads are linked.

**Witness URL:** https://www.squaring.net/sq/ss/spss/o55/spsso55.html

**Primary sources:** ["https://www.squaring.net/sq/ss/spss/o55/spsso55.html"]

**Checks performed:** Confirmed suitable; source and downloadable code locations checked. Witness has not been retrieved or recomputed.

**Status:** confirmed_suitable

**Remaining:** Retrieve the linked construction, independently recompute its scalar and feasibility, and freeze the source/version.

## T033

**Parameters:** Outer square n=1000; integer-sided tile squares; gcd of tile sides is 1

**Scalar:** minimum number of squares in a primitive integer square dissection of the n×n square

**Direction:** minimize

**Human baseline:** {"value": "The maintained Mrs Perkins quilt compilation lists order 27 for square sizes 867–1116, including n=1000. This is a feasible human construction upper bound; the linked Wolfram Demonstration provides constructions.", "author": "Ed Pegg Jr, Richard K. Guy, Stuart Anderson, Geoff Morley and contributors (compiled results)", "year": "2010–2013 compilation; later updates", "source_note": "The squaring.net page links to the Pegg–Guy Wolfram Demonstration. A sequence entry is an upper bound unless an optimality proof is separately established."}

**Current record:** 27 squares is listed as the lowest known order for n=1000 in the maintained compilation; it is not marked or proved optimal.

**Open evidence:** The page explicitly states that most results past order 18 have not been proved best possible. Wynn’s exhaustive enumeration is only through order 18. Thus the 27-square n=1000 entry is a human construction, and no minimum claim is made. The former n=100, order-19 row was replaced: orders through 18 have maximum size 91, so an order-19 quilt at n=100 is optimal.

**Witness URL:** https://demonstrations.wolfram.com/MrsPerkinssQuilts/

**Primary sources:** ["https://squaring.net/quilts/mrs-perkins-quilts.html", "https://demonstrations.wolfram.com/MrsPerkinssQuilts/", "https://arxiv.org/abs/1308.5420"]

**Checks performed:** Opened maintained compilation and verified the order-27 list includes sizes 867–1116, hence n=1000. Read the explicit warning that most orders past 18 are unproved and the statement that Wynn exhaustively enumerated through order 18. Confirmed the page links Pegg and Guy’s Wolfram Demonstration. The demonstration app requires JavaScript; this audit did not independently retrieve or recompute the tile data.

**Status:** confirmed_suitable

**Remaining:** If the construction is needed for direct use, extract/download the linked Wolfram Demonstration data and verify tile areas, adjacency/coverage, side-length gcd and outer size. Do not label 27 optimal.

## T034

**Parameters:** No fixed polyomino selected; orientations allowed must be fixed per candidate; objective is minimum number of congruent copies that tile a rectangle

**Scalar:** minimum order (copy count) of a rectangle tiled by congruent copies of a fixed polyomino P

**Direction:** minimize

**Human baseline:** {"value": "The cited polyomino database and handbook document finite rectangle tilings for named shapes, but no specific shape, copy count, or open lower/upper gap was verified.", "author": "Klarner and later researchers", "year": "1960s onward"}

**Current record:** No configuration-specific order selected.

**Open evidence:** Klarner’s constant concerns asymptotic counting and does not establish the status of the minimum rectangle-tiling order for a specific shape. A finite tiling alone is only an upper bound.

**Witness URL:** https://polyominoes.org/data/5P

**Primary sources:** ["https://polyominoes.org/data/5P", "https://www.csun.edu/~ctoth/Handbook/chap14.pdf", "https://sicherman.net/mikereid/p5_rect.html"]

**Checks performed:** Located public shape and tiling references; no specific tiling or lower-bound proof was inspected.

**Status:** pending

**Remaining:** Choose one named polyomino, extract a rectangle tiling and count, and locate a source proving that this count is not minimal or that a strict interval remains.

## N003

**Parameters:** S² covering by 26 equal spherical caps (dimension 3)

**Scalar:** minimize maximum angular distance from any sphere point to its nearest selected center

**Direction:** minimize

**Human baseline:** {"value": "covering radius 25.8449223 degrees for 26 caps on S²", "author": "R. H. Hardin, N. J. A. Sloane, W. D. Smith", "year": "1994"}

**Current record:** Published listed covering radius 25.8449223° (from catalog); global optimum unproved.

**Open evidence:** Sloane covering library calls configuration putatively optimal and links coordinate file cover.3.26; no proof claim.

**Witness URL:** https://neilsloane.com/coverings/dim3/

**Primary sources:** ["https://neilsloane.com/coverings/index.html", "https://neilsloane.com/coverings/dim3/"]

**Checks performed:** Confirmed suitable; original maintained library identifies authors/year, “putatively optimal” status, and coordinates. Witness has not been retrieved or recomputed.

**Status:** confirmed_suitable

**Remaining:** Retrieve the linked construction, independently recompute its scalar and feasibility, and freeze the source/version.
