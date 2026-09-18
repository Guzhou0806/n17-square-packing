"""Independent exact checker for the M19 nonuniform-grid lower bound.

This checker does not run a coverage sweep and does not import either the T0
producer or the T1 replay harness.  It binds those programs by SHA-256, checks
the two saved 17-row outputs, recounts every saved witness atom by atom, and
reconstructs the grid and endpoint arithmetic from the frozen source.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from math import isqrt
import json
from pathlib import Path
from typing import Any


EXPECTED = {
    "source": "461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652",
    "old_rows": "2883a709797923e7ce0b9889ab946e7399e52d7db5c866ba3faf71f3ca712fa4",
    "old_result": "5fa6210087f3e2c2ac8bb98053f88358051fdfdc4ccc2e6301661648edffc7b0",
    "m12_audit": "b5c2bb56ad69d0e21895797be4e4cb13435826953da282515da40083e58fc9af",
    "m14_certificate": "0e3f8b840924c382a8a76009a1987d9c97dc9184f41ba3e3bc7d40ca9d3b09d1",
    "m14_report": "32e7827975e37ab9e18299bb77e22c42026a53d851641e49497c46640ba06389",
    "m17_plan": "413a6e22f5eed846c5a73ef0831d5d7e9b8d6257fc52a6c84d33083368bc2ee2",
    "m17_authorization": "b82a62f527432432d722ccfe47e60049636ab7e16d19a77112efc772d5b2052b",
    "m17_theorem": "8daf02231120921095f3fae6467b08a7cd58aee28692ac7b34f7443cf60bd383",
    "m17_driver": "b83f57b9288f4a2a2857a72e9ab37736cebeb446341f8e314af28b27924f16ed",
    "m17_sweep": "1ddb94bb2a1a0350489752c44a5e9c4622c247f0142570fa5b622675ca652b38",
    "m17_result": "da21090426dfb196e6697d07c8c560dc5820bba34158ab3b83eaf3f6f5a54898",
    "m17_rows": "c4898a550541964260091bdf6a79a9483832d412cbfa5a8d734de2fe0fc62b77",
    "m17_failure_audit": "982bf9a69797343d64eecec920ebd38b196912745760e682e3b8c2ccea20f38a",
    "m19_precheck": "d05a523c6a6c62ee8ccc81dd77c1ed63ae20c157a0c28e6af2239fd08cdbc2be",
    "m19_plan": "701339de47b7ee0fcd16d51cca1ce8ea078228f4cd7ce0d33c21e60a31d9e684",
    "m19_authorization": "4e584e474d7f3b4f590877aeaa467d1f403bd5fb077c9a8b9ab81be8e758d79e",
    "m19_certificate": "4326a84caec0a60c0f70226c7a79bf4bbede2d1c032af8ca2aef319d2c91c806",
    "m19_producer": "1e8519922c57e6c016616d63f00d5e4dd332a067c1051916c414f847cc704533",
    "t1_review": "a61c3ea70e9883afb6871a172664156058ec5de919906f0980bbc787a8378e56",
    "t1_harness": "61bf58e4f6d64c9ef016dfe1ee3c53ea1182f93b91be390181876847b4ba6e8d",
    "t1_freeze": "452d0c472c0784a48fd0101e0cea56acf338dded8d20069adc3ee15e73ad3a68",
    "t1_result": "052b4dbbacdc0ddf5c08c569516d90cf7e7238deb9919e8e02d518e705f0a3fe",
    "t1_rows": "f480412ee29b4da83141a8666f96161a10d96868cc5ed612050b350b5c4eed8f",
}

PATHS = {
    "source": "coord/m14_m15/inputs/SOURCE_T019.json",
    "old_rows": "research/m12_work/run_001/DIRECTIONS.jsonl",
    "old_result": "research/m12_work/run_001/RESULT.json",
    "m12_audit": "workers/T2/outputs/m12_scaling/ATTEMPT_001_AUDIT.json",
    "m14_certificate": "research/m14_work/CERTIFICATE.json",
    "m14_report": "workers/T2/outputs/m14_m15/M14_FORMAL_REPORT.json",
    "m17_plan": "coord/m17_m18/PLAN.md",
    "m17_authorization": "coord/m17_m18/M17_COMPUTE_AUTHORIZATION.json",
    "m17_theorem": "research/m17_work/THEOREM_DRAFT.md",
    "m17_driver": "research/m17_work/run_refined_net.py",
    "m17_sweep": "research/m12_work/independent_sweep.py",
    "m17_result": "research/m17_work/run_001/RESULT.json",
    "m17_rows": "research/m17_work/run_001/DIRECTIONS.jsonl",
    "m17_failure_audit": "workers/T2/outputs/m17_lower/M17_FAILURE_AUDIT_ATTEMPT_002.json",
    "m19_precheck": "workers/T2/outputs/m17_lower/M19_STATIC_PRECHECK_ATTEMPT_002.json",
    "m19_plan": "coord/m17_m18/M19_PLAN.md",
    "m19_authorization": "coord/m17_m18/M19_COMPUTE_AUTHORIZATION.json",
    "m19_certificate": "research/m19_work/CERTIFICATE.json",
    "m19_producer": "research/m19_work/produce_certificate.py",
    "t1_review": "workers/T1/outputs/m17_m18/M19_REVIEW.md",
    "t1_harness": "workers/T1/outputs/m17_m18/m19_source_replay_v2.py",
    "t1_freeze": "workers/T1/outputs/m17_m18/M19_REPLAY_FREEZE_V2.json",
    "t1_result": "workers/T1/outputs/m17_m18/m19_replay/RESULT.json",
    "t1_rows": "workers/T1/outputs/m17_m18/m19_replay/ROWS.jsonl",
}


class AuditFailure(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads(text: str):
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(
                          AuditFailure(f"invalid JSON constant: {value}")))


def read_json(path: Path):
    return loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    return [loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def reject_floats(value: Any, label: str = "$") -> None:
    require(type(value) is not float, f"JSON float forbidden in certificate at {label}")
    if isinstance(value, dict):
        for key, child in value.items():
            reject_floats(child, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_floats(child, f"{label}[{index}]")


def ftext(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def rational(value: Any, label: str) -> F:
    require(type(value) is str and len(value) <= 512, f"{label}: rational string required")
    try:
        parsed = F(value)
    except (ValueError, ZeroDivisionError) as error:
        raise AuditFailure(f"{label}: invalid rational") from error
    require(value == ftext(parsed), f"{label}: noncanonical rational")
    return parsed


def decimal_bracket(square: F, digits: int) -> list[str]:
    scale = 10 ** digits
    floor = isqrt(square.numerator * scale * scale // square.denominator)
    while F(floor + 1, scale) ** 2 <= square:
        floor += 1
    while F(floor, scale) ** 2 > square:
        floor -= 1
    require(F(floor, scale) ** 2 < square < F(floor + 1, scale) ** 2,
            "decimal bracket is not strict")
    return [f"{floor // scale}.{floor % scale:0{digits}d}",
            f"{(floor + 1) // scale}.{(floor + 1) % scale:0{digits}d}"]


def direct_witness_mass(atoms, L: F, B: F, t: F, centre_uv) -> tuple[F, int, bool]:
    denominator = 1 + t * t
    c, s = (1 - t * t) / denominator, 2 * t / denominator
    require(c * c + s * s == 1 and c > 0 and s >= 0, "invalid direction axes")
    u0, v0 = map(F, centre_uv)
    x0, y0 = c * u0 - s * v0, s * u0 + c * v0
    radius = B * (c + s) / 2
    legal = radius <= x0 <= L - radius and radius <= y0 <= L - radius
    mass, count = F(0), 0
    for x, y, weight in atoms:
        u, v = c * x + s * y, -s * x + c * y
        if abs(u - u0) <= B / 2 and abs(v - v0) <= B / 2:
            mass += weight
            count += 1
    return mass, count, legal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root, report_path = args.root.resolve(), args.report.resolve()
    require(not report_path.exists(), f"refusing to overwrite report: {report_path}")
    paths = {key: root / relative for key, relative in PATHS.items()}
    try:
        for key, path in paths.items():
            require(path.is_file(), f"missing bound file: {key}")
            require(sha256(path) == EXPECTED[key], f"binding mismatch: {key}")

        source = read_json(paths["source"])
        old_rows = read_jsonl(paths["old_rows"])
        old_result = read_json(paths["old_result"])
        m12_audit = read_json(paths["m12_audit"])
        m14_certificate = read_json(paths["m14_certificate"])
        m14_report = read_json(paths["m14_report"])
        m17_auth = read_json(paths["m17_authorization"])
        m17_result = read_json(paths["m17_result"])
        m17_rows = read_jsonl(paths["m17_rows"])
        m17_failure_audit = read_json(paths["m17_failure_audit"])
        m19_precheck = read_json(paths["m19_precheck"])
        m19_auth = read_json(paths["m19_authorization"])
        certificate = read_json(paths["m19_certificate"])
        reject_floats(certificate)
        t1_freeze = read_json(paths["t1_freeze"])
        t1_result = read_json(paths["t1_result"])
        t1_rows = read_jsonl(paths["t1_rows"])

        L, B = F(source["outer_side"]), F(source["square_side"])
        total_mass = F(source["total_mass"])
        threshold = total_mass / 17
        angle_limit = F(source["angle_limit"])
        steps = source["direction_steps"]
        h = angle_limit / steps
        atoms = [(F(x), F(y), F(weight)) for x, y, weight in source["atoms"]]
        require((L, B, total_mass, threshold, steps, h) ==
                (F(459, 100), F(9977, 10000), F(423327, 25000),
                 F(423327, 425000), 180, F(207107, 90000000)),
                "frozen source constants")
        require(source["symmetry"] == "D4" and len(atoms) == 1184 and
                len({(x, y) for x, y, _ in atoms}) == 1184 and
                all(weight >= 0 for _, _, weight in atoms) and
                sum(weight for _, _, weight in atoms) == total_mass,
                "source atoms, sites, or total mass")
        measure = defaultdict(F)
        for x, y, weight in atoms:
            measure[x, y] += weight
        for (x, y), weight in measure.items():
            require(measure.get((L - y, x), F(0)) == weight and
                    measure.get((L - x, y), F(0)) == weight,
                    "source D4 invariance")

        require(len(old_rows) == 181 and [row["index"] for row in old_rows] == list(range(181)),
                "old row count/order")
        require([F(row["t"]) for row in old_rows] == [k * h for k in range(181)],
                "old row directions")
        old_minima = [F(row["minimum"]) for row in old_rows]
        require(all(value > threshold for value in old_minima) and
                min(old_minima) == F(200009, 200000) and
                all(row["direct_count_check"] is True for row in old_rows),
                "old-row strict coverage evidence")
        require(old_result["status"] == "PASS_EXACT_COVERAGE_AND_FIXED_SCALING" and
                old_result["input_sha256"] == EXPECTED["source"] and
                old_result["directions_completed"] == 181 and
                F(old_result["minimum"]) == min(old_minima), "old coverage result")
        require(m12_audit["status"] == "PASS" and m12_audit["test_count"] == 13,
                "M12 independent audit")
        require(m14_report["status"] == "PASS_ENDPOINT_LIMIT_LOWER_BOUND" and
                m14_report["certificate_sha256"] == EXPECTED["m14_certificate"],
                "M14 formal inheritance")

        expected_intervals = [0, 89, 179] + [k for k in range(180) if k not in {0, 89, 179}][:14]
        require(len(m17_rows) == 17 and
                [row["old_interval_index"] for row in m17_rows] == expected_intervals,
                "M17 authorized row order")
        for row in m17_rows:
            interval = row["old_interval_index"]
            require(row["refined_index"] == 2 * interval + 1 and
                    F(row["t"]) == (2 * interval + 1) * h / 2,
                    f"M17 direction at interval {interval}")
        m17_minima = [F(row["minimum"]) for row in m17_rows]
        passed_rows = [row for row in m17_rows if F(row["minimum"]) > threshold]
        failed_rows = [row for row in m17_rows if F(row["minimum"]) <= threshold]
        require(len(passed_rows) == 16 and len(failed_rows) == 1 and
                failed_rows[0]["refined_index"] == 29 and
                F(failed_rows[0]["minimum"]) == F(197153, 200000),
                "M17 threshold classification")
        require(m17_result["status"] == "FAIL_FIXED_REFINED_NET_COVERAGE" and
                m17_result["completed"] == 17 and
                F(m17_result["minimum"]) == min(m17_minima) and
                F(m17_result["strict_mass_threshold"]) == threshold,
                "M17 result")
        require(m17_failure_audit["status"] ==
                "PASS_M17_FIXED_361_NET_REJECTED_BY_EXACT_COUNTEREXAMPLE" and
                m19_precheck["status"] == "GO_PENDING_T1_INDEPENDENT_17_ROW_FULL_REPLAY",
                "T2 M17/precheck inheritance")

        t0_witnesses = []
        for row in m17_rows:
            mass, count, legal = direct_witness_mass(atoms, L, B, F(row["t"]), row["centre_uv"])
            require(legal and mass == F(row["minimum"]) and row["direct_count_check"] is True,
                    f"T0 direct witness at refined index {row['refined_index']}")
            if "centre_xy" in row:
                t = F(row["t"]); den = 1 + t * t
                c, s = (1 - t * t) / den, 2 * t / den
                u0, v0 = map(F, row["centre_uv"])
                require(tuple(map(F, row["centre_xy"])) == (c * u0 - s * v0, s * u0 + c * v0),
                        f"T0 xy/uv transform at refined index {row['refined_index']}")
            t0_witnesses.append({"refined_index": row["refined_index"],
                                 "captured_atoms": count, "mass": ftext(mass)})

        require(m19_auth["status"] == "AUTHORIZED" and
                m19_auth["source_replay_rows"] == 17 and
                m19_auth["new_search_directions"] == 0 and
                m19_auth["T1_harness"] == PATHS["t1_harness"] and
                m19_auth["T0_producer"] == PATHS["m19_producer"],
                "M19 authorization scope")
        for relative, expected_hash in m19_auth["bindings"].items():
            require(sha256(root / relative) == expected_hash, f"M19 authorization binding: {relative}")
        require(t1_freeze["schema"] == "n17.m19.source-replay-freeze.v2" and
                t1_freeze["harness"]["sha256"] == EXPECTED["t1_harness"] and
                t1_freeze["expected_old_interval_order"] == expected_intervals,
                "T1 freeze")
        require(t1_result["authorization_sha256"] == EXPECTED["m19_authorization"] and
                t1_result["status"] == "PASS_EXACT_MATCH_17" and
                t1_result["completed"] == t1_result["expected"] == 17 and
                t1_result["passing_rows"] == 16 and t1_result["failing_rows"] == 1 and
                t1_result["scope"] == "exactly the 17 rows already produced by M17; no unswept direction" and
                F(t1_result["threshold"]) == threshold and t1_result["weight_scale"] == 200000 and
                t1_result["seconds"] <= t1_result["soft_seconds"] == 30.0,
                "T1 replay result")
        normalized_bindings = {key.replace("\\", "/"): value
                               for key, value in t1_result["bindings"].items()}
        require(normalized_bindings[PATHS["m17_rows"]] == EXPECTED["m17_rows"] and
                normalized_bindings["workers/T1/outputs/m10_m11/global_followup/certificate.json"] == EXPECTED["source"],
                "T1 replay source bindings")
        require(len(t1_rows) == 17 and [row["row_number"] for row in t1_rows] == list(range(1, 18)),
                "T1 row count/order")
        t1_witnesses = []
        for t0, t1 in zip(m17_rows, t1_rows):
            expected_class = "PASS" if F(t0["minimum"]) > threshold else "FAIL"
            require((t1["old_interval_index"], t1["refined_index"], F(t1["t"])) ==
                    (t0["old_interval_index"], t0["refined_index"], F(t0["t"])) and
                    F(t1["source_minimum"]) == F(t1["expected_minimum"]) == F(t0["minimum"]) and
                    t1["source_classification"] == t1["expected_classification"] == expected_class and
                    t1["minimum_matches"] is True and t1["direct_witness_matches"] is True,
                    f"T1/T0 row match at refined index {t0['refined_index']}")
            mass, count, legal = direct_witness_mass(atoms, L, B, F(t1["t"]), t1["centre_uv"])
            require(legal and mass == F(t1["direct_witness_mass"]) == F(t0["minimum"]),
                    f"T1 direct witness at refined index {t0['refined_index']}")
            t1_witnesses.append({"refined_index": t0["refined_index"],
                                 "captured_atoms": count, "mass": ftext(mass)})

        require(certificate["schema"] == "n17.m19.nonuniform-grid-lower-bound.v1" and
                certificate["status"] == "PRODUCED_AWAITING_INDEPENDENT_AUDIT",
                "M19 certificate schema/status")
        require(certificate["source_sha256"] == EXPECTED["source"] and
                certificate["old_rows_sha256"] == EXPECTED["old_rows"] and
                certificate["m17_rows_sha256"] == EXPECTED["m17_rows"] and
                certificate["m17_result_sha256"] == EXPECTED["m17_result"] and
                certificate["producer_sha256"] == EXPECTED["m19_producer"],
                "M19 certificate bindings")
        passed_refined = [row["refined_index"] for row in passed_rows]
        failed_refined = [row["refined_index"] for row in failed_rows]
        require(certificate["selection_rule"] ==
                "all and only M17 observed rows strictly above total_mass/17; all old nodes retained" and
                certificate["passed_refined_indices"] == passed_refined and
                certificate["failed_refined_indices"] == failed_refined and
                (certificate["old_count"], certificate["new_pass_count"],
                 certificate["rejected_count"], certificate["merged_count"]) == (181, 16, 1, 197),
                "M19 deterministic selection")

        old_nodes = [k * h for k in range(181)]
        new_nodes = [F(row["t"]) for row in passed_rows]
        nodes = sorted(set(old_nodes + new_nodes))
        require(len(nodes) == 197 and [F(value) for value in certificate["directions"]] == nodes,
                "M19 merged directions")
        gaps = [(right - left) / (1 + left * right)
                for left, right in zip(nodes, nodes[1:])]
        require(len(gaps) == 196 and
                [F(value) for value in certificate["adjacent_half_gap_tangents"]] == gaps,
                "all 196 adjacent half-angle tangent gaps")
        D = max(gaps)
        maximum_indices = [index for index, value in enumerate(gaps) if value == D]
        require(len(maximum_indices) == 1 and D == F(621321000000, 270300253166143) < h,
                "unique M19 maximum gap")
        max_index = maximum_indices[0]
        max_pair = [nodes[max_index], nodes[max_index + 1]]
        require(max_pair == [14 * h, 15 * h] and
                F(certificate["maximum_gap"]) == D and
                [F(value) for value in certificate["maximum_gap_pair"]] == max_pair,
                "M19 maximum gap pair")

        retained_minimum = min(old_minima + [F(row["minimum"]) for row in passed_rows])
        strict_slack = 17 * retained_minimum - total_mass
        side_square = L * L * (1 + D * D) / (B * B * (1 + D) ** 2)
        old_side_square = F(m14_certificate["endpoint"]["side_square"])
        improvement = side_square - old_side_square
        require(F(certificate["L"]) == L and F(certificate["B"]) == B and
                F(certificate["mass"]) == total_mass and
                F(certificate["minimum_mass"]) == retained_minimum == F(200009, 200000) and
                F(certificate["strict_counting_slack"]) == strict_slack == F(13537, 200000) and
                F(certificate["threshold"]) == threshold,
                "M19 mass arithmetic")
        require(F(certificate["side_square"]) == side_square and
                F(certificate["old_m14_side_square"]) == old_side_square and
                F(certificate["squared_improvement"]) == improvement > 0,
                "M19 endpoint improvement")
        require(certificate["radical_expression"] == f"sqrt({ftext(side_square)})" and
                certificate["decimal_bracket_20"] == decimal_bracket(side_square, 20),
                "M19 radical/decimal endpoint")
        require(certificate["claim"] == "s(17) >= sqrt(side_square)" and
                certificate["endpoint_certificate"] is False and
                certificate["claims_strict_endpoint_infeasibility"] is False and
                certificate["M17_uniform_refinement_status"] == "FAILED_AND_RETAINED",
                "M19 claim boundary")

        report = {
            "schema": "n17.m19.t2-independent-verification.v1",
            "status": "PASS_M19_NONUNIFORM_GRID_LOWER_BOUND",
            "claim": f"s(17) >= sqrt({ftext(side_square)})",
            "endpoint_certificate": False,
            "claims_strict_endpoint_infeasibility": False,
            "coverage": {
                "old_full_domain_rows": 181,
                "new_full_domain_rows_replayed": 17,
                "retained_new_rows": 16,
                "rejected_new_rows": 1,
                "t0_t1_exact_minima_match": True,
                "t0_witnesses_independently_recounted": t0_witnesses,
                "t1_witnesses_independently_recounted": t1_witnesses,
            },
            "grid": {
                "nodes": len(nodes), "adjacent_gaps": len(gaps),
                "unique_maximum_gap_index": max_index,
                "maximum_gap_pair": [ftext(value) for value in max_pair],
                "D": ftext(D), "old_D": ftext(h), "D_strictly_smaller": True,
            },
            "mass": {
                "total": ftext(total_mass), "threshold": ftext(threshold),
                "retained_minimum": ftext(retained_minimum),
                "17_minimum_minus_total": ftext(strict_slack),
            },
            "endpoint": {
                "side_square": ftext(side_square),
                "old_m14_side_square": ftext(old_side_square),
                "squared_improvement": ftext(improvement),
                "decimal_bracket_20": decimal_bracket(side_square, 20),
            },
            "independence": {
                "coverage_sweep_run_by_checker": False,
                "producer_imported_by_checker": False,
                "t1_harness_imported_by_checker": False,
                "t0_and_t1_witness_coordinates_required_equal": False,
            },
            "bindings": {key: {"path": PATHS[key], "sha256": sha256(path)}
                         for key, path in paths.items()},
            "certificate_sha256": EXPECTED["m19_certificate"],
            "checker_sha256": sha256(Path(__file__)),
            "claim_boundary": (
                "An ordinary >= lower bound obtained by the inherited strict-dilation argument. "
                "It is not endpoint infeasibility, does not repair M17, and adds no searched direction."
            ),
        }
        code = 0
    except (AuditFailure, KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        report = {"schema": "n17.m19.t2-independent-verification.v1",
                  "status": "FAIL_M19_INDEPENDENT_AUDIT", "error": str(error)}
        code = 1

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "report": str(report_path),
                      "report_sha256": sha256(report_path)}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
