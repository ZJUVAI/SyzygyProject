"""Skutella human construction, padded to the fixed m=15 configuration."""
def run_code():
    base = [(3,3),(6,4),(4,4),(4,6),(3,3),(4,6),(1,3),(4,6)]
    return {"pairs": [[str(u)+"/10", str(v)+"/10"] for u,v in base] + [[0,0] for _ in range(7)]}
