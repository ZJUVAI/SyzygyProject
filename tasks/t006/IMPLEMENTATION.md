# T006 implementation notes

## Configurations

- `T006-C01` fixes degree 4 and girth at least 10. The initial program builds the LPS `X^(5,37)` graph and removes two generator matchings. It does not load a saved witness.
- `T006-C02` fixes degree 4 and girth at least 9. It uses the same LPS construction as a valid cold start because girth at least 10 implies girth at least 9. It does not import or call the checker.
- The human and public reference for C02 is the 270-vertex graph6 witness at [House of Graphs](https://houseofgraphs.org/data/cages/k4_g9_n270.g6). The downloaded file SHA-256 is `b2f7ef96469f839a093f42352a419435a0655a068cd345732d42b48899406e8d`. The converted task witness SHA-256 is `2a28776e32b0da75e771d76ae3343bb214fa41af355452e21fa1a8eb17544f14`.

## Published bounds for C02

Exoo, Goedgebeur, Jooken, Stubbe, and Van den Eede report `n(4,9) <= 270` in *New Small Regular Graphs of Given Girth: the Cage Problem and Beyond*, Electronic Journal of Combinatorics 33(3), #P3.48 (2026), [DOI 10.37236/14834](https://doi.org/10.37236/14834). Their result is a construction and does not prove that 270 is optimal.

The Moore bound is 161, from `1 + 4(1 + 3 + 9 + 27)`. De la Cruz and Pizaña report the stronger computational lower bound `n(4,9) >= 165` in *On Cages and Choosing with Symmetries*, Electronic Journal of Combinatorics 33(1), #P1.54 (2026), [DOI 10.37236/14471](https://doi.org/10.37236/14471). This lower bound does not establish optimality at 270.

The authors' `smallRegGirthGraphs` repository was inspected at commit `c2a1a4e334cd9f4dd31247f1ebfb6e18c004e4bc`. That snapshot does not contain the 270-vertex `(4,9)` witness, so the witness is attributed to House of Graphs, not to that repository.

## Validation and status

The checker reads degree and girth from the selected configuration and computes the vertex count from the graph. It ignores any candidate-declared objective. Unit tests compare the complete checker output when the objective is omitted and when a forged objective is supplied. The C02 record, source, and construction passed Sol review on 2026-11-07; the benchmark registry does not expose pending configurations to the official runner.
