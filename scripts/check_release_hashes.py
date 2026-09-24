#!/usr/bin/env python3
"""Check current publication bytes / 核对当前发布字节。"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify


def main():
    try:
        legacy = verify.read_json(ROOT / 'RELEASE_MANIFEST.json')
        r012 = verify.read_json(ROOT / 'R012_PUBLICATION.json')
        r038 = verify.read_json(ROOT / 'R038_PUBLICATION.json')
        r042 = verify.read_json(ROOT / 'R042_PUBLICATION.json')
        r043 = verify.read_json(ROOT / 'R043_PUBLICATION.json')
        r050 = verify.read_json(ROOT / 'R050_PUBLICATION.json')
        expected = dict(legacy['files'])
        expected.update(r012['files'])
        expected.update(r038['files'])
        expected.update(r042['files'])
        expected.update(r043['files'])
        expected.update(r050['files'])
        count = verify.check_file_map(ROOT, expected)
        print(f'PASS_RELEASE_BYTES: {count} current publication files match; no mathematics inferred. / 当前发布的 {count} 个文件字节匹配；此检查不推出数学正确性。')
        return 0
    except (verify.VerificationError, OSError, ValueError, KeyError) as exc:
        print(f'FAIL_RELEASE_BYTES: {exc} / 发布字节检查失败', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
