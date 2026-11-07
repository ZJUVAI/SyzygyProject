# T048 implementation and acceptance notes

## Configurations and objective

- C01 fixes 17 wires. Its existing H=85, public 71-comparator reference, result, and Sol acceptance are preserved.
- C02 fixes 18 wires. Human H=90; public SorterHunter witness has 77 comparators, 12 layers.
- C03 fixes 19 wires. Human H=98; public SorterHunter witness has 85 comparators, 12 layers.

The scalar objective is comparator count to minimize. The checker exhaustively verifies `2^n` binary inputs with Python integer bitsets. By the zero-one principle this certifies sorting for all totally ordered inputs. It does not prove that a network has minimum size.

## Public sources and bounds

The current source is [Dobbelaere's sorting-network table](https://bertdobbelaere.github.io/sorting_networks.html), checked 2026-11-07. Its live rows and the pinned local HTML snapshot agree on the selected networks:

| Inputs | Public size | Depth | Size lower bound | Size gap |
| ---: | ---: | ---: | ---: | --- |
| 17 | 71 | 12 | 63 | open |
| 18 | 77 | 12 | 68 | open |
| 19 | 85 | 12 | 73 | open |

The 17-input 63 lower bound is noted as an unrefereed tightening in the source review; 60 is the strongest bound derived from published work. For 18 and 19, bounds are those stated in the live table. Depth lower bounds 10–11 are recorded separately and are not used as size proofs. The source labels its networks as SorterHunter-generated but does not report AI use. Origin classification is therefore automated-network source, AI status unknown.

Pinned comparator lists are `data/reference/sorterhunter_{17,18,19}_*.json`. The pinned table snapshot SHA-256 is `fb08a5cd90a460607586be0f753fa19baedc1e5fe1c7d4247efc1923e6dfd0f6`; source revision is SorterHunter commit `8ba90df607cbdc339409e0b173b5a2ffd60fc911`.

## Human baseline and programs

The human baseline reconstructs Batcher's odd-even mergesort on 32 wires and omits comparators involving padded sentinel wires. It yields 85, 90, and 98 comparators for 17, 18, and 19 inputs. All are fully zero-one verified. Initial networks use odd-even transposition sorting and are generated from the public input count only. Baseline and evolution mutate that cold start and do not read `human.py`, `reference.py`, or reference data. Reference files load only in the designated comparison program.

All five programs select by `MATHBENCH_CONFIG_ID`. New configurations are marked accepted by Sol on 2026-11-07. The task contract uses 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread.

## Test coverage

Tests exhaustively verify the C01 public and human witnesses, and each C02/C03 human and public network. Tests check comparator counts, depth metadata, invalid wire pairs, malformed and empty networks, forged score fields, configuration mismatch, and all five program entry points. An independent scalar replay of all `2^17` C01 inputs and the pinned source/PDF hashes remain in place.
