# M19 deterministic implication pre-review

## Verdict

`GO_PENDING_T1_INDEPENDENT_17_ROW_FULL_REPLAY`.

M19 is a separate post-M17 deterministic implication.  M17 remains failed at
old interval 14; the failed midpoint is not relabelled as passing and the M17
protocol is not changed.

## Fixed input set

The 16 producer-reported passing old-interval midpoints are exactly

```text
0,1,2,...,13,89,179.
```

M19 retains all 16, drops none according to quality, adds no new direction and
does not modify atoms, weights or `B`.  Combined with the 181 inherited nodes,
the fixed nonuniform net has 197 distinct nodes and 196 adjacent gaps.

## Independent grid result

All 196 gaps were regenerated as exact Fractions.  The unique maximum is the
unsplit old interval `[14h,15h]`:

```text
D19 = h/(1+14*15*h^2)
    = 621321000000/270300253166143
    < 207107/90000000 = D14.
```

The full ordered gap list and its canonical hash are in
`M19_STATIC_PRECHECK_ATTEMPT_002.json`.

Conditional on independent full-domain coverage of every retained midpoint,
the unchanged M14 support lemma gives

```text
s(17) >= 45900*sqrt(73062612901466039895961496449)
         /2702984545455608711
       ∈ [4.59004266897263595052, 4.59004266897263595053).
```

This would improve M14 by approximately `0.00001167910610349934`, without
recovering the failed full-midpoint M17 endpoint.

## Required evidence before acceptance

The 16 producer rows currently contain a claimed full minimum and a direct
minimum witness.  A witness proves attainability, not a lower bound over the
entire feasible centre domain.  M19 must remain pending until:

1. the locked T1 two-dimensional difference-sweep implementation independently
   replays all 17 observed M17 directions, including the failure;
2. all direction values, complete-domain minima and direct witnesses agree row
   by row with the frozen M17 output;
3. source, implementation, protocol and result hashes are frozen before formal
   certificate assembly;
4. the formal checker regenerates all 197 nodes and 196 gaps rather than trusting
   a declared maximum;
5. old 181-row inheritance, D4, total mass, threshold, support identity, endpoint
   square/root and decimal bracket are independently rebound and checked.

Any mismatch is a stop, not permission to select a better-looking subset.  A
timeout or implementation error is inconclusive.

## Boundary

M19 is not a new search and does not rehabilitate M17.  It is a deterministic
consequence of a fixed set of already observed rows, if and only if complete
independent coverage evidence for those rows is accepted.  It does not prove
optimality, novelty or a world record.
