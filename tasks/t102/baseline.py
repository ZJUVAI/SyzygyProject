"""Sixteen-step traditional rational coordinate search for T102."""
try:
    from .search import search
except ImportError:
    from search import search

def run_code():
    return search(16)
