"""Deterministic valid rational starting program for the selected configuration."""
def run_code():
    n = 11
    return {"points": [[f"{i}/{n-1}", f"{i*i}/{(n-1)**2}"] for i in range(n)]}
