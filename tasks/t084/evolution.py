"""Thirty-two-step heterogeneous coordinate search for T084."""
try:
    from .search import search
except ImportError:
    from search import search

def run_code():
    return search(32)
