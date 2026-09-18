"""Independent M12 audit: exact small-cell oracle and frozen-output comparison.

The oracle deliberately does not reuse the production sweep's geometry, clipping,
or range tree.  It enumerates every open arrangement cell, clips the feasible
centre polygon against that cell using a separately written half-plane routine,
and directly counts atom weights at a rational interior point.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
T0_SOURCE = ROOT / "research" / "m12_work" / "independent_sweep.py"
T0_RESULT = ROOT / "research" / "m12_work" / "run_001" / "RESULT.json"
T0_DIRECTIONS = ROOT / "research" / "m12_work" / "run_001" / "DIRECTIONS.jsonl"
T1_RESULTS = (
    ROOT / "workers" / "T1" / "outputs" / "m10_m11" / "global_followup"
    / "m12" / "results"
)
FIXED_INPUT_SHA = "461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652"
FIXED_T0_SOURCE_SHA = "1ddb94bb2a1a0350489752c44a5e9c4622c247f0142570fa5b622675ca652b38"
FIXED_LAMBDA = F(1000001, 1000000)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_t0():
    require(sha256(T0_SOURCE) == FIXED_T0_SOURCE_SHA, "T0 source hash drift")
    spec = importlib.util.spec_from_file_location("m12_t0_frozen", T0_SOURCE)
    require(spec is not None and spec.loader is not None, "cannot load T0 source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rotation(t: F) -> tuple[F, F]:
    denominator = 1 + t * t
    return (1 - t * t) / denominator, 2 * t / denominator


def oracle_geometry(S: F, B: F, atoms: list[tuple[F, F, F]], t: F):
    c, s = rotation(t)
    r = B * (c + s) / 2
    corners = [(r, r), (S - r, r), (S - r, S - r), (r, S - r)]
    polygon = [(c * x + s * y, -s * x + c * y) for x, y in corners]
    rotated = [(c * x + s * y, -s * x + c * y, w) for x, y, w in atoms]
    boxes = [(u - B / 2, u + B / 2, v - B / 2, v + B / 2, w)
             for u, v, w in rotated]
    return polygon, boxes


def clip_halfplane(poly, axis: int, bound: F, keep_greater: bool):
    """Independent Sutherland-Hodgman clipping using exact fractions."""
    if not poly:
        return []

    def signed(p):
        return p[axis] - bound if keep_greater else bound - p[axis]

    out = []
    previous = poly[-1]
    previous_value = signed(previous)
    for current in poly:
        current_value = signed(current)
        previous_inside = previous_value >= 0
        current_inside = current_value >= 0
        if previous_inside != current_inside:
            ratio = previous_value / (previous_value - current_value)
            out.append((
                previous[0] + ratio * (current[0] - previous[0]),
                previous[1] + ratio * (current[1] - previous[1]),
            ))
        if current_inside:
            out.append(current)
        previous = current
        previous_value = current_value
    return out


def clip_to_cell(poly, ua: F, ub: F, va: F, vb: F):
    result = list(poly)
    for axis, bound, keep_greater in (
        (0, ua, True), (0, ub, False), (1, va, True), (1, vb, False)
    ):
        result = clip_halfplane(result, axis, bound, keep_greater)
    # Consecutive or closing duplicates can arise when a clipping line hits a vertex.
    cleaned = []
    for point in result:
        if not cleaned or point != cleaned[-1]:
            cleaned.append(point)
    if len(cleaned) > 1 and cleaned[0] == cleaned[-1]:
        cleaned.pop()
    return cleaned


def twice_area(poly) -> F:
    if len(poly) < 3:
        return F(0)
    return abs(sum(p[0] * q[1] - p[1] * q[0]
                   for p, q in zip(poly, poly[1:] + poly[:1])))


def point_in_convex_closure(point, poly) -> bool:
    signs = []
    for p, q in zip(poly, poly[1:] + poly[:1]):
        cross = (q[0] - p[0]) * (point[1] - p[1]) - (q[1] - p[1]) * (point[0] - p[0])
        if cross:
            signs.append(cross > 0)
    return not signs or all(value == signs[0] for value in signs)


def brute_cell_minimum(S: F, B: F, atoms: list[tuple[F, F, F]], t: F):
    """Enumerate all arrangement cells that meet the feasible region in positive area."""
    polygon, boxes = oracle_geometry(S, B, atoms, t)
    us = sorted({value for a, b, _, _, _ in boxes for value in (a, b)} |
                {u for u, _ in polygon})
    vs = sorted({value for _, _, a, b, _ in boxes for value in (a, b)} |
                {v for _, v in polygon})
    best = None
    checked = 0
    non_midpoint_cells = 0
    witness = None
    for ua, ub in zip(us, us[1:]):
        for va, vb in zip(vs, vs[1:]):
            piece = clip_to_cell(polygon, ua, ub, va, vb)
            if twice_area(piece) == 0:
                continue
            checked += 1
            midpoint = ((ua + ub) / 2, (va + vb) / 2)
            if not point_in_convex_closure(midpoint, polygon):
                non_midpoint_cells += 1
            point = (sum(p[0] for p in piece) / len(piece),
                     sum(p[1] for p in piece) / len(piece))
            require(ua < point[0] < ub and va < point[1] < vb,
                    "oracle failed to produce an open-cell point")
            value = sum(w for a, b, lo, hi, w in boxes
                        if a < point[0] < b and lo < point[1] < hi)
            if best is None or value < best:
                best = value
                witness = (ua, ub, va, vb, point)
    require(best is not None, "oracle found no feasible open cell")
    return {"minimum": best, "cells": checked,
            "non_midpoint_cells": non_midpoint_cells, "witness": witness}


def compare_fixture(t0, name: str, S: F, B: F,
                    atoms: list[tuple[F, F, F]], t: F,
                    expected: F | None = None):
    oracle = brute_cell_minimum(S, B, atoms, t)
    observed = F(t0.coverage(S, B, atoms, t)["minimum"])
    require(observed == oracle["minimum"],
            f"{name}: sweep {observed} != oracle {oracle['minimum']}")
    if expected is not None:
        require(observed == expected, f"{name}: expected {expected}, got {observed}")
    return {"name": name, "status": "PASS", "minimum": str(observed),
            "oracle_cells": oracle["cells"],
            "non_midpoint_cells": oracle["non_midpoint_cells"]}


def static_record():
    return {
        "n": 17,
        "outer_side": "5",
        "square_side": "1/2",
        "direction_steps": 180,
        "symmetry": "D4",
        "total_mass": "1",
        "angle_limit": "207107/500000",
        "least_cell_mass": "0",
        "atoms": [["5/2", "5/2", "1"]],
    }


def expect_assertion(call, label: str) -> dict:
    try:
        call()
    except AssertionError as error:
        return {"name": label, "status": "PASS", "rejection": str(error)}
    raise AssertionError(f"{label}: expected rejection")


def test_range_tree(t0) -> dict:
    values = [0] * 7
    tree = t0.RangeMin(len(values))
    operations = [(0, 3, 5), (2, 7, 4), (3, 5, 2), (2, 7, -4), (1, 6, 3)]
    for ql, qr, delta in operations:
        tree.add(ql, qr, delta)
        for index in range(ql, qr):
            values[index] += delta
        for lo in range(len(values)):
            for hi in range(lo + 1, len(values) + 1):
                expected = min(values[lo:hi])
                require(tree.minimum(lo, hi) == expected, "range-min mismatch")
                require(values[tree.argmin(lo, hi, expected)] == expected,
                        "argmin mismatch")
    return {"name": "range_tree_all_subranges", "status": "PASS",
            "operations": len(operations), "queries": len(operations) * 28}


def test_fixture_suite(t0) -> list[dict]:
    results = [test_range_tree(t0)]

    # Two rectangles end and start at the same u, and two starts are duplicated.
    tie_atoms = [(F(1), F(2), F(1, 2)), (F(2), F(2), F(1, 3)),
                 (F(2), F(2), F(1, 6))]
    polygon, boxes = oracle_geometry(F(4), F(1), tie_atoms, F(0))
    u_events = Counter(value for a, b, _, _, _ in boxes for value in (a, b))
    require(max(u_events.values()) >= 2 and any(
        boxes[i][1] == boxes[j][0] for i in range(len(boxes)) for j in range(len(boxes))
    ), "tie fixture lacks its intended event ties")
    results.append(compare_fixture(t0, "coincident_start_end_events", F(4), F(1),
                                   tie_atoms, F(0), F(0)))

    outside_atoms = [(F(5, 2), F(5, 2), F(1))]
    results.append(compare_fixture(t0, "outside_atom_event_zero_region", F(5), F(1),
                                   outside_atoms, F(1, 3), F(0)))

    projection = compare_fixture(t0, "full_strip_projection_not_midpoint", F(5), F(1),
                                 outside_atoms, F(1, 2), F(0))
    require(projection["non_midpoint_cells"] > 0,
            "projection fixture did not contain an endpoint-only intersecting cell")
    results.append(projection)

    endpoint_atoms = [(F(1), F(1), F(1, 2)), (F(4), F(1), F(1, 3)),
                      (F(1), F(4), F(1, 5)), (F(4), F(4), F(1, 7)),
                      (F(5, 2), F(5, 2), F(1))]
    limit = F(207107, 500000)
    results.append(compare_fixture(t0, "direction_endpoint_t0", F(5), F(1, 2),
                                   endpoint_atoms, F(0), F(0)))
    results.append(compare_fixture(t0, "direction_endpoint_over_pi_over_4", F(5), F(1, 2),
                                   endpoint_atoms, limit, F(0)))

    original = brute_cell_minimum(F(5), F(1, 2), endpoint_atoms, F(1, 3))["minimum"]
    scaled_atoms = [(FIXED_LAMBDA * x, FIXED_LAMBDA * y, w)
                    for x, y, w in endpoint_atoms]
    scaled = brute_cell_minimum(FIXED_LAMBDA * 5, FIXED_LAMBDA / 2,
                                scaled_atoms, F(1, 3))["minimum"]
    require(original == scaled, "independent scaling bijection fixture failed")
    results.append({"name": "independent_scaling_bijection", "status": "PASS",
                    "minimum": str(original)})
    return results


def test_static_gates(t0) -> list[dict]:
    record = static_record()
    _, _, _, ts, static = t0.check_static(record)
    require(ts[0] == 0 and ts[-1] == F(record["angle_limit"]),
            "direction endpoint construction mismatch")
    require(F(static["strict_containment_margin"]) > 0, "valid margin is not positive")
    results = [{"name": "valid_D4_endpoint_and_lambda", "status": "PASS",
                "D": static["D"], "margin": static["strict_containment_margin"]}]

    broken = deepcopy(record)
    broken["atoms"] = [["1", "2", "1"]]
    results.append(expect_assertion(lambda: t0.check_static(broken), "D4_missing_orbit_rejected"))

    broken = deepcopy(record)
    broken["atoms"] = [["5/2", "5/2", "-1"]]
    broken["total_mass"] = "-1"
    results.append(expect_assertion(lambda: t0.check_static(broken), "negative_weight_rejected"))

    broken = deepcopy(record)
    broken["angle_limit"] = "2/5"
    results.append(expect_assertion(lambda: t0.check_static(broken), "short_direction_arc_rejected"))

    results.append(expect_assertion(lambda: t0.check_static(record, scale=F(3)),
                                    "lambda_containment_failure_rejected"))
    return results


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_full_outputs() -> dict:
    t0_result = read_json(T0_RESULT)
    t0_rows = [json.loads(line) for line in T0_DIRECTIONS.read_text(encoding="utf-8").splitlines()]
    source_path = T1_RESULTS / "source_result.json"
    scaled_path = T1_RESULTS / "scaled_result.json"
    comparison_path = T1_RESULTS / "COMPARISON.json"
    source = read_json(source_path)
    scaled = read_json(scaled_path)
    comparison = read_json(comparison_path)

    require(t0_result["input_sha256"] == FIXED_INPUT_SHA, "T0 input binding mismatch")
    require(t0_result["source_sha256"] == FIXED_T0_SOURCE_SHA, "T0 result source binding mismatch")
    require(t0_result["status"] == "PASS_EXACT_COVERAGE_AND_FIXED_SCALING",
            "T0 result did not pass")
    require(len(t0_rows) == t0_result["directions_completed"] == 181,
            "T0 direction count mismatch")
    require([row["index"] for row in t0_rows] == list(range(181)),
            "T0 direction indices are not consecutive")

    require(source["input"]["certificate_sha256"] == FIXED_INPUT_SHA,
            "T1 source input binding mismatch")
    require(scaled["input"]["certificate_sha256"] == FIXED_INPUT_SHA,
            "T1 scaled input binding mismatch")
    require(source["lambda"] == "1" and scaled["lambda"] == str(FIXED_LAMBDA),
            "T1 lambda labels mismatch")
    require(source["certificate"]["accepted"] and scaled["certificate"]["accepted"],
            "T1 source/scaled replay did not accept")
    require(comparison["all_equal"] and comparison["mismatch_indices"] == [],
            "T1 source/scaled per-direction comparison failed")
    require(comparison["source_result_sha256"] == sha256(source_path),
            "T1 source result hash binding mismatch")
    require(comparison["scaled_result_sha256"] == sha256(scaled_path),
            "T1 scaled result hash binding mismatch")

    t0_values = [F(row["minimum"]) for row in t0_rows]
    source_values = [F(row["minimum_cell_mass"]) for row in source["per_direction"]]
    scaled_values = [F(row["minimum_cell_mass"]) for row in scaled["per_direction"]]
    require(t0_values == source_values == scaled_values,
            "T0/T1 per-direction minima differ")
    expected_minimum = F(200009, 200000)
    require(min(t0_values) == expected_minimum, "unexpected global finite-net minimum")
    require(F(t0_result["static"]["strict_containment_margin"]) ==
            F(2793464693461, 900000000000000000), "strict margin mismatch")
    return {
        "name": "full_181_direction_three_way_comparison",
        "status": "PASS",
        "directions": 181,
        "minimum": str(expected_minimum),
        "t0_directions_sha256": sha256(T0_DIRECTIONS),
        "t0_result_sha256": sha256(T0_RESULT),
        "t1_source_result_sha256": sha256(source_path),
        "t1_scaled_result_sha256": sha256(scaled_path),
        "t1_comparison_sha256": sha256(comparison_path),
    }


def main() -> None:
    t0 = load_t0()
    tests = []
    tests.extend(test_fixture_suite(t0))
    tests.extend(test_static_gates(t0))
    tests.append(test_full_outputs())
    require(all(row["status"] == "PASS" for row in tests), "not all tests passed")
    report = {
        "schema": "n17.m12.t2-independent-audit.v1",
        "status": "PASS",
        "test_count": len(tests),
        "tests": tests,
        "bindings": {
            "t0_source": str(T0_SOURCE.relative_to(ROOT)).replace("\\", "/"),
            "t0_source_sha256": sha256(T0_SOURCE),
            "fixed_input_sha256": FIXED_INPUT_SHA,
            "audit_source_sha256": sha256(Path(__file__)),
        },
        "scope": "Code/math audit and exact verification only; no packing optimization.",
    }
    output = Path(__file__).with_name("ATTEMPT_001_AUDIT.json")
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "tests": len(tests),
                      "report": str(output), "report_sha256": sha256(output)}))


if __name__ == "__main__":
    main()
