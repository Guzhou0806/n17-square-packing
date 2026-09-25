#!/usr/bin/env python3
"""Build and replay the exact C++ backend / 构建并完整复演精确C++后端。"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
import verify

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from native_exact import NativeModel


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    verify.need(__debug__,'Python -O is not a verification mode')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--jobs',type=int,default=4)
    ap.add_argument('--compiler',default='g++')
    ap.add_argument('--boost-include',type=Path)
    args=ap.parse_args()
    verify.need(1<=args.jobs<=12,'Jobs outside 1..12')
    verify.need(sys.platform in ('win32','linux'),'Supported build platforms are Windows MinGW and Linux')
    out=args.output.resolve()
    verify.need(not out.exists() and out!=ROOT and ROOT not in out.parents,'Output must be new and outside package')
    compiler=shutil.which(args.compiler)
    verify.need(compiler is not None,'C++17 g++ compiler not found')
    before=time.monotonic()
    manifest,raw,cert,expected=verify.records()
    structure=verify.containment(cert)
    source=ROOT/'src/native_exact.cpp'
    source_sha=digest(source)
    compiler_sha=digest(compiler)
    compiler_version=subprocess.check_output([compiler,'--version'],text=True)
    out.mkdir(parents=True)
    library=out/('native_exact.dll' if sys.platform=='win32' else 'native_exact.so')
    command=[compiler,'-O3','-std=c++17','-shared']+(['-static'] if sys.platform=='win32' else ['-fPIC'])
    if args.boost_include is not None:
        command+=['-I',str(args.boost_include.resolve())]
    command += [str(source),'-o',str(library)]
    proc=subprocess.run(command,capture_output=True,text=True)
    (out/'BUILD_LOG.txt').write_text(proc.stdout+proc.stderr,encoding='utf-8')
    verify.need(proc.returncode==0,'C++ build failed; inspect BUILD_LOG.txt')
    verify.need(digest(source)==source_sha and digest(compiler)==compiler_sha,'Build source/compiler changed')
    library_sha=digest(library)
    build_seconds=time.monotonic()-before
    inp=dict(mode='native-full',manifest_sha256=manifest,candidate_sha256=verify.CERT_SHA,
        verifier_sha256=digest(Path(__file__)),shared_verifier_sha256=digest(ROOT/'verify.py'),
        python=sys.version,platform=platform.platform(),jobs=args.jobs,compiler_version=compiler_version,
        compiler_sha256=compiler_sha,source_sha256=source_sha,library_sha256=library_sha,command=command)
    verify.write(out/'INPUT.json',inp)
    rows=[];scan_start=time.monotonic()
    with NativeModel(library,cert) as model:
        def run(row):
            r,_=model.row(row)
            return {k:r[k] for k in ('row','minimum_units','cells','slabs')}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            for row in pool.map(run,range(verify.N)):
                verify.need(row['row']==len(rows) and row['minimum_units']==expected[row['row']]['minimum_units'],'Fresh native minimum mismatch')
                rows.append(row)
                if len(rows)%512==0:
                    print(json.dumps(dict(mode='native-full',completed_rows=len(rows),total_rows=verify.N)),flush=True)
        mass=model.mass
    scan_seconds=time.monotonic()-scan_start
    verify.need([r['row'] for r in rows]==list(range(verify.N)),'Incomplete native coverage')
    verify.need(min(r['minimum_units'] for r in rows)==verify.MINIMUM,'Native minimum mismatch')
    verify.need(digest(library)==library_sha and digest(source)==source_sha,'Native library/source changed')
    verify.need(verify.check_manifest()==manifest,'Package changed during native verification')
    verify.write(out/'ROWS.json',rows)
    result=dict(status='PASS_R052_NATIVE_FULL',mode='native-full',bound='462003/100000',
        candidate_sha256=verify.CERT_SHA,manifest_sha256=manifest,checked_rows=verify.N,archived_rows=verify.N,
        minimum_units=verify.MINIMUM,budget_units=verify.BUDGET,strict_surplus_units=17*verify.MINIMUM-verify.BUDGET,
        structure=structure,source_sha256=source_sha,library_sha256=library_sha,absolute_term_mass=mass,
        build_and_structure_seconds=build_seconds,scan_seconds=scan_seconds,seconds=time.monotonic()-before,
        scope='全部行重新计算并与独立BigInt账本精确对账。 / Every row is freshly recomputed and exactly compared with the independent BigInt ledger.')
    verify.write(out/'RESULT.json',result)
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
