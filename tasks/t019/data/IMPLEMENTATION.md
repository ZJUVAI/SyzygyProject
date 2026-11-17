# T019 implementation and review evidence

## Configuration and objective

The official configuration is T019-C01 with `k=343`. The objective is to minimize the diameter `max(tuple)-min(tuple)`. A tuple is admissible when it has 343 distinct integers and misses at least one residue class modulo every prime `p <= 343`. A prime `p > 343` has more residue classes than the tuple has entries, so it cannot cover every class.

The checker recomputes admissibility and the exact integer diameter. It ignores candidate-supplied objective fields. It rejects any configuration ID or `k` value that does not match T019-C01.

## Human and public reference

Thomas Engelsma's published tuple has diameter 2340. The local witness in `data/human_343.json` matches the tuple in the [MIT Prime Gaps artifact](https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt). The [MathBases narrow admissible tuples page](https://mathbases.org/d/narrow-admissible-tuples) lists the database scope and record status. The k=343 row has no optimality marker. This evidence does not prove optimality.

The task's source review and exact replay are recorded in `data/sota.json` and `data/records.json`. The checker independently confirms all 68 primes through 343 and the exact diameter.

## Initial program and search

The initial program returns 343 consecutive multiples of the product of all primes through 343. Every entry is zero modulo each checked prime. This gives a valid seed with diameter `342` times that product.

The traditional baseline starts with a greedy admissible tuple and makes bounded randomized replacements. The evolution program uses interval residue masks and exact final validation. Both programs use the configured random seed. A warm-start file is read only from an explicit runner-provided path. The standard limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread.

The saved best construction and its replay record are in `data/best/`. The prior Sol review applies to the reviewed implementation and recorded run. This cleanup removes nonofficial configurations. Sol must review the resulting implementation before it receives a current acceptance status.
