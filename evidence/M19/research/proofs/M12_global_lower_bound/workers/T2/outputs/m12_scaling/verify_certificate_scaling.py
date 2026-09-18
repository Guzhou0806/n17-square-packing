"""Exact field-by-field binding check for T1's scaled M12 certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ORIGINAL = ROOT / "workers/T1/outputs/m10_m11/global_followup/certificate.json"
SCALED = ROOT / "workers/T1/outputs/m10_m11/global_followup/m12/results/scaled_certificate.json"
LAMBDA = F(1000001, 1000000)
ORIGINAL_SHA = "461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652"
SCALED_SHA = "6979561eb5137270f7baabc782cafc0580f3483a9bfcdf47fef427484285980c"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert digest(ORIGINAL) == ORIGINAL_SHA
    assert digest(SCALED) == SCALED_SHA
    original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    scaled = json.loads(SCALED.read_text(encoding="utf-8"))
    invariant = {"n", "angle_limit", "direction_steps", "total_mass",
                 "least_cell_mass", "symmetry"}
    for field in invariant:
        assert original[field] == scaled[field], field
    assert F(scaled["outer_side"]) == LAMBDA * F(original["outer_side"])
    assert F(scaled["square_side"]) == LAMBDA * F(original["square_side"])
    assert len(original["atoms"]) == len(scaled["atoms"]) == 1184
    for index, (before, after) in enumerate(zip(original["atoms"], scaled["atoms"])):
        x, y, weight = map(F, before)
        sx, sy, scaled_weight = map(F, after)
        assert (sx, sy, scaled_weight) == (LAMBDA * x, LAMBDA * y, weight), index
    report = {
        "schema": "n17.m12.t2-scaling-binding.v1",
        "status": "PASS",
        "lambda": str(LAMBDA),
        "atoms_checked": len(original["atoms"]),
        "invariant_fields_checked": sorted(invariant),
        "original_sha256": digest(ORIGINAL),
        "scaled_sha256": digest(SCALED),
        "source_sha256": digest(Path(__file__)),
    }
    output = Path(__file__).with_name("ATTEMPT_001_SCALING_BINDING.json")
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "report_sha256": digest(output)}))


if __name__ == "__main__":
    main()
