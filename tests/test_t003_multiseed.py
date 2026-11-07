"""Require equal budgets and exact arithmetic for paired search comparisons."""
import json
import pytest
from scripts.run_t003_multiseed import compare_runs


def batch():
    summary = {'all_runs_passed': True,
               'runs': [{'seed': 0, 'objective': '5/2'}],
               'best_objective': '5/2', 'mean_objective': 2.5,
               'total_generation_seconds': 1.0}
    manifest = {'seeds': [0], 'generations_per_seed': 1000, 'population': 12,
                'generation_limit_seconds_per_seed': 300, 'verification_limit_seconds': 60,
                'threads_per_run': 1, 'memory_bytes_per_run': 4*1024**3}
    return summary, manifest


def test_paired_comparison_keeps_exact_small_improvements(tmp_path):
    previous, manifest = batch()
    (tmp_path/'summary.json').write_text(json.dumps(previous))
    (tmp_path/'manifest.json').write_text(json.dumps(manifest))
    current, _ = batch()
    current['best_objective'] = current['runs'][0]['objective'] = '2500000000000000001/1000000000000000000'
    result = compare_runs(current, manifest, tmp_path)
    assert result['best_improvement'] == '1/1000000000000000000'
    assert result['seeds_improved'] == 1


def test_paired_comparison_rejects_different_budgets(tmp_path):
    summary, manifest = batch()
    (tmp_path/'summary.json').write_text(json.dumps(summary))
    (tmp_path/'manifest.json').write_text(json.dumps(manifest))
    manifest['population'] = 24
    with pytest.raises(ValueError, match='population'):
        compare_runs(summary, manifest, tmp_path)
