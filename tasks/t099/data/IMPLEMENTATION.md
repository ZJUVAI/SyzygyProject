# T099 implementation and acceptance notes

## Configuration and objective

T099-C01 fixes 17 wires. The objective is to minimize comparator count. The checker uses Python integer bitsets to exhaustively verify all `2^17` binary inputs. The zero-one principle then certifies sorting for every totally ordered input domain. This verifies feasibility, not minimum size.

## Public sources and bounds

The source is [Dobbelaere's sorting-network table](https://bertdobbelaere.github.io/sorting_networks.html). The pinned witness is `data/reference/sorterhunter_17_71_12.json`. The pinned table snapshot has SHA-256 `fb08a5cd90a460607586be0f753fa19baedc1e5fe1c7d4247efc1923e6dfd0f6`; the source revision is SorterHunter commit `8ba90df607cbdc339409e0b173b5a2ffd60fc911`.

The table lists a 71-comparator, 12-layer feasible network and size bounds 63 to 71. The 63 lower bound is an unpublished, unrefereed strengthening. The strongest lower bound derived from published work in the source review is 60. The source identifies the network as SorterHunter-generated but does not report AI use. Its origin is classified as automated search with AI status unknown.

## Human baseline and programs

The human baseline reconstructs Batcher's odd-even mergesort padded to 32 wires, then omits sentinel-wire comparisons. It yields 85 comparators and passes exact zero-one verification. The initial network uses odd-even transposition sorting on 17 wires and yields 136 comparators. The baseline and evolution programs start from that initial network and do not read `human.py`, `reference.py`, or `data/reference`. Only the designated reference program loads the pinned comparison witness.

The task contract sets a 300-second generation limit, a separate 60-second verification limit, 4 GiB of memory, and one thread.

## Test coverage

Tests verify the C01 public and human witnesses, all 131,072 binary inputs with an independent scalar replay, and the pinned table snapshot hash. They check malformed and invalid networks, forged score fields, configuration mismatch, unsupported removed configuration IDs, all five program entry points, and worker error and timeout handling.

## Paper

- [Using Symmetry and Evolutionary Search to Minimize Sorting Networks](https://www.jmlr.org/papers/v14/valsalam13a.html)
