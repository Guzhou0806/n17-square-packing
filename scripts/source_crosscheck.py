#!/usr/bin/env python3
"""Optional fresh cross-check with retained upstream NumPy sweep.

Only the import/output harness is new. The frozen model.py and sweep.py are
loaded unchanged. This run does not reproduce the historical NumPy binary.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import importlib
import json
from pathlib import Path
import platform
import sys
import time
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify


def namespace(name: str, path: Path) -> None:
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    module.__package__ = name
    sys.modules[name] = module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = None
    start = time.perf_counter()
    report = {"schema": "n17.release.source-crosscheck.v1", "status": "RUNNING",
              "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "python": sys.version, "platform": platform.platform(),
              "adapter_sha256": verify.sha256(Path(__file__)),
              "scope": "Fresh retained-source NumPy sweep on 181 old + 17 M17 directions; not a recreation of historical NumPy 2.5.3."}
    try:
        report["integrity"] = verify.preflight()
        out = verify.reserve_output(args.output)
        base = ROOT / verify.M19_REL
        src = base / "workers/T1/outputs/m10_m11/global_followup/m12/source/src"
        namespace("sqpack", src / "sqpack")
        namespace("sqpack.fractional", src / "sqpack/fractional")
        np = importlib.import_module("numpy")
        model = importlib.import_module("sqpack.fractional.model")
        sweep = importlib.import_module("sqpack.fractional.sweep")
        report["numpy_version"] = np.__version__
        report["frozen_model_sha256"] = verify.sha256(Path(model.__file__))
        report["frozen_sweep_sha256"] = verify.sha256(Path(sweep.__file__))
        record = verify.read_json(base / "workers/T1/outputs/m10_m11/global_followup/certificate.json")
        atoms = tuple(model.Atom(str(i), F(x), F(y), F(w)) for i, (x, y, w) in enumerate(record["atoms"]))
        S, B = F(record["outer_side"]), F(record["square_side"])
        threshold = F(record["total_mass"]) / 17
        scale = sweep.weight_scale(atoms)
        old = verify.read_rows(base / "research/m12_work/run_001/DIRECTIONS.jsonl")
        new = verify.read_rows(base / "research/m17_work/run_001/DIRECTIONS.jsonl")
        expected = [("old", r) for r in old] + [("M17", r) for r in new]
        verify.require(len(expected) == 198, "Unexpected row count")
        rows = []
        with (out / "DIRECTIONS.jsonl").open("x", encoding="utf-8", newline="\n") as stream:
            for i, (family, row) in enumerate(expected):
                t = F(row["t"])
                direction = model.rotation_from_half_tangent(str(i), t)
                minimum, centre = sweep.minimum_covered_mass_integer(atoms, direction, S, B, scale)
                cu, cv = centre
                x0 = direction.ux * cu + direction.vx * cv
                y0 = direction.uy * cu + direction.vy * cv
                radius = B * (abs(direction.ux) + abs(direction.uy)) / 2
                legal = radius <= x0 <= S-radius and radius <= y0 <= S-radius
                covered = [atom for atom in atoms
                           if abs(direction.ux*atom.x + direction.uy*atom.y-cu) <= B/2
                           and abs(direction.vx*atom.x + direction.vy*atom.y-cv) <= B/2]
                direct = sum((a.weight for a in covered), F(0))
                verify.require(legal and direct == minimum == F(row["minimum"]),
                               f"Source/direct/saved mismatch at direction {i}")
                item = {"row_number": i, "family": family, "t": str(t),
                        "minimum": str(minimum), "expected_minimum": row["minimum"],
                        "centre_uv": list(map(str, centre)), "centre_xy": [str(x0), str(y0)],
                        "legal": legal, "direct_mass": str(direct), "captured_atoms": len(covered),
                        "passes_threshold": minimum > threshold}
                rows.append(item)
                stream.write(json.dumps(item, sort_keys=True) + "\n"); stream.flush()
                if i % 30 == 0 or i == 197:
                    print(f"source {i+1}/198: {minimum}", flush=True)
        failed = [r for r in rows if not r["passes_threshold"]]
        verify.require(len(failed) == 1 and failed[0]["family"] == "M17"
                       and failed[0]["minimum"] == "197153/200000"
                       and failed[0]["captured_atoms"] == 125, "Failure witness changed")
        report.update(status="PASS_SOURCE_CROSSCHECK_198", completed=198,
                      certified_net_nodes=197, retained_failure_witnesses=1,
                      all_exact_minima_match=True, exact_direct_witness_checks=198,
                      failed_captured_atoms=125, weight_scale=scale)
        report["integrity_after_replay"] = verify.preflight()
        code = 0
    except (verify.VerificationError, ImportError, OSError, ValueError, KeyError, TypeError) as error:
        report["status"] = "FAIL_OR_INCOMPLETE"
        report["error"] = f"{type(error).__name__}: {error}"
        print(report["error"], file=sys.stderr)
        code = 1
    report["seconds"] = time.perf_counter()-start
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    if out:
        (out / "RESULT.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "seconds": report["seconds"]}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
