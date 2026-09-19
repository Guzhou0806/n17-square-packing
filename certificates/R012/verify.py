#!/usr/bin/env python3
"""R012 public replay / R012 公开复验. Python 3.10+, standard library only.

No numerical optimizer, network, prior PASS log or private workspace is used.
Every catalogue interval is checked over its complete parent-center envelope.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
from sweep import coverage, direct_mass, trig

ROOT = Path(__file__).resolve().parent
SUCCESS = 'PASS_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND'
ATOM_DIGEST = 'ae469399ced8580ddddcef6edc234cf9becd7e94df7752aa8b4f9cefcbaf3643'


def need(ok, text):
    if not ok:
        raise ValueError(text)


def read(path):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'duplicate JSON key')
            out[key] = value
        return out
    def bad(value):
        raise ValueError('nonfinite JSON value')
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=pairs, parse_constant=bad)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrity():
    record = read(ROOT / 'MANIFEST.json')
    expected = record['files']
    actual = set()
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if rel.parts[0] == '.replay-runs':
            continue
        need(not path.is_symlink(), 'symlinks not allowed in certificate')
        if path.is_file() and rel.as_posix() != 'MANIFEST.json':
            actual.add(rel.as_posix())
    need(actual == set(expected), 'certificate file set differs from manifest')
    for name, digest in expected.items():
        rel = Path(name)
        need(not rel.is_absolute() and '..' not in rel.parts, 'unsafe manifest path')
        need(sha(ROOT / rel) == digest, 'SHA-256 mismatch: ' + name)
    return {'status': 'PASS', 'files': len(expected),
            'manifest_sha256': sha(ROOT / 'MANIFEST.json')}


def load_math():
    c = read(ROOT / 'catalogue.json')
    need((c['L'], c['A'], c['h'], c['T'], c['mass'], c['gamma'], c['target']) ==
         ('4613/1000', '99999/100000', '207107/1440000000',
          '207107/500000', '424969/25000', '250023/250000', '461300/99999'),
         'changed theorem parameters')
    L, A, h, T, M, gamma = (F(c[k]) for k in ('L', 'A', 'h', 'T', 'mass', 'gamma'))
    measure = {}
    rows = read(ROOT / 'orbits.json')
    need(len(rows) == 206, 'orbit count')
    for row in rows:
        need(len(row) == 3 and all(type(v) is int for v in row), 'integer orbit required')
        x, y, w = F(row[0], 100000), F(row[1], 100000), F(row[2], 1000000)
        need(0 <= x <= L and 0 <= y <= L and w > 0, 'invalid orbit')
        images = {(a, b) for u, v in ((x, y), (y, x))
                  for a in (u, L-u) for b in (v, L-v)}
        need(not images.intersection(measure), 'duplicate or overlapping orbit')
        measure.update({p: w for p in images})
    atoms = [(x, y, w) for (x, y), w in sorted(measure.items())]
    need(len(atoms) == 1616 and sum((p[2] for p in atoms), F()) == M, 'atomic mass/count')
    canonical = json.dumps([[str(v) for v in row] for row in atoms],
                           separators=(',', ':')).encode()
    need(hashlib.sha256(canonical).hexdigest() == ATOM_DIGEST, 'source measure differs')
    need(T == 2880*h and T*T+2*T > 1 and M < 17*gamma, 'net endpoint or mass gap')
    entries = []
    need(len(c['low']) == 60, 'explicit entry count')
    for row in c['low']:
        need(len(row) == 4 and all(isinstance(v, str) for v in row), 'entry format')
        entries.append(tuple(map(F, row)))
    need(c['ranges'] == [[16, 978, '6249/6250'],
                        [978, 1145, '49992449/50000000'],
                        [1145, 2881, '19997/20000']], 'range definitions')
    for first, stop, B in c['ranges']:
        for k in range(first, stop):
            entries.append((max(F(), (k-F(1, 2))*h), min(T, (k+F(1, 2))*h), k*h, F(B)))
    cursor, margins, jobs = F(), [], []
    for i, (lo, hi, t, B) in enumerate(entries):
        need(lo == cursor and 0 <= lo < hi < 1 and 0 <= t < 1 and 0 < B < A < L,
             'angle gap, overlap or invalid entry')
        ct, st = trig(t)
        widths, factors = [], []
        for u in (lo, hi):
            cp, sp = trig(u)
            dot, cross = ct*cp+st*sp, abs(st*cp-ct*sp)
            need(dot > 0 and dot >= cross, 'relative angle outside supported range')
            widths.append(cp+sp)
            factors.append(dot+cross)
        margin = A-B*max(factors)
        inset = A*min(widths)/2
        need(margin > 0, 'core is not strictly interior throughout parent interval')
        need(B*(ct+st)/2 <= inset < L/2, 'invalid full parent-center envelope')
        jobs.append((i, t, B, inset))
        cursor = hi
        margins.append(margin)
    need(len(jobs) == 2925 and cursor == T, 'incomplete continuous angle union')
    need(sum((r[2]/h).denominator != 1 for r in entries) == 48, 'off-net count')
    target = L/A
    old2 = F(c['previous_endpoint_squared'])
    need(old2 == F(17650291964463886688094912400, 829429719507765981945905041),
         'comparison source changed')
    need(target*target > old2, 'no strict improvement over pinned source')
    scale = 10**20
    n = target.numerator*scale//target.denominator
    fmt = lambda v: f'{v//scale}.{v%scale:020d}'
    summary = {'claim': 's(17) >= 461300/99999', 'lower_bound': str(target),
               'decimal_bracket_20': [fmt(n), fmt(n+1)],
               'mass': str(M), 'common_gamma': str(gamma), 'mass_gap': str(17*gamma-M),
               'atoms': len(atoms), 'orbits': len(rows), 'parent_angle_intervals': len(jobs),
               'off_net_core_entries': 48, 'minimum_containment_margin': str(min(margins)),
               'squared_improvement': str(target*target-old2),
               'expanded_measure_sha256': ATOM_DIGEST}
    return L, A, atoms, gamma, jobs, summary


def counterexamples(L, A, atoms):
    examples = read(ROOT / 'counterexamples.json')
    need(len(examples) == 5, 'negative-control count')
    for e in examples:
        B, t = F(e['B']), F(e['t'])
        xy = tuple(map(F, e['centre']))
        lo, hi = map(F, e['parent_interval'])
        parent_t = min((lo, hi), key=lambda u: sum(trig(u)))
        cp, sp = trig(parent_t)
        r = A*(cp+sp)/2
        need(all(r <= v <= L-r for v in xy), 'not a real parent-center witness')
        ct, st = trig(t)
        need(B*(ct*cp+st*sp+abs(st*cp-ct*sp)) < A, 'negative-control core not interior')
        mass, ids = direct_mass(atoms, B, t, xy)
        vertices = [(xy[0]+B*(a*ct-b*st)/2, xy[1]+B*(a*st+b*ct)/2)
                    for a, b in ((-1,-1),(1,-1),(1,1),(-1,1))]
        polyids = [i for i, (px, py, w) in enumerate(atoms)
                   if all((q[0]-p[0])*(py-p[1])-(q[1]-p[1])*(px-p[0]) >= 0
                          for p, q in zip(vertices, vertices[1:]+vertices[:1]))]
        need(ids == polyids, 'projection/polygon membership disagreement')
        need(mass == F(e['mass']) and len(ids) == e['atom_count'] and mass < 1,
             'negative-control charge mismatch')
    return len(examples)


_GLOBAL = None

def initialize(L, atoms):
    global _GLOBAL
    _GLOBAL = L, atoms


def run_entry(job):
    i, t, B, inset = job
    L, atoms = _GLOBAL
    result = coverage(L, B, atoms, t, inset, backend='tree')
    return {'index': i, 'minimum': result['minimum'], 'slabs': result['slabs'],
            'centre': result['centre_xy'], 'direct_recount': result['direct_recount']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='new output directory / 新输出目录')
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--records', action='store_true', help='NO geometric replay / 不运行覆盖')
    args = parser.parse_args(argv)
    out = None
    start = time.monotonic()
    try:
        need(sys.version_info >= (3, 10), 'Python 3.10+ required')
        need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'),
             'optimized Python is not accepted')
        need(1 <= args.workers <= 16, 'workers must be in [1,16]')
        path = Path(args.output).expanduser()
        need(not path.exists(), 'output already exists')
        resolved = path.resolve()
        if resolved.is_relative_to(ROOT):
            need(resolved.is_relative_to(ROOT / '.replay-runs'), 'protected certificate output')
        before = integrity()
        L, A, atoms, gamma, jobs, report = load_math()
        report['negative_controls'] = counterexamples(L, A, atoms)
        path.mkdir(parents=True, exist_ok=False)
        out = path
        report.update({'mode': 'records' if args.records else 'full',
                       'python': platform.python_version(), 'system': platform.system(),
                       'started_at_utc': datetime.now(timezone.utc).isoformat(),
                       'workers': args.workers, 'integrity_before': before})
        if not args.records:
            minima, slabs = [], 0
            with (out / 'coverage.jsonl').open('x', encoding='utf-8') as log:
                with ProcessPoolExecutor(max_workers=args.workers,
                                         initializer=initialize, initargs=(L, atoms)) as pool:
                    for expected, row in enumerate(pool.map(run_entry, jobs, chunksize=8)):
                        need(row['index'] == expected, 'missing or reordered entry')
                        value = F(row['minimum'])
                        need(value >= gamma and row['direct_recount'], 'coverage obligation failed')
                        log.write(json.dumps(row, sort_keys=True)+'\n')
                        log.flush()
                        minima.append(value)
                        slabs += row['slabs']
                        if (expected+1) % 200 == 0:
                            print(f'Completed {expected+1}/{len(jobs)} intervals', flush=True)
            need(len(minima) == 2925, 'incomplete scan')
            report.update({'coverage_entries_recomputed': len(minima),
                           'actual_catalogue_minimum': str(min(minima)), 'center_strips': slabs,
                           'coverage_log_sha256': sha(out / 'coverage.jsonl')})
        report['integrity_after'] = integrity()
        need(before == report['integrity_after'], 'certificate changed during replay')
        report['status'] = 'PASS_RECORDS_ONLY' if args.records else SUCCESS
        report['seconds'] = time.monotonic()-start
        report['scope'] = ('Supplied exact programs; same event geometry; no independent external '
                           'review or formalization. Records mode does not establish coverage.')
        (out / 'RESULT.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        print(report['status'], flush=True)
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        failure = {'status': 'FAIL_OR_INCOMPLETE', 'error_type': type(exc).__name__,
                   'seconds': time.monotonic()-start}
        if out is not None:
            (out / 'RESULT.json').write_text(json.dumps(failure, indent=2)+'\n', encoding='utf-8')
        print(f"FAIL_OR_INCOMPLETE: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
