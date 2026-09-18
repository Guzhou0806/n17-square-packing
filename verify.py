#!/usr/bin/env python3
"""Reproduce the supplied M19 result, including all inherited M12 directions.

Default: full standard-library replay. --quick: no coverage sweeps.
This is a release adapter; frozen mathematical programs are not modified.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent
M19_REL = "evidence/M19"
M12_REL = M19_REL + "/research/proofs/M12_global_lower_bound"
EVIDENCE_MANIFEST_SHA256 = "2caaea2ce5c690e471edb199089585b8ca783cae3e038f36600f22bd8d4cb935"


class VerificationError(ValueError):
    """An integrity, scope, or result check failed."""


def require(ok: bool, message: str) -> None:
    if not ok:
        raise VerificationError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def read_json(path: Path):
    def bad_constant(value):
        raise VerificationError(f"Non-finite JSON constant: {value}")
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object, parse_constant=bad_constant)


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line, object_pairs_hook=unique_object)
            for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def safe_file(base: Path, relative: str) -> Path:
    require(isinstance(relative, str) and bool(relative), "Empty/non-string path")
    rel = PurePosixPath(relative)
    require(not rel.is_absolute() and ".." not in rel.parts and
            "\\" not in relative and ":" not in relative,
            f"Unsafe manifest path: {relative}")
    path = base.joinpath(*rel.parts)
    require(not any(p.is_symlink() for p in [path, *path.parents]
                    if p == base or base in p.parents), f"Symlink refused: {relative}")
    require(path.is_file(), f"Missing file: {relative}")
    require(path.resolve().is_relative_to(base.resolve()), f"Path escaped root: {relative}")
    return path


def check_file_map(base: Path, entries: dict) -> int:
    require(isinstance(entries, dict) and bool(entries), "Empty file map")
    for name, record in entries.items():
        path = safe_file(base, name)
        require(type(record.get("bytes")) is int and record["bytes"] >= 0,
                f"Invalid byte length: {name}")
        require(path.stat().st_size == record["bytes"], f"Byte length mismatch: {name}")
        require(sha256(path) == record["sha256"], f"SHA-256 mismatch: {name}")
    return len(entries)


def preflight(root: Path = ROOT) -> dict:
    require(sys.version_info >= (3, 10), "Python 3.10 or newer is required")
    require(sys.flags.optimize == 0,
            "Do not use -O/-OO or PYTHONOPTIMIZE: frozen programs use assert checks")
    path = root / "EVIDENCE_MANIFEST.json"
    require(sha256(path) == EVIDENCE_MANIFEST_SHA256,
            "Frozen evidence manifest changed; do not silently update the hash")
    manifest = read_json(path)
    count = check_file_map(root, manifest["files"])
    expected_files = set(manifest["files"])
    actual_files = {p.relative_to(root).as_posix()
                    for name in ("evidence", "archives")
                    for p in (root / name).rglob("*") if p.is_file()}
    require(actual_files == expected_files, "Unexpected/missing files in frozen evidence")
    inherited_counts = {}
    for rel in (M19_REL, M12_REL):
        base = root / rel
        old_manifest = read_json(base / "MANIFEST.json")
        inherited_counts[rel] = check_file_map(base, old_manifest["files"])
    acceptance = read_json(root / M19_REL / "FINAL_ACCEPTANCE.json")
    claim = acceptance["claim"]
    require(acceptance["status"] == "PASS_CERTIFIED_NEW_GLOBAL_LOWER_BOUND",
            "Unexpected project acceptance status")
    cert_path = safe_file(root / M19_REL, claim["certificate"])
    audit_path = safe_file(root / M19_REL, claim["independent_audit"])
    require(sha256(cert_path) == claim["certificate_sha256"], "Acceptance/certificate mismatch")
    require(sha256(audit_path) == claim["independent_audit_sha256"], "Acceptance/audit mismatch")
    cert = read_json(cert_path)
    require(claim["side_square"] == cert["side_square"] and
            claim["decimal_bracket_20"] == cert["decimal_bracket_20"],
            "Acceptance endpoint differs from certificate")
    require(claim["endpoint_certificate"] is False and
            cert["claims_strict_endpoint_infeasibility"] is False,
            "Claim has been upgraded to endpoint infeasibility")
    require(claim["external_priority"] == "NOT_ESTABLISHED" and claim["method_novelty"] is False,
            "Unexpected priority/novelty statement")
    return {"status": "PASS", "frozen_files_checked": count,
            "original_manifest_entries_checked": inherited_counts,
            "acceptance_certificate_and_audit_bound": True,
            "evidence_manifest_sha256": EVIDENCE_MANIFEST_SHA256}


def reserve_output(path: Path, root: Path = ROOT) -> Path:
    out = path.resolve()
    for name in ("evidence", "archives", "verification", "provenance", "docs"):
        protected = (root / name).resolve()
        require(out != protected and not out.is_relative_to(protected),
                f"Refusing output inside protected directory: {name}")
    require(not out.exists(), f"Output already exists: {out}; choose a NEW directory")
    out.mkdir(parents=True, exist_ok=False)
    return out


def execute(script: Path, args: list[str], out: Path, label: str,
            seconds: int = 750, standard_library: bool = True) -> dict:
    command = [sys.executable, "-X", "utf8", "-B"]
    if standard_library:
        command.append("-S")
    command.extend([str(script), *args])
    env = os.environ.copy()
    env.update(PYTHONOPTIMIZE="0", PYTHONDONTWRITEBYTECODE="1",
               PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    started = time.perf_counter()
    logfile = out / f"{label}.log"
    print(f"Running {label} ...", flush=True)
    with logfile.open("x", encoding="utf-8", newline="\n") as stream:
        proc = subprocess.run(command, cwd=str(ROOT), env=env, stdout=stream,
                              stderr=subprocess.STDOUT, timeout=seconds, check=False)
    elapsed = time.perf_counter() - started
    if proc.returncode:
        print(logfile.read_text(encoding="utf-8", errors="replace")[-6000:])
    require(proc.returncode == 0, f"{label} failed, exit {proc.returncode}; see {logfile}")
    print(f"PASS {label} ({elapsed:.2f} seconds)", flush=True)
    return {"label": label, "script": script.relative_to(ROOT).as_posix(),
            "script_sha256": sha256(script), "returncode": proc.returncode,
            "seconds": elapsed, "log": logfile.name, "standard_library_mode": standard_library}


def check_full_outputs(out: Path, root: Path = ROOT) -> dict:
    base = root / M19_REL
    old = read_rows(out / "M12/coverage/DIRECTIONS.jsonl")
    new = read_rows(out / "M19/new_coverage/DIRECTIONS.jsonl")
    saved_old = read_rows(base / "research/m12_work/run_001/DIRECTIONS.jsonl")
    saved_new = read_rows(base / "research/m17_work/run_001/DIRECTIONS.jsonl")
    require(old == saved_old and new == saved_new, "Fresh full-direction rows differ from archive")
    require(len(old) == 181 and len(new) == 17, "Incomplete coverage replay")
    threshold = Fraction(423327, 425000)
    passed = [r for r in new if Fraction(r["minimum"]) > threshold]
    failed = [r for r in new if Fraction(r["minimum"]) <= threshold]
    require(len(passed) == 16 and len(failed) == 1 and failed[0]["refined_index"] == 29,
            "M17 failure / M19 retained subset changed")
    require(Fraction(failed[0]["minimum"]) == Fraction(197153, 200000), "Wrong failed mass")
    require(min(Fraction(r["minimum"]) for r in old + passed) == Fraction(200009, 200000),
            "Wrong retained coverage guarantee")
    require(len({Fraction(r["t"]) for r in old + passed}) == 197, "Merged net not 197")
    require(read_json(out / "M12/REPLAY.json")["status"] == "PASS", "M12 replay did not pass")
    require(read_json(out / "M19/REPLAY.json")["status"] == "PASS", "M19 replay did not pass")
    acceptance = read_json(base / "FINAL_ACCEPTANCE.json")
    require(sha256(out / "M19/M19_AUDIT.json") == acceptance["claim"]["independent_audit_sha256"],
            "Fresh M19 audit bytes differ from accepted audit")
    return {"old_directions_recomputed": 181, "additional_directions_recomputed": 17,
            "unique_coverage_directions_recomputed": 198, "retained_certified_directions": 197,
            "retained_counterexamples": 1, "failed_refined_index": 29,
            "failed_mass": "197153/200000", "retained_minimum": "200009/200000",
            "old_minimum_counts": dict(Counter(r["minimum"] for r in old)),
            "fresh_M19_audit_matches_accepted_bytes": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Integrity + saved-evidence audit ONLY; no coverage sweep")
    parser.add_argument("--output", type=Path, help="New output directory (never overwritten)")
    args = parser.parse_args()
    report = {"schema": "n17.release.replay.v1", "status": "RUNNING",
              "mode": "quick" if args.quick else "full", "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "python": sys.version, "platform": platform.platform(),
              "driver_sha256": sha256(Path(__file__)), "stages": [],
              "trust_scope": "Re-execution of supplied exact programs; not a newly authored geometric verifier, proof-assistant formalization, or peer review.",
              "upstream_numpy_sweep_reexecuted_in_this_run": False,
              "packing_optimization_calls": 0}
    out = None
    start = time.perf_counter()
    try:
        report["integrity"] = preflight()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = reserve_output(args.output or (ROOT / ".replay-runs" / (stamp + "-" + uuid.uuid4().hex[:8])))
        base = ROOT / M19_REL
        if args.quick:
            report["stages"].append(execute(base / "workers/T2/outputs/m17_lower/check_m19.py",
                ["--root", str(base), "--report", str(out / "M19_AUDIT.json")], out, "saved_evidence_audit"))
            require(read_json(out / "M19_AUDIT.json")["status"] == "PASS_M19_NONUNIFORM_GRID_LOWER_BOUND",
                    "Quick audit did not pass")
            report["status"] = "PASS_QUICK_CHECK_ONLY"
            report["coverage_sweeps_performed"] = 0
        else:
            report["stages"].append(execute(ROOT / M12_REL / "replay.py",
                ["--output", str(out / "M12")], out, "M12_full_181"))
            report["stages"].append(execute(base / "replay.py",
                ["--output", str(out / "M19")], out, "M19_full_17_and_endpoint"))
            report["coverage"] = check_full_outputs(out)
            report["status"] = "PASS_FULL_REPLAY"
        report["integrity_after_replay"] = preflight()
        claim = read_json(base / "FINAL_ACCEPTANCE.json")["claim"]
        report["claim"] = {key: claim[key] for key in ("statement", "side_square", "decimal_bracket_20", "endpoint_certificate", "external_priority")}
        code = 0
    except (VerificationError, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        report["status"] = "FAIL_OR_INCOMPLETE"
        report["error"] = f"{type(error).__name__}: {error}"
        print(report["error"], file=sys.stderr)
        code = 1
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    report["seconds"] = time.perf_counter() - start
    if out is not None:
        (out / "RESULT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "report": str(out / "RESULT.json") if out else None,
                      "seconds": report["seconds"]}, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
