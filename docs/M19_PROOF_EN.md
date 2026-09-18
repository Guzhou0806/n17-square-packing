# M19: A nonuniform-direction-net refinement of the n = 17 lower bound

This is an English presentation of the supplied M19 and M12 proofs. The
[original Chinese M19 proof](../evidence/M19/PROOF.md) remains unchanged.
No mathematical conclusion has been strengthened in translation.

The [final acceptance](../evidence/M19/FINAL_ACCEPTANCE.json) and the dependencies
previously missing from the preliminary note are now included. Packaging-time
executions and their scope are recorded separately in
[PACKAGING_REPORT.md](../verification/PACKAGING_REPORT.md).
The producer-stage status in the original JSON is historical, not edited away.
External priority is not established. No strict endpoint or global-optimality
statement is made.

## 1. Theorem

Let s(17) denote the infimum of side lengths of square containers that hold seventeen unit squares, with arbitrary rotations and disjoint interiors. Boundary contact is allowed.

The M19 result is

$$
s(17)\ge S_{19}:=
\frac{45900\sqrt{73062612901466039895961496449}}
     {2702984545455608711}.
$$

Its exact square is

$$
S_{19}^{2}=
\frac{153929043486937667513210640333717690000}
     {7306125452971863634008322287539081521}.
$$

Exact integer comparisons give

```text
4.59004266897263595052 <= S19 < 4.59004266897263595053.
```

This is a bracket for the **lower-bound constant S19**, not a two-sided bracket for s(17).

## 2. Frozen measure and inherited coverage

The source is the T-019 weighted-atom certificate from Joshua Levy's `squares` project, pinned in the local project to commit

```text
035d84c655b4047bc9986c9a3db5106780d92f77
```

The source certificate bytes are identified by SHA-256

```text
461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652
```

The fixed parameters are

$$
L=\frac{459}{100},\qquad
B=\frac{9977}{10000},\qquad
M=\frac{423327}{25000},\qquad
m=\frac{200009}{200000}.
$$

There are 1184 nonnegative rationally weighted atoms. Their measure is D4-symmetric in the container [0,L]^2. The atoms, their weights, and the probe side B are unchanged in M19.

Put

$$
h=\frac{207107}{90000000},\qquad
t_k=kh\quad(0\le k\le180),\qquad
\theta_k=2\arctan(t_k).
$$

The inherited M12 coverage statement is that every closed B-square of each of these 181 directions, at every center for which that square lies in [0,L]^2, captures mass at least m.

M12 describes a complete finite event-cell sweep of the continuous center domain, not a finite sample of centers. In probe coordinates, each atom is captured on a closed rectangle of centers. Rectangle events and the feasible-center polygon divide the domain into cells on which the captured mass is constant. The project reports exact rational geometry and integer weight arithmetic. Closed capture sets, nonnegative weights, and a full-dimensional feasible-center domain are used to extend the interior-cell bound to event lines and the feasible boundary. The default release command recomputes the complete-center coverage, rather than inferring it from a stored minimum alone.

## 3. The failed uniform refinement and the retained directions

The M17 attempt kept the measure and B fixed and proposed adding all 180 half-step nodes, which would have formed a 361-node uniform net in the t parameter.

The retained M17 record gives a failure in old interval k = 14, at the midpoint with refined index 29: a feasible closed B-probe captures only

$$
\frac{197153}{200000}
<\frac{M}{17}=\frac{423327}{425000}.
$$

The saved direct-witness checks identify 125 captured atoms. Its exact center is in the retained M17 direction row; the M19 checker recounts it atom by atom. A single such witness is sufficient to refute the required uniform-coverage premise; proving that it attains the global minimum is unnecessary for that refusal.

Before stopping, 16 additional midpoint directions had passed. They are the midpoints of old intervals

$$
K=\{0,1,\ldots,13,89,179\}.
$$

M19 uses all of those passed midpoints together with the old 181 nodes, for a total of 197 directions. It is a separately recorded reuse of the M17 results, not a reclassification of the failed M17 goal as a success.

The project reports that a standard-library rational event sweep with an integer segment tree and the pinned-source NumPy two-dimensional difference sweep agree on all 17 computed new directions: 16 passed minima equal to m and one failed value. The full-center checks for the passed directions are a computational premise of the theorem.

## 4. Exact angular error of the nonuniform net

For adjacent t values a < b, the tangent of half their actual direction-angle separation is

$$
\frac{b-a}{1+ab}.
$$

For the original interval k, this becomes

$$
d_k=\frac{h}{1+k(k+1)h^2}.
$$

It decreases with k. The first fourteen old intervals have been split, and each resulting subgap has half-angle tangent at most h/2. The earliest unsplit interval is k = 14, whose d_14 is greater than h/2. Consequently, the maximum over the 196 adjacent gaps is

$$
D=d_{14}=\frac{621321000000}{270300253166143}<h.
$$

The supplied certificate also enumerates every adjacent gap and the pair attaining the maximum, so this value can be checked directly without relying only on the monotonicity argument.

The endpoint t_180 = 207107/500000 satisfies

$$
t_{180}^{2}+2t_{180}-1
=\frac{309449}{250000000000}>0,
$$

so the net extends beyond direction pi/4. By symmetry of the measure and container, any probe-orientation coverage question reduces to the interval [0,pi/4]. This does **not** assume that a packing itself has D4 symmetry. The distance delta to a nearest available direction obeys tan|delta| <= D.

## 5. Strict containment and the mass contradiction

For 0 <= w <= D < 1,

$$
(1+D)^2(1+w^2)-(1+w)^2(1+D^2)
=2(D-w)(1-Dw)\ge0.
$$

Putting w = tan|delta| gives

$$
\cos\delta+|\sin\delta|
\le\frac{1+D}{\sqrt{1+D^2}}.
$$

Choose any positive rational q satisfying

$$
q^2B^2(1+D)^2<1+D^2.
$$

Dilate the container and atom coordinates by q, without changing the weights. Inverse dilation preserves each verified grid-direction coverage statement. Every unit square strictly contains a concentric closed square of side qB at a nearest grid direction; that probe is also inside the container whenever the unit square is.

If seventeen unit squares with disjoint interiors fitted in a container of side qL, their strictly interior closed probes would be pairwise disjoint. Each would capture mass at least m, whereas their total captured mass could not exceed M. This contradicts

$$
17m-M=\frac{13537}{200000}>0.
$$

Strict containment is essential: boundary contact between unit squares must not permit an atom to be counted by two probes.

## 6. Passing to the limiting lower bound

Define

$$
c=\frac{\sqrt{1+D^2}}{B(1+D)},\qquad S_{19}=cL.
$$

Every positive rational q < c gives an excluded side qL. For any nonnegative real x < S19, rational density supplies x/L < q < c. A packing in side x would embed in the larger square of side qL, a contradiction. Therefore s(17) >= S19.

This reasoning does not require a strict-containment certificate at q = c. It does not prove that s(17) > S19 or that a packing at S19 is impossible.

## 7. Contribution and attribution

The weighted measure and source coverage method are inherited from Joshua Levy's `squares` project. The sharpened dilation-limit argument is inherited from the source T-022 argument and its local M14 application. M19's incremental content is the added complete-coverage evidence for a specified nonuniform 197-node direction net, the preserved M17 failure witness, and the resulting n = 17 numerical corollary.

The supplied certificate records the previous M14 square as

```text
17065251368053280247690000/809993351783841654158521
```

and an exact positive difference between the new and old squares. The resulting increment over M14 is approximately 0.00001167910610349934.

The project's source-attribution notes state MIT terms for source code and applicable CC BY 4.0 terms for source documents/data. The original notices, pinned source snapshot, and transformation record are included in the nested M12 evidence package. This note does not assign new blanket terms to those materials.


## 8. Evidence and actual replay commands

From the repository root:

```bash
python -X utf8 -B verify.py --output .replay-runs/full-001
```

This runs both inherited and newly added coverage computations from the atom
coordinates, then the bound checks. The [evidence map](EVIDENCE_MAP.md) identifies
all frozen files. The [reproduction guide](REPRODUCIBILITY.md) distinguishes quick
checks, full standard-library replay, and the optional NumPy implementation.

The exact failure witness is preserved at
[evidence/M19/research/m17_work/run_001/DIRECTIONS.jsonl](../evidence/M19/research/m17_work/run_001/DIRECTIONS.jsonl)
in the row with `refined_index = 29`. Event-cell traversal, not direct counting
at a finite set of witnesses, supplies the universal center-coverage premise.

This text is a presentation layer. A passing replay is evidence under the stated
mathematical reduction and program correctness; it is not a proof-assistant kernel
check, an expert endorsement, or a priority certificate.
