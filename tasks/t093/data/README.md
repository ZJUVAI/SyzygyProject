# T093 fixed data provenance

The matrix bytes are stored as deterministic gzip in `tai256c.dat.gz` (zero timestamp, no embedded filename). Decompression gives the exact `tai256c.dat` bytes downloaded from the versioned Debian source mirror for `r-cran-qap` 0.1-1-2. The solution is stored as `tai256c.sln`:

- Matrix: <https://sources.debian.org/data/main/r/r-cran-qap/0.1-1-2/inst/qaplib/tai256c.dat>
- Witness: <https://sources.debian.org/data/main/r/r-cran-qap/0.1-1-2/inst/qaplib/tai256c.sln>
- Original benchmark page: <https://coral.ise.lehigh.edu/data-sets/qaplib/qaplib-problem-instances-and-solutions/>

SHA-256 values:

- decompressed `tai256c.dat`: `e7d72083d49f4768e5a15a02ee33fde038a794e7407e5e485c3c110f1509fafd`
- `tai256c.sln`: `066452382541a9139b2de34113105afbfaf14949a367fe5acef468d80556dcb0`

The matrix file has `n`, followed by the row-major entries of `A`, then `B`. The solution file has `n`, the archived score, then the one-based permutation. `human.py` converts the permutation to the task's zero-based convention. Exact recomputation yields 44,759,294, equal to the archived score.
