"""Stage-A static audit for the proposed 361-direction T-019 refinement.

This program performs no coverage sweep.  It checks inherited bindings, D4,
the old 181 rows, the interleaved rational grid, endpoint coverage, the exact
angular error D=h/2, the generalized mass threshold, static feasible-domain
conditions, and the conditional endpoint algebra.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from math import isqrt
import json
from pathlib import Path


EXPECTED = {
    "source": "461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652",
    "old_directions": "2883a709797923e7ce0b9889ab946e7399e52d7db5c866ba3faf71f3ca712fa4",
    "m12_audit": "b5c2bb56ad69d0e21895797be4e4cb13435826953da282515da40083e58fc9af",
    "m14_certificate": "0e3f8b840924c382a8a76009a1987d9c97dc9184f41ba3e3bc7d40ca9d3b09d1",
    "m14_report": "32e7827975e37ab9e18299bb77e22c42026a53d851641e49497c46640ba06389",
}
PILOT_INDICES = [1, 199, 335, 359]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def ftext(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def decimal_bracket(square: F, digits: int) -> tuple[str, str]:
    scale = 10**digits
    floor = isqrt(square.numerator * scale * scale // square.denominator)
    while F(floor + 1, scale) ** 2 <= square:
        floor += 1
    while F(floor, scale) ** 2 > square:
        floor -= 1
    lower, upper = F(floor, scale), F(floor + 1, scale)
    require(lower * lower < square < upper * upper, "strict decimal bracket")
    def render(integer: int) -> str:
        return f"{integer // scale}.{integer % scale:0{digits}d}"
    return render(floor), render(floor + 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--report", type=Path,
                        default=Path(__file__).with_name("STAGE_A_STATIC_AUDIT.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    report_path = args.report.resolve()
    require(not report_path.exists(), f"refusing to overwrite {report_path}")
    paths = {
        "source": root / "coord/m14_m15/inputs/SOURCE_T019.json",
        "old_directions": root / "research/m12_work/run_001/DIRECTIONS.jsonl",
        "m12_audit": root / "workers/T2/outputs/m12_scaling/ATTEMPT_001_AUDIT.json",
        "m14_certificate": root / "research/m14_work/CERTIFICATE.json",
        "m14_report": root / "workers/T2/outputs/m14_m15/M14_FORMAL_REPORT.json",
    }
    for key, path in paths.items():
        require(sha256(path) == EXPECTED[key], f"binding {key}")

    source = read_json(paths["source"])
    require((source["n"], source["outer_side"], source["square_side"],
             source["angle_limit"], source["direction_steps"], source["total_mass"],
             source["least_cell_mass"], source["symmetry"]) ==
            (17, "459/100", "9977/10000", "207107/500000", 180,
             "423327/25000", "200009/200000", "D4"), "source constants")
    L, B = F(source["outer_side"]), F(source["square_side"])
    terminal = F(source["angle_limit"])
    total_mass = F(source["total_mass"])
    threshold = total_mass / 17
    atoms = [(F(x), F(y), F(weight)) for x, y, weight in source["atoms"]]
    require(len(atoms) == 1184 and all(0 <= x <= L and 0 <= y <= L and weight >= 0
                                           for x, y, weight in atoms), "atoms")
    require(sum(weight for _, _, weight in atoms) == total_mass < 17, "total mass")
    measure = defaultdict(F)
    for x, y, weight in atoms:
        measure[x, y] += weight
    for (x, y), weight in measure.items():
        require(measure.get((L - y, x), F(0)) == weight, "D4 rotation")
        require(measure.get((L - x, y), F(0)) == weight, "D4 reflection")

    old_rows = [json.loads(line) for line in
                paths["old_directions"].read_text(encoding="utf-8").splitlines()]
    require(len(old_rows) == 181 and [row["index"] for row in old_rows] == list(range(181)),
            "old row count/order")
    h = terminal / 180
    require(h == F(207107, 90000000), "old h")
    require([F(row["t"]) for row in old_rows] == [k * h for k in range(181)],
            "old row directions")
    old_minima = [F(row["minimum"]) for row in old_rows]
    require(min(old_minima) == F(source["least_cell_mass"]) > 1 > threshold,
            "old row minimum and generalized threshold")
    transitions = [row["index"] for row, nxt in zip(old_rows, old_rows[1:])
                   if row["minimum"] != nxt["minimum"]]
    require(transitions == [99, 167], "old minimum transitions")

    d = h / 2
    grid = [j * d for j in range(361)]
    require(grid[0] == 0 and grid[-1] == terminal and
            all(left < right for left, right in zip(grid, grid[1:])), "new grid")
    require([grid[2 * k] for k in range(181)] == [F(row["t"]) for row in old_rows],
            "even-row inheritance")
    angular_tangent_gaps = [(right - left) / (1 + left * right)
                            for left, right in zip(grid, grid[1:])]
    D = max(angular_tangent_gaps)
    require(D == d and angular_tangent_gaps.index(D) == 0, "new D=h/2")
    endpoint_polynomial = terminal * terminal + 2 * terminal - 1
    require(endpoint_polynomial > 0, "terminal reaches beyond tan(pi/8)")

    minimum_domain_margin = None
    for t in grid:
        denominator = 1 + t * t
        cosine = (1 - t * t) / denominator
        sine = 2 * t / denominator
        require(cosine * cosine + sine * sine == 1 and cosine >= 0 and sine >= 0,
                "rational direction")
        radius = B * (cosine + sine) / 2
        margin = L / 2 - radius
        require(margin > 0, "nonempty feasible centre domain")
        minimum_domain_margin = margin if minimum_domain_margin is None else min(
            minimum_domain_margin, margin)

    require(0 < D < 1, "support domain")
    # Coefficient comparison of the M14 identity:
    # (1+D)^2(1+w^2)-(1+w)^2(1+D^2)=2(D-w)(1-Dw).
    left_coefficients = [2 * D, -2 * (1 + D * D), 2 * D]
    right_coefficients = [2 * D, -2 * (1 + D * D), 2 * D]
    require(left_coefficients == right_coefficients, "support identity")

    lambda_square = (1 + D * D) / (B * B * (1 + D) * (1 + D))
    endpoint_square = L * L * lambda_square
    lower, upper = decimal_bracket(endpoint_square, 20)
    radical = 180000000**2 + 207107**2
    radical_denominator = 9977 * (180000000 + 207107)
    require(endpoint_square == F(45900**2 * radical, radical_denominator**2),
            "endpoint radical form")
    require(isqrt(radical) ** 2 < radical < (isqrt(radical) + 1) ** 2,
            "endpoint radical irrationality")

    pilots = [{"grid_index": j, "t": ftext(grid[j]),
               "reason": ({1: "first interval and maximum angular-gap endpoint",
                           199: "midpoint across old minimum transition 99/100",
                           335: "midpoint across old minimum transition 167/168",
                           359: "terminal-adjacent midpoint"})[j]}
              for j in PILOT_INDICES]
    require(all(j % 2 == 1 for j in PILOT_INDICES), "pilot indices must be new rows")

    output = {
        "schema": "n17.m17.t2-stage-a-static-audit.v1",
        "status": "GO_CONDITIONAL_180_ODD_ROWS_UNCHECKED",
        "sweep_executed": False,
        "inherited": {
            "L": ftext(L), "B": ftext(B), "total_mass": ftext(total_mass),
            "atoms": len(atoms), "sites": len(measure), "symmetry": "D4",
            "old_direction_count": len(old_rows),
            "old_global_minimum": ftext(min(old_minima)),
            "old_rows_above_generalized_threshold": True,
        },
        "generalized_mass_counting": {
            "threshold": ftext(threshold),
            "strict_acceptance": "global_minimum > total_mass/17",
            "identity": "17*m > total_mass",
            "equality_is_insufficient": True,
        },
        "refined_grid": {
            "count": len(grid), "old_step_h": ftext(h), "new_step": ftext(d),
            "new_odd_rows": 180, "inherited_even_rows": 181,
            "first": ftext(grid[0]), "last": ftext(grid[-1]),
            "D": ftext(D), "D_equals_h_over_2": True,
            "maximum_D_interval": [0, 1],
            "endpoint_polynomial": ftext(endpoint_polynomial),
            "D4_fundamental_arc_covered": True,
        },
        "static_feasibility": {
            "rational_unit_directions_checked": len(grid),
            "nonempty_feasible_centre_domains": len(grid),
            "minimum_L_over_2_minus_probe_radius": ftext(minimum_domain_margin),
            "obvious_structural_impossibility_found": False,
            "coverage_quality_of_odd_rows": "UNKNOWN_UNTIL_EXACT_SWEEP",
        },
        "conditional_endpoint": {
            "condition": "all 180 odd-row exact minima are strictly greater than 423327/425000",
            "D": ftext(D), "lambda_square": ftext(lambda_square),
            "S_square": ftext(endpoint_square),
            "S_radical": f"45900*sqrt({radical})/{radical_denominator}",
            "positive_root_polynomial": {
                "x2": radical_denominator**2,
                "constant": -(45900**2 * radical),
            },
            "decimal_bracket_20": [lower, upper],
            "claim_if_condition_holds": "s(17) >= S",
            "endpoint_strict_certificate": False,
        },
        "frozen_pilot_proposal": {
            "status": "NOT_AUTHORIZED_NOT_RUN", "directions": pilots,
            "interpretation": (
                "A passing pilot proves only those rows. A row minimum <= threshold is an exact "
                "counterexample to this fixed-measure uniform-minimum certificate, not a global "
                "failure of all refinements. A timeout or checker error is inconclusive."
            ),
        },
        "bindings": {key: {"path": str(paths[key]), "sha256": sha256(paths[key])}
                     for key in paths},
        "checker_sha256": sha256(Path(__file__)),
        "claim_boundary": (
            "Static and conditional theorem audit only. No odd direction was swept, so no M17 "
            "lower bound is certified. Old rows are inherited only under exact byte/data bindings."
        ),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": output["status"], "report": str(report_path),
                      "report_sha256": sha256(report_path)}))


if __name__ == "__main__":
    main()
