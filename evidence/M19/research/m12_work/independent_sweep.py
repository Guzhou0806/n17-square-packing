"""Independent exact finite-direction coverage sweep. No third-party imports.

Authored from the centre-rectangle reduction and convex projection argument,
without reading the source repository's verifier/sweep implementation.
"""
from __future__ import annotations
import argparse
from bisect import bisect_left, bisect_right
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from math import lcm
from pathlib import Path
import sys
import time

SOURCE_SHA = '461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652'
SCALE = F(1000001, 1000000)


class RangeMin:
    def __init__(self, n):
        assert n > 0
        self.n = n
        self.val = [0] * (4*n)
        self.lazy = [0] * (4*n)

    def add(self, ql, qr, value):
        def visit(p, lo, hi):
            if ql <= lo and hi <= qr:
                self.val[p] += value
                self.lazy[p] += value
                return
            mid = (lo+hi)//2
            if ql < mid:
                visit(p*2, lo, mid)
            if qr > mid:
                visit(p*2+1, mid, hi)
            self.val[p] = self.lazy[p] + min(self.val[p*2], self.val[p*2+1])
        if ql < qr:
            visit(1, 0, self.n)

    def minimum(self, ql, qr):
        assert 0 <= ql < qr <= self.n
        def visit(p, lo, hi, carry):
            if ql <= lo and hi <= qr:
                return self.val[p] + carry
            carry += self.lazy[p]
            mid = (lo+hi)//2
            values = []
            if ql < mid:
                values.append(visit(p*2, lo, mid, carry))
            if qr > mid:
                values.append(visit(p*2+1, mid, hi, carry))
            return min(values)
        return visit(1, 0, self.n, 0)

    def argmin(self, ql, qr, target):
        # Called only on a strict improvement of the direction minimum.
        def visit(p, lo, hi, carry):
            if hi <= ql or qr <= lo:
                return None
            if ql <= lo and hi <= qr and self.val[p]+carry > target:
                return None
            if hi-lo == 1:
                return lo if self.val[p]+carry == target else None
            mid = (lo+hi)//2
            carry += self.lazy[p]
            left = visit(p*2, lo, mid, carry)
            return left if left is not None else visit(p*2+1, mid, hi, carry)
        answer = visit(1, 0, self.n, 0)
        assert answer is not None
        return answer


def clip(poly, axis, bound, lower):
    def inside(p):
        return p[axis] >= bound if lower else p[axis] <= bound
    result = []
    for p, q in zip(poly, poly[1:]+poly[:1]):
        ip, iq = inside(p), inside(q)
        if ip:
            result.append(p)
        if ip != iq:
            alpha = (bound-p[axis])/(q[axis]-p[axis])
            result.append(tuple(p[k]+alpha*(q[k]-p[k]) for k in (0, 1)))
    return result


def cell_point(poly, ua, ub, va, vb):
    for axis, bound, lower in [(0, ua, True), (0, ub, False),
                                (1, va, True), (1, vb, False)]:
        poly = clip(poly, axis, bound, lower)
        assert poly, 'empty claimed cell'
    poly = list(dict.fromkeys(poly))
    area2 = sum(p[0]*q[1]-p[1]*q[0] for p, q in zip(poly, poly[1:]+poly[:1]))
    assert area2 != 0, 'zero-area claimed cell'
    point = tuple(sum(p[k] for p in poly)/len(poly) for k in (0, 1))
    assert ua < point[0] < ub and va < point[1] < vb
    return point


def geometry(S, B, atoms, t):
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    assert c > 0 and s >= 0 and c*c+s*s == 1
    r = B*(c+s)/2
    assert 0 <= r < S/2
    poly = [(c*x+s*y, -s*x+c*y) for x, y in
            [(r, r), (S-r, r), (S-r, S-r), (r, S-r)]]
    rotated = [(c*x+s*y, -s*x+c*y, w) for x, y, w in atoms]
    return c, s, r, poly, rotated


def coverage(S, B, atoms, t):
    c, s, r, poly, rotated = geometry(S, B, atoms, t)
    denom = lcm(*(w.denominator for _, _, w in atoms))
    rectangles = [(u-B/2, u+B/2, v-B/2, v+B/2, int(w*denom))
                  for u, v, w in rotated]
    vs = sorted({v for _, _, lo, hi, _ in rectangles for v in (lo, hi)} |
                {v for _, v in poly})
    vi = {v: k for k, v in enumerate(vs)}
    events = defaultdict(list)
    for a, b, lo, hi, w in rectangles:
        events[a].append((vi[lo], vi[hi], w))
        events[b].append((vi[lo], vi[hi], -w))
    for u, _ in poly:
        events[u]  # Include all changes in the polygon's affine boundaries.
    us = sorted(events)
    umin, umax = min(u for u, _ in poly), max(u for u, _ in poly)
    tree = RangeMin(len(vs)-1)
    best = None
    best_cell = None
    strips = 0
    def lower(u):
        return max((c*u-(S-r))/s, (r-s*u)/c)
    def upper(u):
        return min((c*u-r)/s, ((S-r)-s*u)/c)
    for a, b in zip(us, us[1:]):
        for lo, hi, w in events[a]:
            tree.add(lo, hi, w)
        if b <= umin:
            continue
        if a >= umax:
            break
        assert umin <= a < b <= umax
        if s == 0:
            vlo, vhi = r, S-r
        else:
            vlo, vhi = min(lower(a), lower(b)), max(upper(a), upper(b))
        assert vlo < vhi
        first = max(0, bisect_right(vs, vlo)-1)
        stop = min(len(vs)-1, bisect_left(vs, vhi))
        assert first < stop
        value = tree.minimum(first, stop)
        strips += 1
        if best is None or value < best:
            best = value
            leaf = tree.argmin(first, stop, value)
            best_cell = (a, b, vs[leaf], vs[leaf+1])
    assert best is not None and best_cell is not None
    point = cell_point(poly, *best_cell)
    direct = sum(w for u, v, w in rotated
                 if abs(u-point[0]) <= B/2 and abs(v-point[1]) <= B/2)
    assert direct == F(best, denom), 'direct witness mismatch'
    x, y = c*point[0]-s*point[1], s*point[0]+c*point[1]
    assert r < x < S-r and r < y < S-r
    return {'t': str(t), 'minimum': str(direct), 'strips': strips,
            'u_events': len(us), 'v_events': len(vs),
            'cell': list(map(str, best_cell)),
            'centre_uv': list(map(str, point)), 'centre_xy': [str(x), str(y)],
            'direct_count_check': True}


def check_static(record, scale=SCALE):
    S, B = F(record['outer_side']), F(record['square_side'])
    assert type(record['n']) is int and record['n'] == 17
    assert type(record['direction_steps']) is int and record['direction_steps'] == 180
    assert record['symmetry'] == 'D4'
    atoms = [(F(x), F(y), F(w)) for x, y, w in record['atoms']]
    assert atoms and all(0 <= x <= S and 0 <= y <= S and w >= 0 for x, y, w in atoms)
    measure = defaultdict(F)
    for x, y, w in atoms:
        measure[x, y] += w
    for (x, y), w in measure.items():
        assert measure.get((S-y, x), F(0)) == w, 'D4 rotation failed'
        assert measure.get((S-x, y), F(0)) == w, 'D4 reflection failed'
    total = sum(w for _, _, w in atoms)
    assert total == F(record['total_mass']) and total < record['n']
    limit = F(record['angle_limit'])
    assert 0 < limit < 1 and limit*limit+2*limit-1 >= 0, 'arc endpoint failed'
    ts = [limit*k/record['direction_steps'] for k in range(record['direction_steps']+1)]
    assert ts[0] == 0 and all(a < b for a, b in zip(ts, ts[1:]))
    D = max((b-a)/(1+a*b) for a, b in zip(ts, ts[1:]))
    margin = 1-scale*B*(1+D)
    assert scale > 1 and margin > 0, 'strict containment failed'
    scaled = [(scale*x, scale*y, w) for x, y, w in atoms]
    assert all((x/scale, y/scale, w) == original for (x,y,w), original in zip(scaled, atoms))
    return S, B, atoms, ts, {'total_mass': str(total), 'mass_margin': str(record['n']-total),
        'atoms': len(atoms), 'sites': len(measure), 'D4': True, 'arc_endpoint': str(limit),
        'arc_polynomial': str(limit*limit+2*limit-1), 'D': str(D),
        'scale': str(scale), 'new_side': str(scale*S), 'new_probe_side': str(scale*B),
        'strict_containment_margin': str(margin), 'inverse_scaling_checked_atoms': len(scaled)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=int, default=600)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    record = json.loads(raw)
    S, B, atoms, ts, static = check_static(record)
    args.output.mkdir(parents=True, exist_ok=False)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    start = time.perf_counter()
    rows = []
    with (args.output/'DIRECTIONS.jsonl').open('x', encoding='utf-8') as stream:
        for k, t in enumerate(ts):
            if time.perf_counter()-start > args.seconds:
                break
            row = coverage(S, B, atoms, t)
            row['index'] = k
            rows.append(row)
            stream.write(json.dumps(row, sort_keys=True)+'\n')
            stream.flush()
            if k % 30 == 0 or k == len(ts)-1:
                print(f'direction {k}/{len(ts)-1}: minimum={row["minimum"]}; elapsed={time.perf_counter()-start:.1f}s', flush=True)
    worst = min(F(row['minimum']) for row in rows) if rows else None
    complete = len(rows) == len(ts)
    passed = complete and worst >= 1
    result = {'schema': 'n17.m12.independent-coverage.v1',
              'status': 'PASS_EXACT_COVERAGE_AND_FIXED_SCALING' if passed else ('FAIL_COVERAGE' if complete else 'BUDGET_EXHAUSTED'),
              'input_sha256': SOURCE_SHA, 'source_sha256': source_hash,
              'python': sys.version, 'static': static, 'directions_completed': len(rows),
              'minimum': str(worst), 'declared_minimum': record['least_cell_mass'],
              'matches_declared_minimum': worst == F(record['least_cell_mass']),
              'seconds': time.perf_counter()-start,
              'claim': 'Independent exact finite coverage plus fixed scaling; final registration requires external review.'}
    (args.output/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
