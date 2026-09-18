"""Frozen M12 harness: record one source verifier sweep without changing its values."""

from __future__ import annotations

import ctypes
import hashlib
import importlib
import json
import os
from fractions import Fraction
from pathlib import Path
import platform
import sys
import time
import types


ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = ROOT / "source" / "src"
CERT_PATH = ROOT.parent / "certificate.json"
RESULTS = ROOT / "results"
LAMBDA = Fraction(1000001, 1000000)
COMMIT = "035d84c655b4047bc9986c9a3db5106780d92f77"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install_namespace(name: str, path: Path) -> None:
    module = types.ModuleType(name)
    module.__path__ = [str(path)]
    module.__package__ = name
    sys.modules[name] = module


def peak_working_set() -> int | None:
    if os.name != "nt":
        return None

    class Counters(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong),
            ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    ok = ctypes.windll.psapi.GetProcessMemoryInfo(
        ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(counters), counters.cb
    )
    return int(counters.PeakWorkingSetSize) if ok else None


def fraction_record(value: Fraction) -> str:
    return str(value)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"source", "scaled"}:
        raise SystemExit("usage: run_replay.py source|scaled")
    mode = sys.argv[1]

    install_namespace("sqpack", SOURCE_ROOT / "sqpack")
    install_namespace("sqpack.fractional", SOURCE_ROOT / "sqpack" / "fractional")
    model = importlib.import_module("sqpack.fractional.model")
    certificate_module = importlib.import_module("sqpack.fractional.certificate")
    import numpy as np

    record = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    limit = Fraction(record["angle_limit"])
    steps = int(record["direction_steps"])
    atoms = tuple(
        model.Atom(f"{index:03d}", Fraction(x), Fraction(y), Fraction(weight))
        for index, (x, y, weight) in enumerate(record["atoms"])
    )
    outer_side = Fraction(record["outer_side"])
    square_side = Fraction(record["square_side"])
    if mode == "scaled":
        atoms = tuple(
            model.Atom(atom.label, LAMBDA * atom.x, LAMBDA * atom.y, atom.weight)
            for atom in atoms
        )
        outer_side *= LAMBDA
        square_side *= LAMBDA
    certificate = certificate_module.Certificate(
        n=int(record["n"]),
        outer_side=outer_side,
        square_side=square_side,
        atoms=atoms,
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        symmetry=record["symmetry"],
    )

    captured: dict[str, tuple[tuple[Fraction, str], ...]] = {}
    original_sweep = certificate_module.sweep_all_directions

    def recording_sweep(cert, *, workers=None):
        values = original_sweep(cert, workers=workers)
        captured["values"] = values
        return values

    certificate_module.sweep_all_directions = recording_sweep
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    try:
        verdict = certificate_module.verify(certificate, workers=1)
    finally:
        certificate_module.sweep_all_directions = original_sweep
    wall_seconds = time.perf_counter() - wall_start
    cpu_seconds = time.process_time() - cpu_start
    per_direction = captured["values"]

    output = {
        "schema_version": "n17.m12.source-faithful-replay.v1",
        "mode": mode,
        "commit": COMMIT,
        "lambda": str(LAMBDA) if mode == "scaled" else "1",
        "input": {
            "certificate_path": str(CERT_PATH),
            "certificate_sha256": sha256(CERT_PATH),
            "certificate_module_sha256": sha256(
                SOURCE_ROOT / "sqpack" / "fractional" / "certificate.py"
            ),
            "model_module_sha256": sha256(SOURCE_ROOT / "sqpack" / "fractional" / "model.py"),
            "sweep_module_sha256": sha256(SOURCE_ROOT / "sqpack" / "fractional" / "sweep.py"),
            "workers_module_sha256": sha256(SOURCE_ROOT / "sqpack" / "workers.py"),
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "workers": 1,
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
            "namespace_shim": True,
            "project_requires_python": ">=3.14,<3.15",
        },
        "certificate": {
            "n": certificate.n,
            "outer_side": fraction_record(certificate.outer_side),
            "square_side": fraction_record(certificate.square_side),
            "atom_count": len(certificate.atoms),
            "direction_count": len(certificate.half_tangents),
            "total_mass": fraction_record(verdict.total_mass),
            "minimum_cell_mass": fraction_record(verdict.minimum_cell_mass),
            "worst_direction": verdict.worst_direction,
            "accepted": verdict.accepted,
        },
        "conditions": [
            {"name": item.name, "detail": item.detail, "holds": item.holds}
            for item in verdict.conditions
        ],
        "per_direction": [
            {"label": label, "minimum_cell_mass": fraction_record(minimum)}
            for minimum, label in per_direction
        ],
        "timing": {
            "wall_seconds": wall_seconds,
            "cpu_seconds": cpu_seconds,
            "peak_working_set_bytes": peak_working_set(),
        },
    }

    RESULTS.mkdir(parents=True, exist_ok=True)
    if mode == "scaled":
        scaled_record = dict(record)
        scaled_record["id"] = record["id"] + "-scaled-1000001-1000000"
        scaled_record["claim"] = "conditional candidate s(17) >= 459000459/100000000"
        scaled_record["outer_side"] = str(certificate.outer_side)
        scaled_record["square_side"] = str(certificate.square_side)
        scaled_record["atoms"] = [
            [str(atom.x), str(atom.y), str(atom.weight)] for atom in certificate.atoms
        ]
        scaled_path = RESULTS / "scaled_certificate.json"
        scaled_path.write_text(
            json.dumps(scaled_record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        output["scaled_certificate_sha256"] = sha256(scaled_path)

    out_path = RESULTS / f"{mode}_result.json"
    out_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "mode": mode,
                "accepted": verdict.accepted,
                "direction_count": len(per_direction),
                "minimum_cell_mass": str(verdict.minimum_cell_mass),
                "worst_direction": verdict.worst_direction,
                "wall_seconds": wall_seconds,
                "cpu_seconds": cpu_seconds,
                "peak_working_set_bytes": output["timing"]["peak_working_set_bytes"],
                "result": str(out_path),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
