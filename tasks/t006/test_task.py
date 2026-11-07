import json
from pathlib import Path
import pytest

TASK_DIR=Path(__file__).parent
from tasks.t006 import check

CONFIG={'parameters':{'degree':4,'girth':10}}
DATA=json.loads((TASK_DIR/'data'/'human_graph.json').read_text())


def test_published_graph_and_independent_score():
    result=check.validate(DATA,CONFIG)
    assert result['objective']==320
    assert result['verification_status']=='exact'
    assert result['details']['edges']==640
    assert result['details']['girth']==10


def test_claimed_objective_is_not_used():
    ordinary=check.validate(DATA,CONFIG)
    altered=check.validate(dict(DATA,objective=1),CONFIG)
    assert altered==ordinary
    assert altered['objective']==320
    assert altered['details']['claimed_objective_ignored']


def test_duplicate_edge_rejected():
    edges=list(DATA['edges']); edges[-1]=edges[0]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_loop_rejected():
    edges=list(DATA['edges']); edges[0]=[0,0]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_boolean_endpoint_rejected():
    edges=list(DATA['edges']); edges[0]=[0,True]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_out_of_range_endpoint_rejected():
    edges=list(DATA['edges']); edges[0]=[0,320]
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':edges},CONFIG)


def test_short_cycle_rejected_after_degree_preserving_switch():
    edges={tuple(e) for e in DATA['edges']}
    edges.remove((0,2)); edges.remove((272,308))
    edges.add((0,308)); edges.add((2,272))
    with pytest.raises(ValueError): check.validate({'vertices':320,'edges':[list(e) for e in edges]},CONFIG)


def test_non_integer_order_rejected():
    with pytest.raises(ValueError): check.validate({'vertices':True,'edges':[]},CONFIG)


def _cycle_adjacency(length, offset=0):
    adj=[[] for _ in range(offset+length)]
    for i in range(length):
        u=offset+i; v=offset+(i+1)%length
        adj[u].append(v); adj[v].append(u)
    return adj


@pytest.mark.parametrize('length',range(3,12))
def test_bounded_girth_reports_known_cycle_lengths(length):
    # Below the bound, report the shortest cycle. At the bound, report 10;
    # above it, None means the bounded check found no cycle of length <= 10.
    expected=length if length < 10 else 10 if length == 10 else None
    assert check._girth(_cycle_adjacency(length),10)==expected


def test_bounded_girth_checks_disconnected_components():
    short=_cycle_adjacency(7)
    long=_cycle_adjacency(11,offset=7)
    combined=[row[:] for row in short]+[row[:] for row in long[7:]]
    assert check._girth(combined,10)==7


CONFIG_C02={'parameters':{'degree':4,'girth':9}}
DATA_C02=json.loads((TASK_DIR/'data'/'human_graph_c02.json').read_text())

def test_c02_published_graph_and_independent_score():
    result=check.validate(DATA_C02,CONFIG_C02)
    assert result['objective']==270
    assert result['details']['degree']==4
    assert result['details']['girth_lower_bound']==9
    assert result['details']['edges']==540

def test_c02_forged_claim_does_not_change_any_validation_output():
    ordinary=check.validate(DATA_C02,CONFIG_C02)
    forged=check.validate(dict(DATA_C02,objective=-999999),CONFIG_C02)
    assert forged==ordinary
    assert forged['objective']==270
    assert forged['details']['claimed_objective_ignored']

def test_c02_lps_seed_is_valid_without_reading_witness():
    from tasks.t006.lps import build_graph
    result=check.validate(build_graph((0,2)),CONFIG_C02)
    assert result['details']['girth_lower_bound']==9

def test_configured_degree_and_girth_are_enforced():
    with pytest.raises(ValueError): check.validate(DATA_C02,CONFIG)
