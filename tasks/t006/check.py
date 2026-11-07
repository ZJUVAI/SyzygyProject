"""Exact checks for simple connected regular graphs with configured girth."""
from collections import deque


def _integer(x):
    return type(x) is int


def _parse(solution, degree):
    if not isinstance(solution, dict):
        raise ValueError('solution must be an object')
    n = solution.get('vertices')
    edges = solution.get('edges')
    if not _integer(n) or n < 1:
        raise ValueError('vertices must be a positive integer')
    if not isinstance(edges, (list, tuple)):
        raise ValueError('edges must be a list')
    if len(edges) * 2 != degree*n:
        raise ValueError('edge count must match configured regular degree')
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
    if any(len(row) != degree for row in adj):
        raise ValueError(f'every vertex must have degree exactly {degree}')
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
    # Reuse the per-root state arrays. The previous implementation cleared
    # O(n) distance and parent arrays for each root, even though each bounded
    # BFS visits only a small part of a sparse high-girth graph.
    seen=[0]*n; dist=[0]*n; parent=[-1]*n
    for root in range(n):
        stamp=root+1; seen[root]=stamp; dist[root]=0; parent[root]=-1
        q=deque([root])
        while q:
            u=q.popleft()
            if dist[u] >= stop_at//2:
                continue
            for v in adj[u]:
                if seen[v] != stamp:
                    seen[v]=stamp; dist[v]=dist[u]+1; parent[v]=u; q.append(v)
                elif parent[u] != v and parent[v] != u:
                    length=dist[u]+dist[v]+1
                    if length < stop_at:
                        return length
                    if length == stop_at:
                        found_boundary_cycle=True
    return stop_at if found_boundary_cycle else None


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or not isinstance(config.get('parameters'), dict):
        raise ValueError('unsupported configuration')
    degree=config['parameters'].get('degree'); target_girth=config['parameters'].get('girth')
    if type(degree) is not int or degree < 2 or type(target_girth) is not int or target_girth < 3:
        raise ValueError('unsupported configuration')
    n,edges,adj=_parse(solution,degree)
    girth=_girth(adj,target_girth)
    if girth is not None and girth < target_girth:
        raise ValueError(f'girth must be at least {target_girth} (found {girth})')
    return {'objective':n,'verification_status':'exact','details':{
        'degree':degree,'girth':girth,'girth_lower_bound':target_girth,'vertices':n,'edges':len(edges),
        'connected':True,'claimed_objective_ignored':True,
        'optimality_proved':False}}
