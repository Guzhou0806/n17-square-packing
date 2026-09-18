"""Directed tests for the independent M19 checker; no sweep is executed."""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import check_m19 as audit


ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name("M19_DIRECTED_TESTS_FINAL.json")


def main() -> None:
    if OUT.exists():
        raise AssertionError(f"refusing to overwrite {OUT}")
    source = audit.read_json(ROOT / audit.PATHS["source"])
    t0_rows = audit.read_jsonl(ROOT / audit.PATHS["m17_rows"])
    t1_rows = audit.read_jsonl(ROOT / audit.PATHS["t1_rows"])
    cert = audit.read_json(ROOT / audit.PATHS["m19_certificate"])
    L, B = F(source["outer_side"]), F(source["square_side"])
    total = F(source["total_mass"])
    threshold = total / 17
    h = F(source["angle_limit"]) / source["direction_steps"]
    atoms = [(F(x), F(y), F(weight)) for x, y, weight in source["atoms"]]
    results = []

    def check(name, condition, evidence):
        assert condition, name
        results.append({"name": name, "status": "PASS", "evidence": evidence})

    t0_masses = [audit.direct_witness_mass(atoms, L, B, F(row["t"]), row["centre_uv"])[0]
                 for row in t0_rows]
    check("all_T0_witnesses_recount",
          t0_masses == [F(row["minimum"]) for row in t0_rows],
          "17 exact atom-by-atom recounts equal the saved minima")

    t1_masses = [audit.direct_witness_mass(atoms, L, B, F(row["t"]), row["centre_uv"])[0]
                 for row in t1_rows]
    check("all_T1_witnesses_recount",
          t1_masses == [F(row["source_minimum"]) for row in t1_rows],
          "17 independent replay witnesses exactly recount")

    differing_centres = sum(t0["centre_uv"] != t1["centre_uv"]
                            for t0, t1 in zip(t0_rows, t1_rows))
    check("witness_coordinates_need_not_match",
          differing_centres > 0 and t0_masses == t1_masses,
          f"{differing_centres} row(s) use different centres while all minima agree")

    passing = [row for row in t0_rows if F(row["minimum"]) > threshold]
    failing = [row for row in t0_rows if F(row["minimum"]) <= threshold]
    check("strict_threshold_partition",
          len(passing) == 16 and [row["refined_index"] for row in failing] == [29],
          "strict > threshold keeps 16 rows and retains the k=14 failure")

    old_nodes = [k * h for k in range(181)]
    selected = sorted(set(old_nodes + [F(row["t"]) for row in passing]))
    contaminated = sorted(set(selected + [F(failing[0]["t"])]))
    check("failed_direction_is_not_silently_selected",
          len(selected) == 197 and len(contaminated) == 198 and
          [F(value) for value in cert["directions"]] == selected,
          "adding failed refined index 29 would visibly change the certificate node count")

    gaps = [(right - left) / (1 + left * right)
            for left, right in zip(selected, selected[1:])]
    D = max(gaps)
    check("all_gap_max_not_hardcoded",
          len(gaps) == 196 and gaps.count(D) == 1 and
          D == F(cert["maximum_gap"]) and
          selected[gaps.index(D):gaps.index(D) + 2] == [14 * h, 15 * h],
          "enumeration finds one maximum at the first unrefined interval")

    side_square = L * L * (1 + D * D) / (B * B * (1 + D) ** 2)
    lower, upper = map(F, cert["decimal_bracket_20"])
    check("exact_decimal_bracket",
          lower * lower < side_square < upper * upper and
          upper - lower == F(1, 10**20),
          "20-place neighboring decimals strictly bracket the positive root")

    check("claim_boundary_preserved",
          cert["endpoint_certificate"] is False and
          cert["claims_strict_endpoint_infeasibility"] is False and
          cert["M17_uniform_refinement_status"] == "FAILED_AND_RETAINED",
          "M19 is an ordinary >= implication and does not repair M17")

    output = {
        "schema": "n17.m19.t2-directed-tests.v1",
        "status": "PASS",
        "test_count": len(results),
        "tests": results,
        "sweep_executed": False,
        "checker_sha256": hashlib.sha256(Path(audit.__file__).read_bytes()).hexdigest(),
        "certificate_sha256": hashlib.sha256(
            (ROOT / audit.PATHS["m19_certificate"]).read_bytes()).hexdigest(),
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"], "tests": len(results),
                      "output": str(OUT),
                      "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
