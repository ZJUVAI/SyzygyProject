"""Exact validator for binary linear [68,15] codes."""
import itertools

N, K = 68, 15

def _rank(rows):
    rows = [sum(int(x) << j for j, x in enumerate(row)) for row in rows]
    rank = 0
    for col in range(N):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
        if rank == len(rows):
            break
    return rank

def _matrix(solution):
    if not isinstance(solution, dict) or 'generator_matrix' not in solution:
        raise ValueError('solution must contain generator_matrix')
    m = solution['generator_matrix']
    if not isinstance(m, (list, tuple)) or len(m) != K:
        raise ValueError('generator_matrix must have 15 rows')
    out=[]
    for row in m:
        if not isinstance(row, (list, tuple)) or len(row) != N:
            raise ValueError('each generator row must have 68 entries')
        r=[]
        for x in row:
            if type(x) is not int or x not in (0,1):
                raise ValueError('matrix entries must be integer 0 or 1 (bool is rejected)')
            r.append(x)
        out.append(r)
    if _rank(out) != K:
        raise ValueError('generator matrix must have rank 15 over GF(2)')
    return out

def _min_distance(rows):
    packed=[sum(x << j for j,x in enumerate(row)) for row in rows]
    word=0
    previous_gray=0
    best=N+1
    for i in range(1, 1 << K):
        gray=i ^ (i >> 1)
        changed=gray ^ previous_gray
        word ^= packed[changed.bit_length()-1]
        weight=bin(word).count("1")
        if weight < best:
            best=weight
        previous_gray=gray
    return best

def validate(solution, config, strict=False):
    params=config.get('parameters', {})
    if params != {'n':68,'k':15,'q':2}:
        raise ValueError('unsupported configuration')
    rows=_matrix(solution)
    d=_min_distance(rows)
    claimed=solution.get('objective')
    if claimed is not None and (type(claimed) is not int or claimed != d):
        # Claimed values are ignored as evidence; mismatches are reported in details.
        claimed_mismatch=True
    else:
        claimed_mismatch=False
    return {'objective':d,'verification_status':'exact','details':{'rank':K,'codewords_checked':(1<<K)-1,'claimed_objective_mismatch':claimed_mismatch}}
