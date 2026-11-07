"""Show the four requested raw objectives for every fixed configuration."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
from decimal import Decimal, localcontext
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def read(path):
    return json.loads(path.read_text())


def display(value, digits=15, quadratic_radicand=None):
    """Round only for display. Preserve the original value in JSON output."""
    if value is None:
        return '—'
    if quadratic_radicand is not None and isinstance(value,str) and value.startswith('['):
        a,b=map(Fraction,value[1:-1].split(','))
        if b==0:
            return display(str(a),digits=digits)
        with localcontext() as ctx:
            ctx.prec=max(60,digits+15)
            v=Decimal(a.numerator)/Decimal(a.denominator)+Decimal(b.numerator)/Decimal(b.denominator)*Decimal(quadratic_radicand).sqrt()
        return format(v,f'.{digits}g')
    named_root = re.fullmatch(r'(fourth|eighth)_root\(([^()]+)\)',str(value))
    power_root = re.fullmatch(r'\(([+-]?\d+(?:/[+-]?\d+)?)\)\^\(1/(4|8)\)',str(value))
    if named_root or power_root:
        if named_root:
            degree=4 if named_root.group(1)=='fourth' else 8
            exact=Fraction(named_root.group(2))
        else:
            degree=int(power_root.group(2));exact=Fraction(power_root.group(1))
        if exact<0:
            raise ValueError('An even real root needs a nonnegative value')
        with localcontext() as ctx:
            ctx.prec=max(60,digits+15)
            number=Decimal(exact.numerator)/Decimal(exact.denominator)
            for _ in range(2 if degree==4 else 3):number=number.sqrt()
        return format(number,f'.{digits}g')
    if isinstance(value,str) and value.startswith('sqrt_sum:'):
        terms=json.loads(value.removeprefix('sqrt_sum:'))
        if not isinstance(terms,list) or not terms or any(type(d)is not int or d<0 for d in terms):
            raise ValueError('A square-root sum needs nonnegative integer radicands')
        with localcontext() as ctx:
            ctx.prec=max(60,digits+15)
            number=sum((Decimal(d).sqrt() for d in terms),Decimal(0))
        return format(number,f'.{digits}g')
    if type(value) is int:
        return str(value) if abs(value) < 10**30 else format(value, '.12g')
    try:
        exact = Fraction(str(value))
        if exact.denominator == 1:
            return display(exact.numerator)
        with localcontext() as ctx:
            ctx.prec = max(60, digits+15)
            number = Decimal(exact.numerator) / Decimal(exact.denominator)
    except (ValueError, TypeError, ZeroDivisionError):
        if 'sqrt' in str(value):
            from tasks.t002.check import Q
            q = Q.parse(str(value).replace('sqrt(2)', 'sqrt2'))
            with localcontext() as ctx:
                ctx.prec = max(60, digits+15)
                number = Decimal(q.a.numerator)/Decimal(q.a.denominator) + Decimal(q.b.numerator)/Decimal(q.b.denominator)*Decimal(2).sqrt()
        else:
            decimal = re.search(r'0\.\d+', str(value))
            if decimal is None:
                return str(value)
            number = Decimal(decimal.group())
    return format(number, f'.{digits}g')


def collect():
    from mathbench.registry import INITIAL_TASKS, load_task, task_path
    rows = []
    for task_id in INITIAL_TASKS:
        directory = task_path(task_id)
        if not (directory / 'task.json').is_file():
            continue
        task = load_task(task_id)
        if task.get('acceptance_status') != 'accepted_by_sol':
            continue
        public = read(directory / 'sota.json')['configurations']
        initial_results = read(directory / 'records.json').get('initial_results', {})
        for config in task['configurations']:
            cid = config['id']
            initial = initial_results.get(cid)
            own_file = directory / 'best' / cid / 'result.json'
            own = read(own_file) if own_file.exists() else None
            record = public[cid]
            reproduced = record.get('verification', {}).get('run', {})
            reported = record.get('highest_reported', {}).get('value', record.get('public_value'))
            rows.append({
                'task_id': task['task_id'], 'config_id': cid,
                'parameters': config['parameters'], 'direction': config['direction'],
                'initial': initial.get('objective') if initial else None,
                'search': own.get('objective') if own and own.get('validity') == 1 else None,
                'best_reproduced': reproduced.get('objective') if reproduced.get('validity') == 1 else None,
                'best_reported': reported,
                'public_checked_at': record.get('checked_at'),
                'reported_witness_status': record.get('highest_reported', {}).get('reproduction_status'),
            })
    return rows


def markdown(rows, underline_best=False, highlight_best=False):
    lines = ['| 配置 | 初始程序 ↕ | 搜索结果 ↕ | 最佳结果（复现）↕ | 最佳结果（报告）↕ |',
             '|---|---:|---:|---:|---:|']
    for row in rows:
        arrow = '↑' if row['direction'] == 'maximize' else '↓'
        raw = [row[key] for key in ('initial', 'search', 'best_reproduced', 'best_reported')]
        radicand=3 if row.get('task_id')=='T083' else None
        def comparable(value):
            if value is None:
                return None
            try:
                return Fraction(str(value))
            except (ValueError, TypeError, ZeroDivisionError):
                return Fraction(display(value, digits=16, quadratic_radicand=radicand))
        exact = [comparable(v) for v in raw]
        valid = [v for v in exact if v is not None]
        best = (max if row['direction'] == 'maximize' else min)(valid) if valid else None
        close = [v is not None and best is not None and
                 (v == best if v.denominator == best.denominator == 1 else
                  abs(v-best) <= Fraction('1e-12')*max(abs(v),abs(best))) for v in exact]
        uncertain = any(is_close and v != best for v,is_close in zip(exact,close))
        values = [display(v, digits=16, quadratic_radicand=radicand) for v in raw]
        if underline_best or highlight_best:
            values = [(f'**≈ {v}**' if highlight_best else f'≈ {v}')
                      if uncertain and is_close else
                      (f'**🏆 {v}**' if highlight_best else f'<u>{v}</u>')
                      if e is not None and e == best else v
                      for v,e,is_close in zip(values,exact,close)]
        lines.append(f"| {row['config_id']} {arrow} | " + ' | '.join(values) + ' |')
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--underline-best', action='store_true')
    parser.add_argument('--highlight-best', action='store_true')
    args = parser.parse_args()
    rows = collect()
    if args.json:
        print(json.dumps({'generated_utc': datetime.now(timezone.utc).isoformat(),
                          'scope': 'Own verified search result and archived same-parameter public results.',
                          'configurations': rows}, ensure_ascii=False, indent=2))
    else:
        print(markdown(rows, underline_best=args.underline_best, highlight_best=args.highlight_best))
