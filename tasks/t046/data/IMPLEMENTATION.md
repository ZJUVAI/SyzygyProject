# T046 implementation notes

## Configuration and evidence

T046-C01 is the only maintained configuration: binary linear `[68,15]`. The public Grassl BKLC entry reports a construction distance of 24 and an upper bound of 26. The saved Magma BKLC database witness is independently verified by rank and exact enumeration. This is a best-known construction, not a proof of optimality.

The frozen human-method baseline is a direct sum of three public first-order Reed–Muller `[16,5,8]` codes, followed by 20 zero coordinates. Its exact distance is 8. The local traditional search uses systematic matrices and exact scoring. Its saved result has distance 19. The evolutionary entry uses the C01 spectrum search and does not read a comparison witness.

## Run settings

Generation is limited to 300 seconds. Exact verification is limited to 60 seconds. Memory is 4 GiB and the thread count is one. Replay the public witness with:

```sh
MATHBENCH_CONFIG_ID=T046-C01 .venv/bin/python -m mathbench evaluate T046 tasks/t046/sota.py --strict --config T046-C01
```
