# T006 implementation notes

## Official configuration

`T006-C01` fixes degree 4 and girth at least 10. The starter builds the LPS `X^(5,37)` graph and removes two generator matchings. It does not load a saved witness. The deterministic initial graph has 50,616 vertices and is checked by the independent task evaluator.

The human baseline is the 320-vertex graph reported by Exoo, Goedgebeur, Jooken, Stubbe, and Van den Eede. Their paper gives an upper bound. It does not prove that the minimum order `n(4,10)` is 320. The task-local edge list was converted from `genLifts/data/graphs/cage/n320_k4_g10.g6` in the authors' public repository. The exact graph is independently checked by the task evaluator.

Sources: [paper v2](https://arxiv.org/abs/2511.07247v2), [authors' data repository](https://github.com/AGT-Kulak/smallRegGirthGraphs), [LPS paper](https://doi.org/10.1007/BF02126799).
