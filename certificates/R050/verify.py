#!/usr/bin/env python3
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import concurrent.futures
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CERT = ROOT / 'certificate/R050_CERTIFICATE.json.gz'
PYTHON = ROOT / 'results/R050_PYTHON_FULL_REPLAY.json.gz'
PARTS = ROOT / 'results/bigint-parts'
CERT_SHA = '84283b2af955b85184dc4793ae2b65e08aae5f3817a611038598dd54f479f400'
PYTHON_SHA = 'a7b256a6a7c0273f99977400915563ff6a7374d56a0701c490d384f4f7ef9ad1'
CHECKER_SHA = 'b145b1ebbb2d3a0dccba62ee7b5ed64403bf0542ce5e8ee87113977df917faa4'
ROWS = 15706
MINIMUM = 1000271689
BUDGET = 17003093868
BOUND = F(4613000, 998509)


def need(ok, en, zh):
    if not ok:
        raise ValueError(en + ' / ' + zh)


def raw_json(path):
    data = path.read_bytes()
    if path.suffix == '.gz':
        data = gzip.decompress(data)
    return data, json.loads(data)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_manifest():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text(encoding='utf-8'))
    need(manifest['schema'] == 'n17.r050.public-package.manifest.v1',
         'manifest schema mismatch', '清单格式不匹配')
    found = set()
    for entry in manifest['files']:
        name = entry['path']
        path = Path(name)
        need(not path.is_absolute() and '..' not in path.parts and '\\' not in name
             and name not in found and name != 'MANIFEST.json',
             'invalid manifest path', '清单路径无效')
        found.add(name)
        data = (ROOT / path).read_bytes()
        need(len(data) == entry['bytes'] and sha(data) == entry['sha256'],
             'package file mismatch: ' + name, '包文件不匹配：' + name)
    expected = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
                and p.name != 'MANIFEST.json'
                and not any(part in ('.cache', '__pycache__', '.replay-runs') for part in p.relative_to(ROOT).parts)}
    need(found == expected, 'manifest allowlist differs from package files',
         '清单允许文件与包内文件不一致')


def check_records():
    check_manifest()
    cert_raw, cert = raw_json(CERT)
    py_raw, py = raw_json(PYTHON)
    _, containment = raw_json(ROOT / 'results/R050_INDEPENDENT_CONTAINMENT.json')
    source = json.loads((ROOT / 'SOURCE_PIN.json').read_text(encoding='utf-8'))
    need(sha(cert_raw) == CERT_SHA == source['certificate_sha256'],
         'certificate SHA mismatch', '证书 SHA 不匹配')
    need(sha(py_raw) == PYTHON_SHA == source['python_full_replay_sha256'],
         'Python ledger SHA mismatch', 'Python 账本 SHA 不匹配')
    need(source['secondary_reconstructed_sha256'] == CHECKER_SHA,
         'checker pin mismatch', '检查器来源锁定不匹配')
    for name, expected_sha in source['r043_python_sources']['sha256'].items():
        need(sha((ROOT / 'src' / name).read_bytes()) == expected_sha,
             'R043 source pin mismatch: ' + name,
             'R043 源码锁定不匹配：' + name)
    recipe = json.loads((ROOT / 'src/secondary-adaptation.json').read_text(
        encoding='utf-8'))
    need(recipe['source_sha256'] == source['secondary_checker_source']['sha256']
         and recipe['result_sha256'] == CHECKER_SHA,
         'secondary recipe pin mismatch', '第二检查器配方锁定不匹配')
    need(cert['L'] == '4613/1000' and cert['A'] == '998509/1000000'
         and F(cert['L']) / F(cert['A']) == BOUND and cert['bound'] == str(BOUND),
         'bound identity mismatch', '下界身份不匹配')
    need(cert['budget_units'] == BUDGET and cert['minimum_units'] <= MINIMUM
         and len(cert['entries']) == ROWS,
         'certificate summary mismatch', '证书汇总不匹配')
    need(py['status'] == 'PASS_FULL_EXACT_PYTHON_REPLAY'
         and py['certificate_sha256'] == CERT_SHA
         and py['minimum_units'] == MINIMUM
         and py['budget_units'] == BUDGET
         and py['intervals'] == ROWS
         and F(py['bound']) == BOUND
         and py['counting_surplus_units'] == 17 * MINIMUM - BUDGET == 1524845,
         'Python full replay summary mismatch', 'Python 全量结果汇总不匹配')
    need(containment['status'] == 'PASS_INDEPENDENT_EXACT_CONTROLS'
         and containment['certificate_sha256'] == CERT_SHA
         and containment['containment']['intervals'] == ROWS
         and containment['containment']['quadratic_inequalities'] == 4 * ROWS
         and F(containment['containment']['minimum_positive_quadratic_numerator']) > 0,
         'recorded containment mismatch', '已存包含证明不匹配')
    sys.path.insert(0, str(ROOT / 'src'))
    import independent_controls
    sites, weights, triples, _ = independent_controls.expand(cert)
    need(len(sites) == 8988 and len(triples) == 2008
         and len(cert['point_orbits']) == 1134
         and len(cert['threshold_orbits']) == 253,
         'resource count mismatch', '资源数量不匹配')
    cursor = F(0)
    for row in cert['entries']:
        a, b, t, core = map(F, row)
        need(a == cursor and a < b < 1 and 0 <= t < 1 and 0 < core < F(cert['A']),
             'angular partition mismatch', '角区间划分不匹配')
        cursor = b
    need(cursor * cursor + 2 * cursor > 1,
         'angular coverage gap', '角度覆盖缺口')
    rows = py['rows']
    need(len(rows) == ROWS and [r['row'] for r in rows] == list(range(ROWS)),
         'Python row ledger incomplete', 'Python 行账本不完整')
    charges = [r['minimum_units'] for r in rows]
    histogram = Counter(map(str, charges))
    need(min(charges) == MINIMUM and dict(histogram) == py['histogram']
         and sum(r['slabs'] for r in rows) == py['slabs']
         and sum(r['cells'] for r in rows) == py['cells'],
         'Python row ledger summary mismatch', 'Python 行账本汇总不匹配')
    part_paths = sorted(PARTS.glob('*.json'))
    need(len(part_paths) == 118, 'BigInt part count mismatch', 'BigInt 分块数量不匹配')
    cursor = 0
    full_histogram = Counter()
    block_minima = []
    for path in part_paths:
        _, part = raw_json(path)
        lo, hi = part['range']
        part_hist = Counter({str(k): v for k, v in part['histogram'].items()})
        need(lo == cursor and lo < hi <= ROWS
             and path.name == f'{lo:06d}_{hi:06d}.json'
             and part['status'] == 'PASS_EXACT_MOVABLE_SUPPORT_SCAN'
             and part['certificate_sha256'] == CERT_SHA
             and part['parent_side'] == cert['A']
             and part['measure'] == 'base'
             and part['atoms'] == len(sites)
             and part['thresholds'] == len(triples)
             and part['budget_units'] == BUDGET
             and not part['escape_rows']
             and sum(part_hist.values()) == hi - lo
             and part['minimum_units'] == min(map(int, part_hist))
             and part_hist == Counter(map(str, charges[lo:hi])),
             'BigInt block mismatch: ' + path.name,
             'BigInt 分块不匹配：' + path.name)
        cursor = hi
        full_histogram.update(part_hist)
        block_minima.append(part['minimum_units'])
    need(cursor == ROWS and min(block_minima) == MINIMUM
         and full_histogram == histogram,
         'BigInt full coverage mismatch', 'BigInt 全覆盖不匹配')
    return cert_raw, cert, py, containment


def reserve(path):
    path = path.resolve()
    need(not path.exists(), 'output exists', '输出目录已存在')
    path.mkdir(parents=True)
    return path


def run_containment(out, cert_raw, expected):
    cert_path = out / 'certificate.json'
    cert_path.write_bytes(cert_raw)
    target = out / 'containment.json'
    subprocess.run([sys.executable, '-X', 'utf8', '-B', '-S',
                    str(ROOT / 'src/independent_controls.py'), str(cert_path),
                    '--containment-only', '--output', str(target)], check=True)
    _, result = raw_json(target)
    need(result['certificate_sha256'] == CERT_SHA
         and result['containment'] == expected['containment'],
         'fresh containment mismatch', '新鲜包含复演不匹配')
    return 'PASS_R050_INDEPENDENT_CONTAINMENT'


def run_python(out, cert_raw, frozen, jobs):
    cert_path = out / 'certificate.json'
    cert_path.write_bytes(cert_raw)
    target = out / 'python.json'
    subprocess.run([sys.executable, '-X', 'utf8', '-B',
                    str(ROOT / 'src/replay_parallel.py'), str(cert_path),
                    '--output', str(target), '--jobs', str(jobs)], check=True)
    _, result = raw_json(target)
    for key in ('status', 'certificate_sha256', 'parent_side', 'bound',
                'intervals', 'budget_units', 'minimum_units', 'strict_core_margin',
                'counting_surplus_units', 'slabs', 'cells', 'histogram', 'rows'):
        need(result[key] == frozen[key], 'fresh Python mismatch: ' + key,
             '新鲜 Python 复演不匹配：' + key)
    return 'PASS_R050_PYTHON_COMPLETE_EXACT_REPLAY'


def run_bigint(out, cert_raw, cert, frozen, jobs, source):
    need(shutil.which('node') is not None, 'Node.js executable not found',
         '未找到 Node.js 可执行程序')
    cert_path = out / 'certificate.json'
    cert_path.write_bytes(cert_raw)
    sys.path.insert(0, str(ROOT / 'src'))
    import prepare_secondary
    checker = prepare_secondary.ensure_secondary(source)
    need(sha(checker.read_bytes()) == CHECKER_SHA,
         'reconstructed checker SHA mismatch', '重建检查器 SHA 不匹配')
    jobs = max(1, min(jobs, ROWS))
    spans = [(j * ROWS // jobs, (j + 1) * ROWS // jobs) for j in range(jobs)]

    def one(span):
        lo, hi = span
        proc = subprocess.run(['node', str(checker), '--certificate', str(cert_path),
                               '--expected-sha', CERT_SHA, '--A', cert['A'],
                               '--start', str(lo), '--stop', str(hi)],
                              text=True, capture_output=True, encoding='utf-8', check=True)
        result = json.loads(proc.stdout)
        need(result['range'] == [lo, hi]
             and result['status'] == 'PASS_EXACT_MOVABLE_SUPPORT_SCAN'
             and result['certificate_sha256'] == CERT_SHA
             and result['parent_side'] == cert['A']
             and result['measure'] == 'base'
             and result['atoms'] == 8988
             and result['thresholds'] == 2008
             and result['budget_units'] == BUDGET
             and not result['escape_rows']
             and sum(result['histogram'].values()) == hi - lo
             and result['minimum_units'] == min(map(int, result['histogram']))
             and Counter({str(k): v for k, v in result['histogram'].items()})
                 == Counter(str(row['minimum_units']) for row in frozen['rows'][lo:hi]),
             'fresh BigInt chunk mismatch', '新鲜 BigInt 分块不匹配')
        (out / f'bigint-{lo:06d}-{hi:06d}.json').write_text(
            json.dumps(result, indent=2) + '\n', encoding='utf-8')
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        parts = list(executor.map(one, spans))
    histogram = Counter()
    for part in parts:
        histogram.update({str(k): v for k, v in part['histogram'].items()})
    need(min(p['minimum_units'] for p in parts) == MINIMUM
         and dict(histogram) == frozen['histogram'],
         'fresh BigInt replay mismatch', '新鲜 BigInt 复演不匹配')
    (out / 'bigint.json').write_text(json.dumps({
        'status': 'PASS_R050_BIGINT_COMPLETE_EXACT_REPLAY',
        'certificate_sha256': CERT_SHA, 'range': [0, ROWS],
        'checker_sha256': CHECKER_SHA,
        'minimum_units': MINIMUM, 'histogram': dict(histogram),
        'escape_rows': []}, indent=2) + '\n', encoding='utf-8')
    return 'PASS_R050_BIGINT_COMPLETE_EXACT_REPLAY'


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--containment', action='store_true')
    mode.add_argument('--python-full', action='store_true')
    mode.add_argument('--bigint-full', action='store_true')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--secondary-source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'),
         'optimized Python is not supported', '不支持 Python 优化模式')
    need(args.jobs >= 1, 'jobs must be positive', '并行数必须为正')
    cert_raw, cert, frozen, containment = check_records()
    out = reserve(args.output)
    status = 'PASS_R050_RECORDED_TWO_COMPLETE_EXACT_REPLAYS'
    if args.containment:
        status = run_containment(out, cert_raw, containment)
    elif args.python_full:
        status = run_python(out, cert_raw, frozen, args.jobs)
    elif args.bigint_full:
        status = run_bigint(out, cert_raw, cert, frozen, args.jobs,
                            args.secondary_source)
    result = {'status': status, 'research_id': 'N17-R050',
              'strict_lower_bound': str(BOUND), 'certificate_sha256': CERT_SHA,
              'observed_global_minimum_units': MINIMUM, 'budget_units': BUDGET,
              'counting_surplus_units': 17 * MINIMUM - BUDGET,
              'intervals': ROWS, 'bigint_parts': 118}
    (out / 'RESULT.json').write_text(json.dumps(result, ensure_ascii=False,
                                                indent=2) + '\n', encoding='utf-8')
    print(status)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
