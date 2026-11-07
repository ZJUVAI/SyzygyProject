"""Deterministic axis-aligned grid seed selected by MATHBENCH_CONFIG_ID."""
import json, os
# EVOLVE-BLOCK-START

def run_code():
    cid = os.environ.get('MATHBENCH_CONFIG_ID', 'T002-C01')
    n = {'T002-C01': 26, 'T002-C02': 29, 'T002-C03': 38}.get(cid)
    if n is None:
        raise ValueError('unknown T002 configuration')
    if n==26:
        return {'squares':[{'x':str(2*(i%5)+1)+'/2','y':str(2*(i//5)+1)+'/2','t':'0'} for i in range(26)]}
    width=6 if n==29 else 7
    return {'squares':[{'x':str(2*(i%width)+1)+'/2','y':str(2*(i//width)+1)+'/2','t':'0'} for i in range(n)]}

# EVOLVE-BLOCK-END
if __name__ == '__main__': print(json.dumps(run_code()))
