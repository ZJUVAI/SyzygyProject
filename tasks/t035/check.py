"""Exact checks for a simple connected 4-regular graph with girth at least 10."""
from collections import deque


def _integer(x):
    return type(x) is int


def _parse(solution):
    if not isinstance(solution, dict):
        raise ValueError('solution must be an object')
    n = solution.get('vertices')
    edges = solution.get('edges')
    if not _integer(n) or n < 1:
        raise ValueError('vertices must be a positive integer')
    if not isinstance(edges, (list, tuple)):
        raise ValueError('edges must be a list')
    if len(edges) != 2*n:
        raise ValueError('a 4-regular graph must have exactly 2*vertices edges')
    pairs=[]; seen=set()
    for edge in edges:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError('each edge must contain two endpoints')
        u,v=edge
        if not _integer(u) or not _integer(v):
            raise ValueError('edge endpoints must be integers; bool is rejected')
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError('edge endpoint out of range')
        if u == v:
            raise ValueError('self-loops are not allowed')
        e=(min(u,v),max(u,v))
        if e in seen:
            raise ValueError('duplicate edges are not allowed')
        seen.add(e); pairs.append(e)
    adj=[[] for _ in range(n)]
    for u,v in pairs:
        adj[u].append(v); adj[v].append(u)
    if any(len(row) != 4 for row in adj):
        raise ValueError('every vertex must have degree exactly 4')
    reached={0}; q=[0]
    for u in q:
        for v in adj[u]:
            if v not in reached:
                reached.add(v); q.append(v)
    if len(reached) != n:
        raise ValueError('graph must be connected')
    return n,pairs,adj


def _girth(adj, stop_at=10):
    """Certify no cycle shorter than stop_at and detect a stop_at-cycle."""
    n=len(adj); found_boundary_cycle=False
    for root in range(n):
        dist=[-1]*n; parent=[-1]*n; dist[root]=0; q=deque([root])
        while q:
            u=q.popleft()
            if dist[u] >= stop_at//2:
                continue
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v]=dist[u]+1; parent[v]=u; q.append(v)
                elif parent[u] != v and parent[v] != u:
                    length=dist[u]+dist[v]+1
                    if length < stop_at:
                        return length
                    if length == stop_at:
                        found_boundary_cycle=True
    return stop_at if found_boundary_cycle else None


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get('parameters') != {'degree':4,'girth':10}:
        raise ValueError('unsupported configuration')
    n,edges,adj=_parse(solution)
    girth=_girth(adj,10)
    if girth is not None and girth < 10:
        raise ValueError(f'girth must be at least 10 (found {girth})')
    claimed=solution.get('objective')
    mismatch=claimed is not None and (not _integer(claimed) or claimed != n)
    return {'objective':n,'verification_status':'exact','details':{
        'degree':4,'girth':girth,'girth_lower_bound':10,'vertices':n,'edges':len(edges),
        'connected':True,'claimed_objective_mismatch':mismatch,
        'optimality_proved':False}}
