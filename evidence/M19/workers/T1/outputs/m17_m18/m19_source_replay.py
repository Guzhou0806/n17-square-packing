"""Replay exactly the 17 M17 rows with the locked upstream NumPy sweep.

Prepared for M19 review; do not run without a separate M19 authorization.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SOURCE_ROOT = ROOT / "workers/T1/outputs/m10_m11/global_followup/m12/source/src"
CERTIFICATE = ROOT / "workers/T1/outputs/m10_m11/global_followup/certificate.json"
M17_ROWS = ROOT / "research/m17_work/run_001/DIRECTIONS.jsonl"
AUTHORIZATION = ROOT / "coord/m17_m18/M19_COMPUTE_AUTHORIZATION.json"
SWEEP_SOURCE = SOURCE_ROOT / "sqpack/fractional/sweep.py"
MODEL_SOURCE = SOURCE_ROOT / "sqpack/fractional/model.py"
OUTPUT = Path(__file__).with_name("m19_replay")

CERTIFICATE_SHA256 = "461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652"
M17_ROWS_SHA256 = "c4898a550541964260091bdf6a79a9483832d412cbfa5a8d734de2fe0fc62b77"
SWEEP_SHA256 = "b6b5f016a8d6ab632e0ea8ee30effa75d4bf11ca9acece72e2e933048b5714ee"
MODEL_SHA256 = "2ef606e89a77f703041e5397d6f34ebb76289adfd2876c80abae868b081b6696"
EXPECTED_ORDER = [0, 89, 179, *range(1, 15)]
MAX_ROWS = 17
SOFT_SECONDS = 30.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def covered_mass(atoms, direction, square_side: F, centre: tuple[F, F]) -> F:
    """Direct exact count at the source sweep's returned (u, v) witness."""

    half = square_side / 2
    cu, cv = centre
    total = F(0)
    for atom in atoms:
        u = direction.ux * atom.x + direction.uy * atom.y
        v = direction.vx * atom.x + direction.vy * atom.y
        if abs(u - cu) <= half and abs(v - cv) <= half:
            total += atom.weight
    return total


def main() -> None:
    if not AUTHORIZATION.exists():
        raise ValueError("M19 execution is not authorized")
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    if authorization.get("status") != "AUTHORIZED":
        raise ValueError("M19 execution authorization is not active")

    bindings = {
        CERTIFICATE: CERTIFICATE_SHA256,
        M17_ROWS: M17_ROWS_SHA256,
        SWEEP_SOURCE: SWEEP_SHA256,
        MODEL_SOURCE: MODEL_SHA256,
    }
    for path, expected in bindings.items():
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"frozen input drift: {path}: {actual} != {expected}")

    if OUTPUT.exists():
        raise FileExistsError(f"refusing to overwrite {OUTPUT}")

    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    expected_rows = [json.loads(line) for line in M17_ROWS.read_text(encoding="utf-8").splitlines()]
    order = [int(row["old_interval_index"]) for row in expected_rows]
    if len(expected_rows) != MAX_ROWS or order != EXPECTED_ORDER:
        raise ValueError(f"M17 row scope changed: {order}")

    sys.path.insert(0, str(SOURCE_ROOT))
    import numpy as np
    from sqpack.fractional.model import Atom, rotation_from_half_tangent
    from sqpack.fractional.sweep import minimum_covered_mass_integer, weight_scale

    outer_side = F(record["outer_side"])
    square_side = F(record["square_side"])
    threshold = F(record["total_mass"]) / 17
    atoms = tuple(
        Atom(f"{index:03d}", F(x), F(y), F(weight))
        for index, (x, y, weight) in enumerate(record["atoms"])
    )
    scale = weight_scale(atoms)

    OUTPUT.mkdir(parents=False, exist_ok=False)
    output_rows: list[dict[str, object]] = []
    started = time.perf_counter()
    status = "PASS_EXACT_MATCH_17"
    with (OUTPUT / "ROWS.jsonl").open("x", encoding="utf-8") as stream:
        for row_number, expected in enumerate(expected_rows, start=1):
            if time.perf_counter() - started > SOFT_SECONDS:
                status = "BUDGET_EXHAUSTED"
                break
            tangent = F(expected["t"])
            direction = rotation_from_half_tangent(str(expected["refined_index"]), tangent)
            minimum, centre = minimum_covered_mass_integer(
                atoms, direction, outer_side, square_side, scale
            )
            direct = covered_mass(atoms, direction, square_side, centre)
            expected_minimum = F(expected["minimum"])
            result = {
                "row_number": row_number,
                "old_interval_index": int(expected["old_interval_index"]),
                "refined_index": int(expected["refined_index"]),
                "t": str(tangent),
                "expected_minimum": str(expected_minimum),
                "source_minimum": str(minimum),
                "minimum_matches": minimum == expected_minimum,
                "source_classification": "PASS" if minimum > threshold else "FAIL",
                "expected_classification": "PASS" if expected_minimum > threshold else "FAIL",
                "centre_uv": [str(centre[0]), str(centre[1])],
                "direct_witness_mass": str(direct),
                "direct_witness_matches": direct == minimum,
            }
            output_rows.append(result)
            stream.write(json.dumps(result, sort_keys=True) + "\n")
            stream.flush()
            if not result["minimum_matches"] or not result["direct_witness_matches"]:
                status = "FAIL_SOURCE_MISMATCH"

    elapsed = time.perf_counter() - started
    if status == "PASS_EXACT_MATCH_17" and len(output_rows) != MAX_ROWS:
        status = "BUDGET_EXHAUSTED"
    summary = {
        "status": status,
        "scope": "exactly the 17 rows already produced by M17; no unswept direction",
        "completed": len(output_rows),
        "expected": MAX_ROWS,
        "threshold": str(threshold),
        "passing_rows": sum(row["source_classification"] == "PASS" for row in output_rows),
        "failing_rows": sum(row["source_classification"] == "FAIL" for row in output_rows),
        "seconds": elapsed,
        "soft_seconds": SOFT_SECONDS,
        "numpy_version": np.__version__,
        "weight_scale": scale,
        "authorization_sha256": sha256(AUTHORIZATION),
        "bindings": {str(path.relative_to(ROOT)): expected for path, expected in bindings.items()},
    }
    (OUTPUT / "RESULT.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
