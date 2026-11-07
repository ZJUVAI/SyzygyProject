"""Replay Nunn-Coxson's published witness for the selected T054 config."""
import json
from pathlib import Path
from tasks.t054.check import config_id, config_length

def run_code():
    cid=config_id(); length=config_length(cid); idx=int(cid[-1:])
    path=Path(__file__).with_name("data") / "reference" / f"nunn_coxson_length{length}.json"
    record=json.loads(path.read_text(encoding="utf-8")); bits=bin(int(record["hex_code"],16))[2:].zfill(length)
    if len(bits)!=length: raise ValueError("source code length mismatch")
    return {"sequence":[1 if bit=="1" else -1 for bit in bits]}
