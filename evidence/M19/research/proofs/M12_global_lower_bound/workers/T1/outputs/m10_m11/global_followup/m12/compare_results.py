"""Mechanical exact comparison of the two completed M12 result files."""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
source = json.loads((RESULTS / "source_result.json").read_text(encoding="utf-8"))
scaled = json.loads((RESULTS / "scaled_result.json").read_text(encoding="utf-8"))
certificate = json.loads((ROOT.parent / "certificate.json").read_text(encoding="utf-8"))
limit_num, limit_den = map(int, certificate["angle_limit"].split("/"))
steps = int(certificate["direction_steps"])

rows = []
for index, (left, right) in enumerate(zip(source["per_direction"], scaled["per_direction"], strict=True)):
    numerator = limit_num * index
    denominator = limit_den * steps
    from fractions import Fraction

    tangent = str(Fraction(numerator, denominator))
    rows.append(
        {
            "index": index,
            "half_tangent": tangent,
            "source_label": left["label"],
            "source_minimum": left["minimum_cell_mass"],
            "scaled_label": right["label"],
            "scaled_minimum": right["minimum_cell_mass"],
            "equal": left == right,
        }
    )

jsonl = RESULTS / "DIRECTIONS_COMPARISON.jsonl"
jsonl.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
summary = {
    "schema_version": "n17.m12.exact-comparison.v1",
    "direction_count": len(rows),
    "all_equal": all(row["equal"] for row in rows),
    "mismatch_indices": [row["index"] for row in rows if not row["equal"]],
    "source_accepted": source["certificate"]["accepted"],
    "scaled_accepted": scaled["certificate"]["accepted"],
    "source_minimum": source["certificate"]["minimum_cell_mass"],
    "scaled_minimum": scaled["certificate"]["minimum_cell_mass"],
    "source_worst_direction": source["certificate"]["worst_direction"],
    "scaled_worst_direction": scaled["certificate"]["worst_direction"],
    "source_result_sha256": hashlib.sha256((RESULTS / "source_result.json").read_bytes()).hexdigest(),
    "scaled_result_sha256": hashlib.sha256((RESULTS / "scaled_result.json").read_bytes()).hexdigest(),
    "directions_jsonl_sha256": hashlib.sha256(jsonl.read_bytes()).hexdigest(),
}
(RESULTS / "COMPARISON.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(summary, sort_keys=True))
