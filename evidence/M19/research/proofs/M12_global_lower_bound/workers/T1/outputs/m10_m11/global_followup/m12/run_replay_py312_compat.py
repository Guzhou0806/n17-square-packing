"""Single authorized compatibility shim for Python 3.12, then run frozen harness."""

from __future__ import annotations

import os
from pathlib import Path
import runpy


if hasattr(os, "process_cpu_count"):
    raise SystemExit("compatibility wrapper refused: os.process_cpu_count already exists")

# Python 3.13 added process_cpu_count. The locked source uses it only to cap a
# worker pool. M12 passes workers=1, so this value cannot change geometry,
# weights, direction order, or arithmetic; min(..., workers=1, ...) stays 1.
os.process_cpu_count = os.cpu_count  # type: ignore[attr-defined]

runpy.run_path(str(Path(__file__).with_name("run_replay.py")), run_name="__main__")

