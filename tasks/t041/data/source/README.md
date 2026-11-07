# Frozen source assets

The public construction assets are from `Sprite143/erdos-106-counterexample`
at commit `edbfb534e78d4f1f9b1a5a7298b9b022285b4962`. The upstream archive is
`repository.tar.gz` (SHA-256
`52d3dfb518072b709e8abfa4d609a8a5f97f5a3bd33c3431721480ff69317173`). The
closed-form constructor is `public_construct.py` (SHA-256
`fecd1d59a3989d97a402ab662fca966b60aa8faff3e9fbd8d58a58e0524cd7aa`). The
original numerical search certificate is separate and reports
`2000062156200269/500000000000000`. It is not the score of the later
closed-form construction.

The upstream repository is MIT licensed. `LICENSE` is retained with the copied
constructor. `deepmind_2511.02864v1.pdf` is the source checked for AlphaEvolve
§6.35. `original_grid17_human_asset.json` is the exact downloaded human-method
asset from the research archive; `data/human_grid_witness.json` is the task's
converted, independently checked witness.

The task-local checker does not import the upstream checker. It rebuilds the
closed-form witness, then uses exact rational corner containment and its own
separating-axis tests over all 136 square pairs.
