"""Directed exact checks for the M17 counterexample and M19 static grid."""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "M17_M19_DIRECTED_TESTS.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise AssertionError(f"refusing to overwrite {OUTPUT}")
    source = json.loads((ROOT / "coord/m14_m15/inputs/SOURCE_T019.json").read_text())
    rows = [json.loads(line) for line in
            (ROOT / "research/m17_work/run_001/DIRECTIONS.jsonl").read_text().splitlines()]
    audit = json.loads((BASE / "M17_FAILURE_AUDIT_ATTEMPT_002.json").read_text())
    precheck = json.loads((BASE / "M19_STATIC_PRECHECK_ATTEMPT_002.json").read_text())
    outcomes = []

    fail = rows[-1]
    t = F(fail["t"])
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    x0, y0 = map(F, fail["centre_xy"])
    B, L = F(source["square_side"]), F(source["outer_side"])
    corners = [(x0 + B * (e * c - f * s) / 2,
                y0 + B * (e * s + f * c) / 2)
               for e in (-1, 1) for f in (-1, 1)]
    assert all(0 < x < L and 0 < y < L for x, y in corners)
    outcomes.append({"test": "all_four_failing_probe_corners_strictly_inside", "status": "PASS"})

    mass = F(0)
    captured = []
    for index, (x, y, weight) in enumerate(source["atoms"]):
        dx, dy = F(x) - x0, F(y) - y0
        if abs(c * dx + s * dy) <= B / 2 and abs(-s * dx + c * dy) <= B / 2:
            mass += F(weight)
            captured.append(index)
    assert mass == F(197153, 200000)
    assert captured == [row["atom_index"] for row in audit["counterexample"]["captured_atoms"]]
    outcomes.append({"test": "alternate_xy_relative_atom_recount", "status": "PASS",
                     "captured_atoms": len(captured)})

    threshold = F(source["total_mass"]) / 17
    assert mass - threshold == F(-7003, 680000)
    assert 17 * mass - F(source["total_mass"]) == F(-7003, 40000)
    outcomes.append({"test": "exact_threshold_deficit", "status": "PASS"})

    passed = sorted(row["old_interval_index"] for row in rows[:-1])
    assert passed == list(range(14)) + [89, 179]
    assert rows[-1]["old_interval_index"] == 14
    outcomes.append({"test": "m17_failure_preserved_and_m19_passed_set_fixed", "status": "PASS"})

    h = F(207107, 90000000)
    nodes = sorted(set([k * h for k in range(181)] +
                       [(2 * k + 1) * h / 2 for k in passed]))
    gaps = [(right - left) / (1 + left * right)
            for left, right in zip(nodes, nodes[1:])]
    maximum = max(gaps)
    assert len(nodes) == 197 and len(gaps) == 196
    assert maximum == h / (1 + F(210) * h * h) == F(precheck["grid"]["D"])
    assert gaps.index(maximum) == 28 and nodes[28] == 14 * h and nodes[29] == 15 * h
    outcomes.append({"test": "all_196_m19_gaps_and_unique_maximum", "status": "PASS"})

    assert precheck["status"] == "GO_PENDING_T1_INDEPENDENT_17_ROW_FULL_REPLAY"
    assert precheck["coverage_evidence_status"][
        "direct_minimum_witnesses_are_not_full_coverage_proofs"] is True
    outcomes.append({"test": "m19_acceptance_remains_pending_full_replay", "status": "PASS"})

    output = {"schema": "n17.m17-m19.t2-directed-tests.v1", "status": "PASS",
              "tests": len(outcomes), "outcomes": outcomes}
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "tests": len(outcomes),
                      "report": str(OUTPUT), "sha256": digest(OUTPUT)}))


if __name__ == "__main__":
    main()
