"""Optional exact C++ backend; immutable frozen Python implementations remain oracles.

All geometry and containment is rational. cpp_int coordinates are unbounded;
only signed charges use int64, guarded by an absolute expanded mass < 2**50.
This module computes centre minima, not resource capacity or a new theorem.
"""
from collections import Counter
import ctypes
from itertools import combinations
import json
from math import comb, lcm
from pathlib import Path
import native_geometry as legal


def need(ok, message):
    if not ok:
        raise ValueError(message)


def prepare_model(cert, sites, owners, weights, *, allow_signed_expression=False):
    D = cert['coordinate_denominator']
    LD = legal.Q(cert['L'])*D
    need(type(D) is int and D > 0 and LD.denominator == 1, 'site scale')
    need(len(owners) == len(sites) and all(type(x) is int and type(y) is int for x, y in sites), 'sites')
    need(len(weights) == 3 and len(weights[0]) == len(cert['point_orbits']) and
         len(weights[1]) == len(cert['threshold_orbits']) and
         len(weights[2]) == len(cert.get('generic_trigger_orbits', [])), 'weight lengths')
    need(all(type(w) is int for group in weights for w in group), 'integer weights')
    need(allow_signed_expression or all(w >= 0 for group in weights for w in group),
         'negative resource weights require explicit open-cell expression mode')
    terms = Counter()
    for i, owner in enumerate(owners):
        need(type(owner) is int and 0 <= owner < len(weights[0]), 'owner')
        terms[(i,)] += weights[0][owner]
    for objects, ws, key, fixed_k in [(cert['threshold_orbits'], weights[1], 'triples', 2),
                                    (cert.get('generic_trigger_orbits', []), weights[2], 'groups', None)]:
        for obj, w in zip(objects, ws):
            k = fixed_k if fixed_k else obj['k']
            for group in obj[key]:
                need(type(k) is int and 1 <= k <= len(group) and len(group) == len(set(group)) and
                     all(type(i) is int and 0 <= i < len(sites) for i in group), 'trigger indices')
                need(fixed_k is None or len(group) == 3, 'threshold triple')
                if not w:
                    continue
                for size in range(k, len(group)+1):
                    coeff = (-1 if (size-k)%2 else 1)*comb(size-1, k-1)*w
                    for subset in combinations(group, size):
                        terms[tuple(sorted(subset))] += coeff
    terms = [(ids, w) for ids, w in terms.items() if w]
    mass = sum(abs(w) for _, w in terms)
    need(mass < 2**50, 'expanded signed mass exceeds native safe range')
    lines = [f'1 {len(sites)} {len(terms)}']
    lines += [f'{2*x-int(LD)} {2*y-int(LD)}' for x, y in sites]
    lines += [f'{w} {len(ids)} '+ ' '.join(map(str, ids)) for ids, w in terms]
    return ('\n'.join(lines)+'\n').encode('ascii'), mass


def row_parameters(cert, row):
    vals = legal.row_geometry(cert, row)
    names = ['L', 'A', 'a', 'b', 't', 'B', 'c', 's', 'low', 'high', 'parent_t', 'parent_c', 'parent_s']
    grid = dict(zip(names, vals))
    L, _, _, _, t, B, _, _, low, *_ = vals
    D = cert['coordinate_denominator']
    p, q = t.numerator, t.denominator
    C, S, R = q*q-p*p, 2*p*q, q*q+p*p
    H = L/2-low
    scale = lcm(2*D, (B/2).denominator, H.denominator)
    half, h = B*scale/2, H*scale
    need(half.denominator == h.denominator == 1 and C >= S >= 0, 'native row scale/octant')
    grid['scale_denominator'] = R*scale
    h = int(h)
    grid['polygon'] = [(C*x+S*y, -S*x+C*y) for x, y in [(-h,-h),(h,-h),(h,h),(-h,h)]]
    return f'{C} {S} {scale//(2*D)} {int(half)*R} {h}'.encode('ascii'), grid


class NativeModel:
    """Immutable model supports concurrent scan calls; close only after all calls finish."""
    def __init__(self, library, cert, sites=None, owners=None, weights=None, *, allow_signed_expression=False):
        self.lib = ctypes.CDLL(str(Path(library).resolve()))
        self.lib.n17_create.argtypes = [ctypes.c_char_p]
        self.lib.n17_create.restype = ctypes.c_void_p
        self.lib.n17_destroy.argtypes = [ctypes.c_void_p]
        self.lib.n17_destroy.restype = None
        self.lib.n17_scan.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        self.lib.n17_scan.restype = ctypes.c_void_p
        self.lib.n17_free.argtypes = [ctypes.c_void_p]
        self.lib.n17_free.restype = None
        self.lib.n17_error.argtypes = []
        self.lib.n17_error.restype = ctypes.c_char_p
        self.cert = cert
        if sites is None:
            sites, owners = legal.physical_sites(cert)
        if weights is None:
            weights = legal.weight_vectors(cert, None)
        # Research Mobius expressions may have negative coefficients even when
        # the original table is monotone. The caller must separately prove that
        # property; this opt-in only computes open-cell values, never a theorem.
        self.model_bytes, self.mass = prepare_model(cert, sites, owners, weights,
                                                   allow_signed_expression=allow_signed_expression)
        self.handle = self.lib.n17_create(self.model_bytes)
        if not self.handle:
            raise ValueError(self.lib.n17_error().decode())

    def row(self, row, samples=0, detail=False):
        need(self.handle is not None, 'closed native model')
        parameters, grid = row_parameters(self.cert, row)
        ptr = self.lib.n17_scan(self.handle, parameters, samples, int(detail))
        if not ptr:
            raise ValueError(self.lib.n17_error().decode())
        try:
            result = json.loads(ctypes.string_at(ptr))
        finally:
            self.lib.n17_free(ptr)
        result['row'] = row
        return result, grid

    def close(self):
        if self.handle is not None:
            self.lib.n17_destroy(self.handle)
            self.handle = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
