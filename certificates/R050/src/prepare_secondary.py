#!/usr/bin/env python3
"""Reconstruct the previously verified checker from pinned upstream bytes.

Upstream source is fetched locally, not redistributed in this repository.
Only this project's byte edits are distributed. Both hashes are mandatory.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCE_SHA = '63e858e28c4dee40f5763a832e1cfdf1f1fce3a1e5c632d087525bf1ee20ed14'
RESULT_SHA = 'b145b1ebbb2d3a0dccba62ee7b5ed64403bf0542ce5e8ee87113977df917faa4'
SOURCE_URL = ('https://raw.githubusercontent.com/Guzhou0806/n17-square-packing/'
              '32edfd3da78bf80a309398f552b3b602b9c45d6c/'
              'certificates/R038/src/exact_parent_side_scan.js')

def ensure_secondary(source=None):
    target = ROOT / '.cache' / 'secondary_mixed_scan.js'
    if target.exists():
        if hashlib.sha256(target.read_bytes()).hexdigest() != RESULT_SHA:
            raise ValueError('Cached secondary checker hash mismatch.')
        return target
    recipe = json.loads((ROOT/'secondary-adaptation.json').read_text())
    if (recipe['format'], recipe['source_sha256'], recipe['result_sha256'],
            recipe['source_url']) != (
            'sha256-pinned-byte-edits-v1', SOURCE_SHA, RESULT_SHA, SOURCE_URL):
        raise ValueError('Unexpected adaptation identity.')
    if source is None:
        with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
            original = response.read()
    else:
        original = Path(source).read_bytes()
    if hashlib.sha256(original).hexdigest() != SOURCE_SHA:
        raise ValueError('Upstream checker hash mismatch.')
    chunks, cursor = [], 0
    for edit in recipe['edits']:
        start, end = edit['start'], edit['end']
        if not (type(start) is int and type(end) is int
                and cursor <= start <= end <= len(original)):
            raise ValueError('Invalid or unordered byte edit.')
        chunks.extend((original[cursor:start], edit['replacement'].encode('utf-8')))
        cursor = end
    chunks.append(original[cursor:])
    reconstructed = b''.join(chunks)
    if hashlib.sha256(reconstructed).hexdigest() != RESULT_SHA:
        raise ValueError('Reconstructed checker differs from the verified file.')
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='secondary-', dir=target.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(reconstructed)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return target

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        help='Use an existing pinned upstream file; no download.')
    args = parser.parse_args()
    path = ensure_secondary(args.source)
    print('PASS: reconstructed checker matches completed verification, SHA-256 '+RESULT_SHA)
    print(path)
