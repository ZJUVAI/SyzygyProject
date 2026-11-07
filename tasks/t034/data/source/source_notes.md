# Source and reconstruction notes

## Primary construction source

P. R. Herwig, M. J. H. Heule, P. M. van Lambalgen, and H. van Maaren, “A New Method to Construct Lower Bounds for Van der Waerden Numbers,” *Electronic Journal of Combinatorics* 14 (2007), R6. The official journal record is <https://www.combinatorics.org/ojs/index.php/eljc/article/view/v14i1r6>; it was published on 2007-01-03. Table 3 lists `W(2,7)`, prime 617, zero zippings, and the lower bound `>3703`. Sections 4.2 and 5 describe power-residue coloring and its conversion to a consecutive interval. The journal page and paper were checked online; a local PDF copy could not be saved in this implementation pass. The earlier author-hosted manuscript at <https://www.cs.utexas.edu/~marijn/publications/waerden.pdf> shows a 2005 pre-publication version of the same paper.

This is a reconstruction of the method and result reported by Herwig et al. Their paper says the power-residue technique is due to Rabung and cites his 1979 paper. We do not attribute the specific p=617 search run to Rabung personally.

For `p=617`, the 2-color power-residue classes are quadratic residues and nonresidues modulo p. On positions `i=0,...,6p`, assign color 0 to nonzero quadratic residues, color 1 to nonresidues, and assign the multiples `0,p,...,5p` color 0. Assign the final endpoint `6p` color 1. Translate positions to `[1,3703]` by adding one. The endpoint exception is required: if both endpoints had the same color, positions `0,p,...,6p` would be a monochromatic 7-term progression with step p.

## Later same-bound report

D. Monroe, “New lower bounds for van der Waerden numbers using distributed computing,” *JCMCC* 128 (2025), 305–315. Table 1 again lists `W(2,7)>3703`; Table 2 gives 617 as the method prime. The paper describes the construction as Rabung's discrete-log method and provides source code at <https://github.com/hmonroe/vdw>. It reports checking primes up to 950 million and does not report a higher 2-color, length-7 bound. Repository commit pin was not available during implementation; the paper is the fixed literature record used here.

## Newer result check

Campos, Fox, and Schildkraut, “A new lower bound for two-color van der Waerden numbers,” arXiv:2608.20824 (2026), proves a general asymptotic lower bound and describes AI use. It does not report an explicit same-parameter `k=7` coloring with length greater than 3703. This check is not a full literature survey.
