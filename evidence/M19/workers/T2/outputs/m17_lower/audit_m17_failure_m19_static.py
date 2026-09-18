"""Independent M17 counterexample audit and M19 static nonuniform-grid review.

No coverage sweep is run.  M17 is rejected from one exact legal centre whose
captured mass is recomputed atom by atom.  M19 is checked only for deterministic
grid/algebra consequences and remains pending the separately authorized T1
full-source replay of all 17 observed M17 rows.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from math import isqrt
import json
from pathlib import Path


EXPECTED = {
    "source": "461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652",
    "plan": "413a6e22f5eed846c5a73ef0831d5d7e9b8d6257fc52a6c84d33083368bc2ee2",
    "authorization": "b82a62f527432432d722ccfe47e60049636ab7e16d19a77112efc772d5b2052b",
    "theorem": "8daf02231120921095f3fae6467b08a7cd58aee28692ac7b34f7443cf60bd383",
    "driver": "b83f57b9288f4a2a2857a72e9ab37736cebeb446341f8e314af28b27924f16ed",
    "sweep": "1ddb94bb2a1a0350489752c44a5e9c4622c247f0142570fa5b622675ca652b38",
    "result": "da21090426dfb196e6697d07c8c560dc5820bba34158ab3b83eaf3f6f5a54898",
    "directions": "c4898a550541964260091bdf6a79a9483832d412cbfa5a8d734de2fe0fc62b77",
    "m19_plan": "701339de47b7ee0fcd16d51cca1ce8ea078228f4cd7ce0d33c21e60a31d9e684",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def ftext(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def canonical_hash(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def decimal_bracket(square: F, digits: int) -> list[str]:
    scale = 10**digits
    floor = isqrt(square.numerator * scale * scale // square.denominator)
    while F(floor + 1, scale) ** 2 <= square:
        floor += 1
    while F(floor, scale) ** 2 > square:
        floor -= 1
    require(F(floor, scale) ** 2 < square < F(floor + 1, scale) ** 2,
            "endpoint bracket")
    return [f"{floor // scale}.{floor % scale:0{digits}d}",
            f"{(floor + 1) // scale}.{(floor + 1) % scale:0{digits}d}"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--m17-report", type=Path,
                        default=Path(__file__).with_name("M17_FAILURE_AUDIT.json"))
    parser.add_argument("--m19-report", type=Path,
                        default=Path(__file__).with_name("M19_STATIC_PRECHECK.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    m17_path, m19_path = args.m17_report.resolve(), args.m19_report.resolve()
    require(not m17_path.exists() and not m19_path.exists(), "refusing to overwrite reports")
    paths = {
        "source": root / "coord/m14_m15/inputs/SOURCE_T019.json",
        "plan": root / "coord/m17_m18/PLAN.md",
        "authorization": root / "coord/m17_m18/M17_COMPUTE_AUTHORIZATION.json",
        "theorem": root / "research/m17_work/THEOREM_DRAFT.md",
        "driver": root / "research/m17_work/run_refined_net.py",
        "sweep": root / "research/m12_work/independent_sweep.py",
        "result": root / "research/m17_work/run_001/RESULT.json",
        "directions": root / "research/m17_work/run_001/DIRECTIONS.jsonl",
        "m19_plan": root / "coord/m17_m18/M19_PLAN.md",
    }
    for key, path in paths.items():
        require(sha256(path) == EXPECTED[key], f"binding {key}")

    source = read_json(paths["source"])
    authorization = read_json(paths["authorization"])
    result = read_json(paths["result"])
    rows = [json.loads(line) for line in
            paths["directions"].read_text(encoding="utf-8").splitlines()]
    require(result["status"] == "FAIL_FIXED_REFINED_NET_COVERAGE", "result status")
    require(result["completed"] == len(rows) == 17 and
            result["planned_new_nodes"] == 180 and result["old_nodes_inherited"] == 181,
            "run counts")
    require(result["source_sha256"] == EXPECTED["source"] and
            result["sweep_sha256"] == EXPECTED["sweep"] and
            result["driver_sha256"] == EXPECTED["driver"] and
            result["authorization_sha256"] == EXPECTED["authorization"], "run bindings")

    L, B = F(source["outer_side"]), F(source["square_side"])
    total_mass = F(source["total_mass"])
    threshold = total_mass / 17
    h = F(source["angle_limit"]) / source["direction_steps"]
    atoms = [(F(x), F(y), F(weight)) for x, y, weight in source["atoms"]]
    require(len(atoms) == 1184 and len({(x, y) for x, y, _ in atoms}) == 1184,
            "source atom sites")
    require(sum(weight for _, _, weight in atoms) == total_mass, "source total mass")
    require(F(result["strict_mass_threshold"]) == threshold == F(423327, 425000),
            "frozen threshold")

    pilots = authorization["pilot_old_interval_indices"]
    continuation = [k for k in range(180) if k not in pilots]
    expected_intervals = pilots + continuation[:14]
    require([row["old_interval_index"] for row in rows] == expected_intervals,
            "authorized run order through first failure")
    for row in rows:
        interval = row["old_interval_index"]
        require(row["refined_index"] == 2 * interval + 1 and
                F(row["t"]) == (2 * interval + 1) * h / 2,
                f"row direction {interval}")
    minima = [F(row["minimum"]) for row in rows]
    require(all(value > threshold for value in minima[:-1]) and minima[-1] <= threshold,
            "first threshold failure")
    require(F(result["minimum"]) == minima[-1], "reported run minimum")

    failing = rows[-1]
    t = F(failing["t"])
    denominator = 1 + t * t
    c, s = (1 - t * t) / denominator, 2 * t / denominator
    require(c * c + s * s == 1 and c > 0 and s >= 0, "failing direction axes")
    u0, v0 = map(F, failing["centre_uv"])
    x0, y0 = map(F, failing["centre_xy"])
    require((c * x0 + s * y0, -s * x0 + c * y0) == (u0, v0),
            "centre xy/uv transform")
    radius = B * (c + s) / 2
    require(radius < x0 < L - radius and radius < y0 < L - radius,
            "strictly legal failing centre")
    ua, ub, va, vb = map(F, failing["cell"])
    require(ua < u0 < ub and va < v0 < vb, "witness inside reported open cell")

    captured = []
    boundary_hits = []
    direct_mass = F(0)
    for index, (x, y, weight) in enumerate(atoms):
        u, v = c * x + s * y, -s * x + c * y
        du, dv = abs(u - u0), abs(v - v0)
        if du <= B / 2 and dv <= B / 2:
            captured.append({"atom_index": index, "weight": ftext(weight)})
            direct_mass += weight
            if du == B / 2 or dv == B / 2:
                boundary_hits.append(index)
    require(direct_mass == F(failing["minimum"]) == F(197153, 200000),
            "direct failing-centre atom count")
    require(failing["direct_count_check"] is True, "producer direct-count flag")
    deficit = direct_mass - threshold
    count_margin = 17 * direct_mass - total_mass
    require(deficit == F(-7003, 680000) and count_margin == F(-7003, 40000),
            "failure margins")

    bindings = {key: {"path": str(path), "sha256": sha256(path)}
                for key, path in paths.items()}
    m17_output = {
        "schema": "n17.m17.t2-exact-counterexample-audit.v1",
        "status": "PASS_M17_FIXED_361_NET_REJECTED_BY_EXACT_COUNTEREXAMPLE",
        "sweep_rerun": False,
        "run_protocol": {
            "pilot_old_interval_indices": pilots,
            "completed_rows": len(rows), "passed_rows_before_failure": 16,
            "first_failed_old_interval_index": failing["old_interval_index"],
            "first_failed_refined_index": failing["refined_index"],
        },
        "counterexample": {
            "t": ftext(t), "centre_uv": [ftext(u0), ftext(v0)],
            "centre_xy": [ftext(x0), ftext(y0)],
            "probe_radius_xy": ftext(radius),
            "strictly_inside_feasible_centre_domain": True,
            "inside_reported_open_cell": True,
            "captured_atom_count": len(captured),
            "captured_atoms": captured,
            "closed_boundary_atom_hits": boundary_hits,
            "direct_captured_mass": ftext(direct_mass),
            "threshold": ftext(threshold),
            "mass_minus_threshold": ftext(deficit),
            "17_mass_minus_total_mass": ftext(count_margin),
        },
        "logic": (
            "One legal centre with captured mass <= total_mass/17 disproves the universal "
            "row condition. The reported point is sufficient even without proving it is the "
            "global minimum of that direction."
        ),
        "bindings": bindings,
        "checker_sha256": sha256(Path(__file__)),
        "claim_boundary": (
            "Rejects only the fixed T-019 measure, B, full midpoint grid and uniform-minimum "
            "certificate. It does not reject other measures, grids, B values, or lower-bound methods."
        ),
    }

    passed_intervals = sorted(row["old_interval_index"] for row in rows[:-1])
    require(passed_intervals == list(range(14)) + [89, 179], "fixed M19 passed set")
    old_nodes = [k * h for k in range(181)]
    new_nodes = [(2 * k + 1) * h / 2 for k in passed_intervals]
    nodes = sorted(set(old_nodes + new_nodes))
    require(len(nodes) == 197, "M19 node count")
    gaps = []
    for index, (left, right) in enumerate(zip(nodes, nodes[1:])):
        value = (right - left) / (1 + left * right)
        gaps.append({"gap_index": index, "left": ftext(left), "right": ftext(right),
                     "tangent_half_angle_gap": ftext(value)})
    gap_values = [F(row["tangent_half_angle_gap"]) for row in gaps]
    D = max(gap_values)
    maximum_indices = [i for i, value in enumerate(gap_values) if value == D]
    expected_D = h / (1 + F(14 * 15) * h * h)
    require(D == expected_D < h and len(maximum_indices) == 1, "M19 maximum gap")
    max_gap = gaps[maximum_indices[0]]
    require(F(max_gap["left"]) == 14 * h and F(max_gap["right"]) == 15 * h,
            "M19 maximum unrefined interval")
    endpoint_square = L * L * (1 + D * D) / (B * B * (1 + D) ** 2)
    radical = D.denominator**2 + D.numerator**2
    radical_denominator = 9977 * (D.denominator + D.numerator)
    require(endpoint_square == F(45900**2 * radical, radical_denominator**2),
            "M19 radical endpoint")
    m19_output = {
        "schema": "n17.m19.t2-static-precheck.v1",
        "status": "GO_PENDING_T1_INDEPENDENT_17_ROW_FULL_REPLAY",
        "relation_to_m17": (
            "Separate deterministic implication. M17 remains failed; the failed interval 14 "
            "midpoint is excluded, and no new direction is searched or generated."
        ),
        "fixed_passed_old_interval_indices": passed_intervals,
        "coverage_evidence_status": {
            "producer_reported_passed_rows": 16,
            "direct_minimum_witnesses_are_not_full_coverage_proofs": True,
            "required_before_acceptance": (
                "T1 locked independent two-dimensional difference sweep must fully replay all "
                "17 observed rows and agree row by row, including the failure."
            ),
        },
        "grid": {
            "old_nodes": 181, "retained_new_nodes": 16, "total_nodes": len(nodes),
            "adjacent_gaps": len(gaps), "all_gaps": gaps,
            "all_gaps_canonical_sha256": canonical_hash(gaps),
            "maximum_gap_indices": maximum_indices,
            "maximum_gap": max_gap,
            "D": ftext(D), "old_D": ftext(h), "D_strictly_below_old_D": True,
        },
        "conditional_endpoint": {
            "condition": "independent full replay validates every one of the 16 retained rows",
            "S_square": ftext(endpoint_square),
            "S_radical": f"45900*sqrt({radical})/{radical_denominator}",
            "positive_root_polynomial": {
                "x2": radical_denominator**2,
                "constant": -(45900**2 * radical),
            },
            "decimal_bracket_20": decimal_bracket(endpoint_square, 20),
            "claim_if_condition_holds": "s(17) >= S",
            "endpoint_strict_certificate": False,
        },
        "bindings": bindings,
        "checker_sha256": sha256(Path(__file__)),
        "claim_boundary": (
            "Static grid/algebra review only. M19 is not accepted until independent complete "
            "coverage replay validates all retained rows; witness recounts alone are insufficient."
        ),
    }
    for path, output in ((m17_path, m17_output), (m19_path, m19_output)):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "m17_status": m17_output["status"], "m17_report": str(m17_path),
        "m17_sha256": sha256(m17_path), "m19_status": m19_output["status"],
        "m19_report": str(m19_path), "m19_sha256": sha256(m19_path)}))


if __name__ == "__main__":
    main()
