"""Best reproduced fixed local-search witness; not a historical human record."""
import json
from pathlib import Path

def run_code():
    return json.loads((Path(__file__).parent/'data/search_reference.json').read_text())
