# T085 implementation record

Status: **accepted by Sol on 2026-11-06**.

## Source and open status

The fixed configuration is 21 unit disks covering a disk centered at the origin. Friedman's *Circles Covering Circles* table was checked on 2026-11-06: it reports `r=3.804+` for n=21, credits Jeremy Tan in 2018, and labels the result found. The page shows proofs for n=11 through n=20 in 2026, but n=21 remains marked found. The n=21 table image is saved at `data/source/friedman_tan21.png`. No exact witness for the 3.804 report was recovered, so this value is reported as unverified.

Kershner's 1939 paper, “The Number of Circles Covering a Set,” American Journal of Mathematics 61(3), 665–671, DOI 10.2307/2371320, is the primary source for the classical triangular-lattice covering method. The human baseline is a local finite patch based on that method: the 19 lattice sites with hexagonal index radius 2, at rational spacing slightly below the infinite-plane covering spacing, plus two repeated origin centers. The checker proves this patch covers radius 7/2. The exact finite patch is not attributed to Kershner as a published n=21 result.

## Mathematical model and exact certificate

The input has 21 arbitrary rational centers and a positive rational target radius. There is no coordinate or denominator cap. This domain has the same supremum as the real-coordinate problem: contract every center and the target disk about the origin by a rational factor below 1. Unit covering disks do not shrink, which creates positive coverage slack. Approximate the contracted centers by rational points and choose a rational target radius approaching the contracted radius.

Let `f(p)=min_i |p-c_i|^2`. The disk is covered exactly when `f(p)<=1` everywhere. On each Voronoi region, `f` is squared distance to one center. Its maximum over the region clipped by the target disk occurs at a region vertex or at an extremum on a circular boundary arc. The checker enumerates all triple-center Voronoi vertices inside the target disk; all pair-bisector intersections with its boundary; radial extrema for each center on the boundary; and four fixed boundary points for the constant-distance case when a center is at the origin. This set includes every possible maximum. It may include extra non-Voronoi points, which are safe to check.

Triple and pair critical points have rational coordinates or coordinates in a quadratic extension. For an algebraic boundary point `p=p0+v*sqrt(d)`, each coverage inequality reduces to the sign of `a+b*sqrt(d)` for rational `a,b,d`. The checker resolves the sign with integer/rational arithmetic and checks every center. It uses no sampling, floats, coordinate caps, or claimed scores.

## Programs and isolation

`init_program.py` is standalone and returns 21 coincident unit disks, which exactly cover radius 1. `baseline.py` and `evolution.py` start from that seed and make seeded integer-center mutations. They use only exact feasibility checks and do not read `human.py`, `reference.py`, or comparison files. `human.py` reconstructs the finite triangular-lattice patch from its formula. `reference.py` reads the frozen file under `data/reference/`.

Search defaults are 12 and 20 fixed mutations with seed from `MATHBENCH_SEED`. They alternate radius-1 layout mutations with radius-3/2 expansion attempts. The saved evolution replay used seed 0: 20 attempts, 10 radius expansions and 10 feasible radius-1 layouts, with no radius improvement. `MATHBENCH_SEARCH_SECONDS` enables a machine-dependent cutoff. Each program reports tested and feasible candidate counts.

## Validation commands

Run `.venv/bin/python -m pytest tasks/t085 -q`. Result: **29 passed**. Tests cover the human and fixed witnesses, coincident-center boundary case, all five `run_code()` entries, malformed and non-finite input, exact full-domain coverage failure, duplicate centers, score invariance, large rational strings, cold initialization, search isolation, runner error/timeout paths, and evaluator use with a temporary registry patch.

The source image and witness provenance are saved in task-local `data/`. This directory is awaiting Sol's independent mathematical review and runner replay.
