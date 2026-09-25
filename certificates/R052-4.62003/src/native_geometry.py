"""Unchanged exact geometry subset / 原样提取的精确几何子集。"""
from __future__ import annotations
from fractions import Fraction as Q

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def trig(t: Q) -> tuple[Q, Q]:
    return (1-t*t)/(1+t*t), 2*t/(1+t*t)


def physical_sites(cert: dict) -> tuple[list[tuple[int, int]], list[int]]:
    scale = cert['coordinate_denominator']
    require(type(scale) is int and scale > 0, 'invalid coordinate denominator')
    side = Q(cert['L'])*scale
    require(side.denominator == 1, 'outer side not integral on site grid')
    outer = int(side)
    sites: list[tuple[int, int]] = []
    owners: list[int] = []
    for j, (x, y, weight) in enumerate(cert['point_orbits']):
        require(all(type(z) is int for z in (x, y, weight)) and
                0 <= x <= outer and 0 <= y <= outer and weight >= 0,
                'invalid point orbit')
        image = sorted({(a, b) for u, v in ((x, y), (y, x))
                        for a in (u, outer-u) for b in (v, outer-v)})
        sites.extend(image)
        owners.extend([j]*len(image))
    require(len(sites) == len(set(sites)), 'duplicate physical site')
    return sites, owners


def weight_vectors(cert: dict, override: dict | None) -> tuple[list[int], list[int], list[int]]:
    vectors = ([item[2] for item in cert['point_orbits']],
               [item['weight'] for item in cert['threshold_orbits']],
               [item['weight'] for item in cert.get('generic_trigger_orbits', [])])
    if override is None:
        pass
    elif 'nonzero' in override:
        vectors = tuple([0]*len(part) for part in vectors)
        types = {'point': 0, 'threshold': 1, 'generic': 2}
        seen = set()
        for item in override['nonzero']:
            family, index = types[item['type']], item['index']
            require(type(index) is int and 0 <= index < len(vectors[family]),
                    'override weight index outside fixed support')
            require((family, index) not in seen, 'duplicate override weight')
            seen.add((family, index))
            vectors[family][index] = item['weight_units']
    else:
        require(len(override['point_orbits']) == len(vectors[0]) and
                len(override['threshold_orbits']) == len(vectors[1]) and
                len(override.get('generic_trigger_orbits', [])) == len(vectors[2]),
                'override support length mismatch')
        require([item[:2] for item in override['point_orbits']] ==
                [item[:2] for item in cert['point_orbits']],
                'override point support mismatch')
        require([item['triples'] for item in override['threshold_orbits']] ==
                [item['triples'] for item in cert['threshold_orbits']] and
                [(item['k'], item['groups'])
                 for item in override.get('generic_trigger_orbits', [])] ==
                [(item['k'], item['groups'])
                 for item in cert.get('generic_trigger_orbits', [])],
                'override trigger support mismatch')
        vectors = ([item[2] for item in override['point_orbits']],
                   [item['weight'] for item in override['threshold_orbits']],
                   [item['weight'] for item in override.get('generic_trigger_orbits', [])])
    require(all(type(w) is int and w >= 0 for part in vectors for w in part),
            'weights must be nonnegative integers')
    return vectors


def row_geometry(cert: dict, row: int):
    require(0 <= row < len(cert['entries']), 'row out of range')
    L, A = Q(cert['L']), Q(cert['A'])
    a, b, t, B = map(Q, cert['entries'][row])
    require(0 <= a < b < 1 and a <= t <= b and 0 < B < A < L,
            'invalid row geometry')
    c, s = trig(t)
    fa, fb = sum(trig(a)), sum(trig(b))
    parent_t = a if fa <= fb else b
    parent_c, parent_s = trig(parent_t)
    radius = A*min(fa, fb)/2
    low, high = radius, L-radius
    require(low < high, 'parent legal-center domain has no interior')
    # Strict containment of the selected probe in every parent orientation
    # of this interval, following the original package's rational criterion.
    for endpoint in (a, b):
        ce, se = trig(endpoint)
        dot, cross = c*ce+s*se, abs(c*se-s*ce)
        require(dot > 0 and dot >= cross,
                'row angle too far from probe orientation')
        require(A-B*(dot+cross) > 0, 'probe not strictly in parent interval')
    require(B*(c+s)/2 <= radius, 'probe not contained by source envelope')
    return L, A, a, b, t, B, c, s, low, high, parent_t, parent_c, parent_s

