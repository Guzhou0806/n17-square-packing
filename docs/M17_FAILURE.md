# M17: retained failed uniform refinement

M17 fixed the T-019 atoms, weights and probe side `B=9977/10000`, then proposed
adding all 180 midpoints to the old 181-direction net. Its frozen order began with
old intervals `0, 89, 179`, followed by the other intervals in order.
It stopped after 17 computed new directions.

The last of those directions is old interval `k=14`, refined index `29`,
with half-tangent parameter `t = 29 * 207107 / 180000000`.
At the saved legal probe center, the captured mass is

```text
197153/200000 < (423327/25000)/17 = 423327/425000.
```

The exact direct recount captures 125 atoms. This single feasible probe refutes the
required uniform coverage condition for **that fixed measure, probe, and proposed
full net**. It does not refute every possible refinement, a different probe size,
a reweighting, or a stronger global packing lower bound.

- [All 17 exact rows, including center coordinates](../evidence/M19/research/m17_work/run_001/DIRECTIONS.jsonl)
- [Negative result record](../evidence/M19/research/m17_work/run_001/RESULT.json)
- [Precomputation conditional theorem](../evidence/M19/research/m17_work/THEOREM_DRAFT.md)
- [Independent failure audit](../evidence/M19/workers/T2/outputs/m17_lower/M17_FAILURE_AUDIT_ATTEMPT_002.json)

M19 subsequently retained **all and only** the 16 passing midpoint rows, covering
old intervals `0..13, 89, 179`. No failed row was silently promoted. The combined
net has 197 nodes, and its largest unsplit gap is still the interval `[14h,15h]`.
The failure remains a required replay outcome, even when the M19 result passes.
