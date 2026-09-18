#!/usr/bin/env python3
"""Check all as-exported file bytes against RELEASE_MANIFEST.json.

This is an archive-integrity check, not a mathematical verification. Later
legitimate edits create a new release snapshot, not a reason to repair old hashes.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify


def main() -> int:
    try:
        record = verify.read_json(ROOT/'RELEASE_MANIFEST.json')
        n = verify.check_file_map(ROOT,record['files'])
        print(f'PASS_RELEASE_BYTES: {n} exported files match; no mathematics inferred.')
        return 0
    except (verify.VerificationError,OSError,ValueError,KeyError) as exc:
        print(f'FAIL_RELEASE_BYTES: {exc}',file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
