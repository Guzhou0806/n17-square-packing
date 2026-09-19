#!/usr/bin/env python3
"""Check current publication bytes / 核对当前发布字节.

Keep the original M19 release manifest as a historical record. R012's
publication manifest explicitly supersedes only changed presentation files
and adds its scientific files; mathematical replay remains separate.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify


def main():
    try:
        legacy = verify.read_json(ROOT / 'RELEASE_MANIFEST.json')
        publication = verify.read_json(ROOT / 'R012_PUBLICATION.json')
        expected = dict(legacy['files'])
        expected.update(publication['files'])
        count = verify.check_file_map(ROOT, expected)
        print(f'PASS_RELEASE_BYTES: {count} current publication files match; no mathematics inferred.')
        return 0
    except (verify.VerificationError, OSError, ValueError, KeyError) as exc:
        print(f'FAIL_RELEASE_BYTES: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
