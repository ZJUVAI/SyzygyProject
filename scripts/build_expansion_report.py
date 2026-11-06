"""Report accepted configuration additions from saved review evidence."""
import json
from pathlib import Path
import sys
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.registry import load_task


def read(path):
    return json.loads((ROOT / path).read_text())


def display(run):
    value = run['objective']
    if isinstance(value, int):
        return str(value)
    if 'sqrt2' in str(value):
        return str(value).replace('sqrt2', '√2')
    return format(float(Fraction(str(run.get('objective_value', value)))), '.12g')


def main():
    submissions = read('runs/configuration_expansion/review.json')
    release = {t['task_id']: t for t in read('runs/release_review/review.json')}
    audits = {a['config_id']: a for a in read('reports/independent_audit.json')}
    selections = {t['task_id']: t for t in read('research/configuration_selection.json')['tasks']}
    rows = ['# 新增配置基线与Sol验收', '',
            '2026-11-04：7个独立GPT-6 Luna任务代理实现14个新增配置，GPT-6.1 Sol复核。首批总量从21个配置增至35个，任务数保持20。', '',
            '每个新增配置均有初始程序、传统搜索、人类构造复现和固定参考。Sol运行了56次严格程序评测和14次冷启动导出检查，并独立复算关键量。全部35个配置的140次严格运行通过；全套187项测试、15项子测试通过。', '',
            '表内数值为原始数学目标；小数为显示值。精确值、认证区间、参数、来源与运行环境见JSON及保存构造。当前只报告逐配置成绩，尚未冻结跨配置汇总公式。', '',
            '| 配置 | 参数 | 方向 | 初始程序 | 传统搜索 | 人类对照 | 固定参考 |',
            '|---|---|---|---:|---:|---:|---:|']
    entries = []
    for submission in sorted(submissions, key=lambda t: t['task_id']):
        tid = submission['task_id']
        meta = load_task(tid)
        assert meta['configuration_expansion_review']['acceptance_status'] == 'accepted_by_sol'
        assert submission['automated_checks_passed'] and release[tid]['automated_checks_passed']
        for staged in submission['configurations']:
            cid = staged['config_id']
            config = next(c for c in meta['configurations'] if c['id'] == cid)
            assert config['acceptance_status'] == 'accepted_by_sol'
            runs = {r['program']: r for r in release[tid]['runs'] if r['config_id'] == cid}
            assert len(runs) == 4 and all(r['validity'] == 1 for r in runs.values())
            audit = audits[cid]
            assert audit['broken_construction_rejected'] and audit['claimed_score_ignored']
            entry = {'task_id': tid, 'config_id': cid, 'parameters': config['parameters'],
                     'direction': config['direction'], 'acceptance_status': 'accepted_by_sol',
                     'implementation_agent': meta['configuration_expansion_review']['implementation_agent'],
                     'implementation_model': 'gpt-6-luna', 'reviewer': 'GPT-6.1 Sol',
                     'program_runs': runs, 'cold_export_check': staged['cold_export_check'],
                     'independent_audit': audit, 'records': f'tasks/{tid.lower()}/records.json',
                     'witness_directory': f'reports/witnesses/{tid}/{cid}'}
            entries.append(entry)
            selected = next(c for c in selections[tid]['configurations'] if c['id'] == cid)
            label = selected.get('parameter_label', json.dumps(config['parameters'], ensure_ascii=False))
            direction = '最小化' if config['direction'] == 'minimize' else '最大化'
            rows.append('| ' + ' | '.join([cid, label, direction] + [display(runs[k]) for k in ('init_program', 'baseline', 'human', 'reference')]) + ' |')
    assert len(entries) == 14
    limitations = [
        'T002-C02（17个正方形）因公开Lean最优性证明及源代码重建报告而退役。本项目未完整重放该证明。以T002-C04（38个）替换，ID不复用。',
        '29个正方形采用Schadt的2025年传统搜索布局，并通过后续有理化证书复现。当前公开最好值更小，单列于纪录档案。',
        '等圆半径作保守缩小；Heilbronn的12点坐标按公开十进制文本解释为精确有理数。',
        'LABS采用公开历史搜索见证。部分来源未披露个人作者或AI参与情况，档案保留未知状态。',
        '传统搜索采用固定迭代预算与种子0。连续优化的结果可能随数值库与机器变化；最终有效性和数学成绩由独立检查器确认。',
        '本轮完成任务包和基线。未开展完整模型比较，未声称突破公开纪录。']
    rows += ['', '## 来源与限制', ''] + ['- ' + note for note in limitations]
    rows += ['', '逐配置来源见各任务的`records.json:configuration_records`。全部原始构造见`reports/witnesses/`。T002的两个新增人类见证可用`tasks/t002/rebuild_witnesses.py`离线重建。', '',
             '```sh', '.venv/bin/python -m mathbench evaluate T001 tasks/t001/baseline.py --config T001-C03 --strict --output runs/example',
             '.venv/bin/python -m mathbench replay T002 reports/witnesses/T002/T002-C04/human/solution.json',
             '.venv/bin/python scripts/independent_audit.py', '```', '']
    result = {'date': '2026-11-04', 'acceptance_status': 'accepted_by_sol',
              'task_count': 20, 'configuration_count': 35, 'expanded_task_count': 7,
              'added_configuration_count': 14, 'added_strict_program_runs': 56,
              'cold_export_checks': 14, 'full_strict_program_runs': 140,
              'passed_tests': 187, 'passed_subtests': 15,
              'full_model_experiments_run': False, 'limitations': limitations, 'configurations': entries}
    (ROOT / 'reports/configuration_expansion.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'reports/configuration_expansion.md').write_text('\n'.join(rows))
    print('Saved expansion report:', len(entries), 'accepted configurations')


if __name__ == '__main__':
    main()
