# T101 fixed data provenance

`tai256c.dat` and `tai256c.sln` were downloaded from the versioned Debian source mirror for `r-cran-qap` 0.1-1-2:

- Matrix: <https://sources.debian.org/data/main/r/r-cran-qap/0.1-1-2/inst/qaplib/tai256c.dat>
- Witness: <https://sources.debian.org/data/main/r/r-cran-qap/0.1-1-2/inst/qaplib/tai256c.sln>
- Original benchmark page: <https://coral.ise.lehigh.edu/data-sets/qaplib/qaplib-problem-instances-and-solutions/>

SHA-256 values:

- `tai256c.dat`: `e7d72083d49f4768e5a15a02ee33fde038a794e7407e5e485c3c110f1509fafd`
- `tai256c.sln`: `066452382541a9139b2de34113105afbfaf14949a367fe5acef468d80556dcb0`

The matrix file has `n`, followed by the row-major entries of `A`, then `B`. The solution file has `n`, the archived score, then the one-based permutation. `human.py` converts the permutation to the task's zero-based convention. Exact recomputation yields 44,759,294, equal to the archived score.
