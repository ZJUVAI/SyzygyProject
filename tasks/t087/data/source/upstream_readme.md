# A certified lower bound for the minimum-autocorrelation constant

**Kevin Russell** — *ProjectForty2 / CHRONOS agent*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21227361.svg)](https://doi.org/10.5281/zenodo.21227361)

This repository contains a short computer-assisted note and its full
verification package: an exact-arithmetic **lower bound** for the
minimum-autocorrelation constant of Barnard and Steinerberger (Problem 6.6 of
the AlphaEvolve suite). For a nonnegative `f` in `L¹(ℝ)` with autocorrelation
`a_f(t) = ∫ f(x) f(x+t) dx`, the constant is

> ```
> C = sup_{ f >= 0 }  ( min_{ t in [0,1] } a_f(t) ) / ||f||_1^2 .
> ```

The published bounds are `0.37 < C <= 0.411` (Barnard–Steinerberger 2020),
unimproved since. The headline result here:

> **Theorem.**
> ```
> C >= 2378625 / 5958277 = 0.39921356...
> ```

This is the first improvement of the lower bound since 2020 and, to our
knowledge, the first exact-arithmetic certificate for this constant. The
witness is a nonnegative **step function** — exactly the bounded-step-function
search the AlphaEvolve authors proposed for this problem but did not carry out
(their arbitrary-function search reward-hacked its own numerical integrator and
was discarded).

## Why it is exact

For a step function `f = Σ hᵢ·1_[i·d,(i+1)·d)` the autocorrelation `a_f` is
piecewise linear with breakpoints only at multiples of `d`, so its minimum over
the continuous interval `[0,1]` is attained at a grid node or the endpoint
`t=1` and equals a minimum of finitely many **exact rationals**. With rational
heights `hᵢ` and rational `d`, the norm `||f||_1`, every node value
`a_f(k·d) = d·Σ hᵢ hᵢ₊ₖ`, the interpolated endpoint value, their minimum, and
the final ratio are all exact rationals. No floating point enters the certified
path.

## What this does *not* claim

Honest scoping is the point of the note:

- **A lower bound, not closure.** This is a one-sided bound. It does **not**
  determine `C`, and it does **not** touch the proven upper bound `0.411`.
- **The upper bound is a convex wall.** We record (Section 4) that `0.411` is
  *exactly* the optimum of the natural convex (Fourier/Bochner) relaxation —
  solving that relaxation returns `0.41077` with **zero gap** to
  Barnard–Steinerberger. Improving the upper bound requires the nonconvex
  "autocorrelation-of-a-nonnegative-function" constraint that Madrid–Ramos
  (2020) could only handle non-constructively; our construction-certification
  method has no purchase on it.
- **No new technique, no optimality.** The construction is a finer, certified
  instance of a known search space. We do not claim the witness is optimal, and
  we do not prove the true extremizer is asymmetric — only that our best
  construction is, and that symmetrizing it strictly lowers the ratio (to
  `0.2281`), and that the step-function family appears to plateau near `0.40`.
- **Everything else is measurement**, labeled as such. Only the boxed
  inequality is certified.

## Reproduce / verify it

Verification uses **only the Python standard library** (`fractions`, `json`) —
no third-party packages, no floating point on the certified path. Requires
**Python ≥ 3.10**.

```bash
make verify        # recompute the bound from the certificate, exactly
```

`make verify` runs `scripts/verify_bound.py`, which reads the exact rational
heights from `certs/certificate_n480.json`, recomputes `||f||_1`, every node
autocorrelation, the endpoint value at `t=1`, their minimum over `[0,1]`, and
the final ratio **from scratch** in exact arithmetic (by an implementation
independent of the optimizer that produced the construction), and confirms:

```
[OK]  recomputed exact ratio == pinned certificate ratio
[OK]  exact ratio >= displayed 0.39921356 (valid rounded-down lower bound)
[OK]  exact ratio exceeds published 0.37 by 0.029214
[OK]  exact ratio < proven upper bound 0.411
LOWER BOUND VERIFIED:  C6.6 >= 2378625/5958277 = 0.39921356...
```

Any mismatch exits nonzero and `make verify` fails loudly.

## Build the PDF

The prebuilt `c66_autocorrelation_bound.pdf` is included. To rebuild with
[tectonic](https://tectonic-typesetting.github.io/):

```bash
tectonic c66_autocorrelation_bound.tex
```

## Attribution

Credit belongs where the mathematics originated.

- The constant, **both published bounds**, and the near-extremal
  **modified-arcsine construction** are due to **R. C. Barnard and
  S. Steinerberger**, *Three convolution inequalities on the real line with
  connections to additive combinatorics*, J. Number Theory **207** (2020)
  42–55, [arXiv:1903.08731](https://arxiv.org/abs/1903.08731).
- The framing as Problem 6.6 and the note that a bounded-step-function search
  was the authors' intended-but-unfinished retry are from **B. Georgiev,
  J. Gómez-Serrano, T. Tao, A. Z. Wagner**, *Mathematical exploration and
  discovery at scale*, [arXiv:2511.02864](https://arxiv.org/abs/2511.02864).
- The strict-but-non-constructive `C < 0.411` result is **J. Madrid and
  A. Ramos**, *On optimal autocorrelation inequalities on the real line*,
  CPAA **19** (2020), [arXiv:2003.06962](https://arxiv.org/abs/2003.06962).
- **Method lineage:** the exact-certificate recipe (rational reconstruction,
  independent recomputation, directed rounding of any displayed decimal, no
  unenclosed float on the certified path) follows earlier notes by the author —
  on the Erdős minimum-overlap constant
  ([10.5281/zenodo.21194860](https://doi.org/10.5281/zenodo.21194860)),
  on three autoconvolution inequalities
  ([10.5281/zenodo.21194862](https://doi.org/10.5281/zenodo.21194862)),
  and on Mertens-type extremal ceilings
  ([10.5281/zenodo.21221207](https://doi.org/10.5281/zenodo.21221207)).

This note was prepared computer-assisted with **CHRONOS**, ProjectForty2's
autonomous research agent, under the author's direction; the author reviewed the
mathematics and takes responsibility for all claims.

## Layout

```
.
├── c66_autocorrelation_bound.tex   the note (source of truth)
├── c66_autocorrelation_bound.pdf   prebuilt PDF
├── Makefile                        `make verify`
├── requirements.txt                standard library only (certified path)
├── LICENSE                         MIT (code) + CC BY 4.0 (note text)
├── scripts/
│   ├── verify_bound.py             VERIFY: independent exact recomputation (stdlib only)
│   └── c66_certify.py              the original certifier (produced the certificate)
├── certs/
│   └── certificate_n480.json       exact rational heights, d, min_g, L1, ratio
└── data/
    └── construction_n480.npz       optimizer output (provenance; not needed to verify)
```

## Cite this work / permanent archive

This bundle is deposited on Zenodo as a citable archive:

- **Concept DOI** (cites *all* versions):
  [10.5281/zenodo.21227361](https://doi.org/10.5281/zenodo.21227361)
- **This-version DOI** (release `v1.0`):
  [10.5281/zenodo.21227362](https://doi.org/10.5281/zenodo.21227362)
- **Development history:**
  [github.com/techno-optimist/minimum-autocorrelation-bound](https://github.com/techno-optimist/minimum-autocorrelation-bound)

## License

Code and certificate data are released under the MIT License (see `LICENSE`).
The note text (`c66_autocorrelation_bound.tex/.pdf`) is © 2026 Kevin Russell,
released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
