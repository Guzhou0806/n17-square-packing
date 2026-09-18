# M12 independent code and mathematics audit

Date: 2026-09-17  
Scope: T0 exact sweep, endpoint/cell logic, fixed scaling theorem, and T0/T1 output agreement. No packing search or optimization was performed.

## Verdict

`PASS_FOR_REGISTRATION`.

No correctness defect or unsafe acceptance path was found. The fixed instance supports

`s(17) >= 459000459/100000000 = 4.59000459`.

This verdict is limited to the locked T-019 certificate, fixed
`lambda=1000001/1000000`, the frozen 181-direction net, and the stated exact arithmetic. It does not establish novelty, priority, or a stronger value of lambda.

## Frozen bindings

- T-019 input SHA-256: `461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652`.
- T0 sweep source SHA-256: `1ddb94bb2a1a0350489752c44a5e9c4622c247f0142570fa5b622675ca652b38`.
- T0 result SHA-256: `5fa6210087f3e2c2ac8bb98053f88358051fdfdc4ccc2e6301661648edffc7b0`.
- T0 directions SHA-256: `2883a709797923e7ce0b9889ab946e7399e52d7db5c866ba3faf71f3ca712fa4`.
- T1 source result SHA-256: `4ad6d4fff965e014a1aba2947ee404eb0987fca2606a7125a58286cf8971e3e0`.
- T1 scaled result SHA-256: `d0725160831f743e967083054dac76a5d49ce01577d32404c055e0f8662aee02`.
- T1 comparison SHA-256: `f45ad7ef4131198621ea76e2982b3db58032da83921c86b8dfffca4454fcc347`.

## Code audit

The T0 implementation satisfies the necessary contracts:

1. All geometry is `Fraction`; weights are put over an exact common denominator and the range tree stores integers.
2. Equal-u start/end events are grouped and applied before querying the next open strip. Event lines themselves are correctly omitted because weights are nonnegative and capture rectangles are closed.
3. Polygon-vertex u coordinates split the feasible polygon exactly where its affine upper or lower boundary can change. Therefore the minimum lower endpoint and maximum upper endpoint over a strip are attained at strip endpoints.
4. The queried v-leaf interval is exactly the set of open v-cells with positive-length intersection with the whole strip projection. `bisect_right(...)-1` at the lower endpoint and `bisect_left(...)` at the upper endpoint handle equality in the safe direction.
5. Polygon vertex v coordinates are included, so regions beyond every atom v-event remain represented and can expose coverage zero.
6. The lazy range-add/range-min and `argmin` carry invariants are correct. An independent array oracle checked every subrange after five overlapping add/remove operations.
7. The selected minimum cell is clipped against the feasible polygon, an exact rational interior point is produced, and all atoms are recounted directly at that point.
8. Static gates reject negative weight, missing D4 orbit, insufficient direction endpoint, and failed strict-containment margin.
9. The input byte hash is checked before the full run, so permissive JSON-to-`Fraction` parsing cannot silently widen this fixed-instance claim.

## Independent exact fixture audit

The frozen T2 test source has SHA-256
`1858a6fef3537dbba004eccf7fdf39b1c923a31e203433de6e7eac2d9cb7d81c`.
Its first execution passed all 13 tests; report SHA-256 is
`b5c2bb56ad69d0e21895797be4e4cb13435826953da282515da40083e58fc9af`.

The independent oracle does not reuse T0's rotation, clipping, projection, or tree implementation. It constructs every rectangle-event cell, clips the feasible polygon against each cell with a separately written exact half-plane routine, discards zero-area contacts, takes a rational interior point, and directly sums weights.

Covered cases:

- coincident rectangle starts and an end/start tie at one u event;
- a feasible zero-mass region outside all atom events;
- cells intersecting the feasible polygon only near a strip endpoint while their rectangle midpoint lies outside it;
- `t=0` and the last net direction, which is slightly beyond `pi/4`;
- an exact synthetic dilation bijection;
- D4 pass/failure, negative-weight rejection, direction-endpoint failure, and lambda containment failure;
- complete T0/T1-original/T1-scaled 181-direction comparison.

## Full-output comparison

All three exact direction vectors are identical, index by index:

- T0 independent sweep;
- T1 locked-source replay of the original certificate;
- T1 locked-source replay of the explicitly scaled certificate.

There are 181 entries and no mismatch. The minimum is `200009/200000`; the distribution is 113 entries at `200009/200000` and 68 entries at `50003/50000`.

The scaled certificate was also checked field by field, not only through its verifier result: all 1184 coordinates equal lambda times the corresponding original coordinate, all 1184 weights are unchanged, `outer_side` and `square_side` are multiplied by lambda, and the six invariant metadata fields are unchanged. The frozen binding script SHA-256 is
`9a0d907cc01afb7198144d0babfb3b39c8e29f47fa9eb10a412ae2563e12eaa9`; its first-run report SHA-256 is
`cc33c64e74331888acfd38ac581790819efbea095dd864778094fd1d45bbc7a6`.

## Mathematical audit

For a fixed direction, each atom contributes a closed B-by-B rectangle in centre space. The coverage sum is constant on each open arrangement cell. Because all weights are nonnegative and the rectangles are closed, the value at an event line or feasible-domain boundary is at least the limiting value from a neighboring generic interior sequence. Thus the minimum over the closed feasible polygon is bounded below by the enumerated open-cell minimum. The feasible polygon has nonempty interior because `r<S/2` is checked exactly.

The half-tangent grid covers the full D4 fundamental interval: the last t satisfies
`t^2+2t-1=309449/250000000000>0`. For adjacent half-tangents, the tangent of half their angle difference is
`(t_(k+1)-t_k)/(1+t_k*t_(k+1))`; its maximum is
`D=207107/90000000`. Hence a nearest net direction differs by delta with
`tan(abs(delta))<=D`, and `cos(delta)+abs(sin(delta))<=1+D`.

For the scaled probe,

`1-B'(1+D)=2793464693461/900000000000000000>0`.

Therefore every unit square strictly contains the same-centre B' probe at a nearest net direction. Exact dilation is a bijection between the original and scaled feasible-centre domains and preserves each atom/probe incidence. The 181-direction lower mass is therefore unchanged.

If 17 unit squares had pairwise disjoint interiors, their strictly interior closed probes would be pairwise disjoint. Each captures mass greater than 1, while the total atom mass is
`423327/25000<17`; no atom can be counted by two disjoint probes. This is the required contradiction.

## Source-faithful replay qualification

T1 ran under Python 3.12 although the source project declares Python 3.14. The only compatibility wrapper supplies missing `os.process_cpu_count` as `os.cpu_count`. The replay explicitly requests one worker; the locked `_worker_count` takes a minimum containing that requested value, so the result is necessarily one and the shim cannot alter geometry, direction order, or arithmetic. The original pre-direction failure was retained. This environment deviation does not weaken the numerical comparison.

## Remaining limits

- This is a fixed-instance certificate audit, not a proof that larger scaling factors fail or succeed.
- The independent small fixtures validate algorithmic edge cases; the full 1184-atom assurance comes from the complete T0 exact run plus a structurally separate source-faithful T1 run.
- External priority and literature coverage remain unknown, as already stated in the proof draft.

