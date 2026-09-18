# Evidence map

## Minimal reading path

1. [English theorem](M19_PROOF_EN.md).
2. [Original final acceptance](../evidence/M19/FINAL_ACCEPTANCE.json) and
   [machine certificate](../evidence/M19/research/m19_work/CERTIFICATE.json).
3. [Full reproduction guide](REPRODUCIBILITY.md), then `verify.py` at the root.
4. [Fresh assembly-time records](../verification/PACKAGING_REPORT.md).

## Exact file map

| Purpose | Frozen location |
|---|---|
| 1,184 atoms and rational weights | `evidence/M19/workers/T1/outputs/m10_m11/global_followup/certificate.json` |
| Same source bound into formal audit | `evidence/M19/coord/m14_m15/inputs/SOURCE_T019.json` |
| 181 old-direction records | `evidence/M19/research/m12_work/run_001/DIRECTIONS.jsonl` |
| M17's 17 additional records | `evidence/M19/research/m17_work/run_001/DIRECTIONS.jsonl` |
| M17 failure summary | `evidence/M19/research/m17_work/run_001/RESULT.json` |
| M19 gap and endpoint certificate | `evidence/M19/research/m19_work/CERTIFICATE.json` |
| Original certificate producer | `evidence/M19/research/m19_work/produce_certificate.py` |
| Standard-library full coverage implementation | `evidence/M19/research/m12_work/independent_sweep.py` |
| M19 saved-evidence arithmetic/witness checker | `evidence/M19/workers/T2/outputs/m17_lower/check_m19.py` |
| Accepted M19 audit | `evidence/M19/workers/T2/outputs/m17_lower/M19_FORMAL_REPORT.json` |
| 17-row historical source replay | `evidence/M19/workers/T1/outputs/m17_m18/m19_replay/` |
| Complete M12 dependency | `evidence/M19/research/proofs/M12_global_lower_bound/` |
| Preserved upstream license | `evidence/M19/research/proofs/M12_global_lower_bound/UPSTREAM_LICENSE.txt` |
| Original upload mapping | `provenance/INPUTS.json` |
| New frozen-evidence inventory | `EVIDENCE_MANIFEST.json` |
| Original ZIPs | `archives/` |

The separately uploaded M12 ZIP contains the same 57 files, with identical bytes,
as the M12 package nested inside M19. It is not copied to a second expanded location.
The separately uploaded atom certificate, M12/M17 rows, M17 result and final
acceptance also match the existing M19 files exactly.

## Why the historical paths are retained

The original checkers infer their package root from their own locations and bind
many paths by SHA-256. Flattening those folders or rewriting their files would
break that provenance. The new root entry point provides a simple interface while
keeping all 129 extracted M19 files intact. Some retained protocol documents refer
to the wider private research project; only M12/M17/M19 coverage and M19's endpoint
are part of this release's replay claim. Incidental M18 receipts are not an M18
proof package.

A hash proves byte identity relative to the chosen manifest, not mathematical
correctness or an authenticated publication date. A record stating `PASS` is not
used in place of actually rerunning the default coverage path.
