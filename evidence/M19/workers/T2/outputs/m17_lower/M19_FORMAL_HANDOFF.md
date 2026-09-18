# M19 independent-verification handoff

Status: `PASS_M19_NONUNIFORM_GRID_LOWER_BOUND`.

T1 replayed exactly the 17 frozen M17 rows with an independent full-domain
implementation: 16 strict passes and the retained refined-index-29 failure all
match T0 exactly.  T2 did not execute a sweep.  The final checker instead bound
both implementations and outputs by SHA-256, directly recounted all 34 saved
witnesses, reconstructed the deterministic 197-node set and all 196 gaps, and
verified the inherited M14 endpoint algebra.

Accepted claim:

```text
s(17) >= sqrt(
  153929043486937667513210640333717690000
  /7306125452971863634008322287539081521
)
in [4.59004266897263595052, 4.59004266897263595053).
```

The unique maximum gap is
`621321000000/270300253166143`, between
`1449749/45000000` and `207107/6000000` (old interval `[14h,15h]`).
The retained minimum mass is `200009/200000`, with exact counting slack
`17m-M = 13537/200000 > 0`.

Claim boundary: this is a non-strict endpoint lower bound obtained via the
inherited strict-dilation family.  It does not prove endpoint infeasibility, does
not repair M17, and includes no new searched direction.

Primary evidence:

- `M19_FORMAL_REPORT.json`
- `M19_DIRECTED_TESTS_FINAL.json`
- `check_m19.py`
- `reports/RESULTS_REPORT.md`
