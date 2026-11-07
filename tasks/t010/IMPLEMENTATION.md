# T010 implementation notes

## Configurations and source evidence

C01 `(17,6)` remains unchanged and accepted. C02 `(23,10)` and C03 `(25,10)` have passed Sol review. The primary source is Ota, Osa, and Harada, [arXiv:2610.11609](https://arxiv.org/abs/2610.11609), which publishes complete lists for `(22,84,9)` and `(24,196,9)` and an exhaustive checker. The source files are retained in `data/source_22_84_9.txt` and `data/source_24_196_9.txt`. Their SHA-256 values and fixed ancillary URLs are in `sota.json`.

The paper states `A₂(n,d)=A₂(n+1,d+1)` for odd `d`. Appending an overall parity bit to each source word therefore gives C02's `(23,84,10)` and C03's `(25,196,10)` witness. The fixed witnesses are `data/parity_extended_23_84_10.json` and `data/parity_extended_25_196_10.json`. The Brouwer table gives upper bounds 150 and 466, so neither configuration has a proof of optimality. The paper does not disclose AI assistance; the archive leaves that provenance unclassified.

## Traditional construction

The classical baseline uses the primitive narrow-sense binary BCH `[31,11,≥11]` code with generator polynomial `x^20+x^18+x^17+x^13+x^10+x^9+x^7+x^6+x^4+x^2+1`. The generator matrix has rank 11 on the first 11 coordinate columns. The method sets the first seven or five coordinates to zero, which leaves 16 or 64 words, then punctures the next coordinate. This gives lengths 23 and 25. The minimum distance guarantee is at least 10 after puncturing; exact checks find distance 10 for both witnesses. `human.py` reconstructs the code from the polynomial and coordinate operations.

## Programs and verification

All programs dispatch on `MATHBENCH_CONFIG_ID`. The cold seed for C02/C03 is the singleton zero word and reads no reference file. `baseline.py` performs seeded add-only greedy trials from the BCH construction. `human.py` regenerates the BCH witness. `sota.py` and `reference.py` return the saved parity-extended public witness. `evolution.py` uses the bounded add-only search for C02/C03; the compiled C01 kernel remains specific to C01.

The checker validates word ranges, duplicates, and all pairwise distances with integer XOR and population counts. It returns the number of codewords as the objective and ignores any claimed objective in the input. C02 checks 3,486 pairs in the public witness; C03 checks 19,110. Generation is limited to 300 seconds; verification is limited to 60 seconds, with 4 GiB memory and one thread.
