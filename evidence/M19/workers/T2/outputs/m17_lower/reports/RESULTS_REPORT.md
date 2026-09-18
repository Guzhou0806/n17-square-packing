# M17 failure audit and M19 final independent acceptance

## Outcome

- M17 full 361-node midpoint refinement: **rejected by exact counterexample**.
- M19 fixed 197-node nonuniform consequence: **accepted by independent exact
  verification**.

No sweep was rerun by T2.

## M17 exact counterexample

The frozen run stopped at its 17th computed new direction:

```text
old interval index: 14
refined grid index: 29
t:                  6006103/180000000
```

The reported centre was independently checked in both `(x,y)` and rotated
`(u,v)` coordinates.  It lies strictly inside the feasible centre domain and
strictly inside the reported open event cell.  All four probe corners are
strictly inside the `L=459/100` container.

An independent closed-boundary loop over all 1184 T-019 atoms captures exactly
125 atoms and gives

```text
direct mass          = 197153/200000 = 0.985765
frozen threshold     = 423327/425000 ≈ 0.9960635294
mass - threshold     = -7003/680000
17*mass - total mass = -7003/40000.
```

No captured atom lies exactly on the probe boundary.  The full captured-atom
index and weight list is preserved in `M17_FAILURE_AUDIT_ATTEMPT_002.json`.

This single legal centre disproves the universal requirement for that direction;
it is unnecessary to accept the producer's stronger claim that the point is a
global minimum.  Thus the fixed T-019 measure, fixed `B`, full 180-midpoint
refinement cannot support the proposed M17 counting certificate.

## M17 scope

The result does not show that stronger lower bounds are impossible.  It does not
exclude another measure, a different probe size, nonuniform directions or a
different counting theorem.  The first 16 reported passing directions are
preserved as data, while M17 itself remains failed.

## M19 deterministic nonuniform grid

M19 separately freezes the 16 producer-reported passing midpoint intervals
`0..13,89,179` and merges them with all 181 old nodes.  Exact regeneration gives:

| Quantity | Exact result |
|---|---|
| old nodes | 181 |
| retained midpoint nodes | 16 |
| total distinct nodes | 197 |
| adjacent gaps | 196 |
| unique largest gap | old interval `[14h,15h]` |
| `D19` | `621321000000/270300253166143` |

All 196 exact gap records are stored in `M19_STATIC_PRECHECK_ATTEMPT_002.json`.
The maximum is strictly smaller than M14's `h=207107/90000000`.

T1's independently implemented two-dimensional difference sweep replayed
exactly the 17 frozen M17 rows, with no new direction.  All 17 full-domain
minima matched exactly: 16 retained rows pass the strict threshold, while the
failed refined index 29 remains failed.  T2 separately recounted every saved
T0 and T1 witness atom by atom; the two implementations are allowed to return
different minimizing centres.

The inherited M14 strict-dilation argument therefore yields

```text
s(17) >= 45900*sqrt(73062612901466039895961496449)
         /2702984545455608711
       ∈ [4.59004266897263595052, 4.59004266897263595053).
```

This is an ordinary `>=` lower bound obtained as a limit of strict dilations.
It is not a certificate that the endpoint itself is infeasible.

## Verification

The earlier six M17/static-precheck checks passed.  Eight final M19 directed
checks also passed: all 17 T0 witnesses recount; all 17 T1 witnesses recount;
different valid minimizing centres are accepted; the strict threshold gives the
fixed 16/1 partition; adding the failed midpoint visibly changes the certified
node set; all 196 gaps give the unique maximum at `[14h,15h]`; the exact
neighboring 20-place decimals strictly bracket the positive root; and the claim
boundary preserves both M17 failure and the absence of endpoint infeasibility.

## Reproduction

```powershell
python workers/T2/outputs/m17_lower/audit_m17_failure_m19_static.py `
  --root . `
  --m17-report <new-m17-report> `
  --m19-report <new-m19-report>
```

The program refuses to overwrite reports.  It performs only direct atom counting
and exact grid/algebra checks; it never calls either sweep implementation.

Final M19 acceptance can be reproduced, again to a fresh report path, with:

```powershell
python workers/T2/outputs/m17_lower/check_m19.py `
  --root . `
  --report <new-m19-formal-report>
```

The final checker does not import or execute the T0 producer or T1 harness and
does not launch a sweep.  It binds their frozen source/output hashes, compares
the saved per-direction minima, directly validates both sets of witnesses, and
reconstructs the complete certificate arithmetic.

## Visualization decision

No chart is generated.  The decisive result is a single exact rational
counterexample and M19 depends on a 196-entry exact maximum comparison.  A chart
would not add proof value and could obscure the strict threshold distinction.

## Claim boundary

M17 is rejected only in its fixed form.  M19 certifies only the stated ordinary
lower bound for the frozen T-019/M12/M14 inheritance chain.  Neither result
establishes optimality, novelty, world-record status or an endpoint-strict
inequality.
