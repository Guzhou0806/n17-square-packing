# M17 refined-direction certificate schema

## Purpose and status

This schema describes the evidence required to turn the stage-A conditional
theorem into a certified lower bound.  Stage A performs no new-direction sweep.
The schema is therefore not itself a certificate.

The proposal keeps the T-019 atom measure, `L=459/100` and `B=9977/10000`.
It interleaves the 181 old directions with 180 odd half-step directions:

```text
h = 207107/90000000
t_j = j*h/2,  j=0,...,360.
```

## Frozen acceptance threshold

Let

```text
M = 423327/25000
tau = M/17 = 423327/425000.
```

The required condition is the strict inequality

```text
global_minimum > tau.
```

It is not necessary to prove `global_minimum >= 1`.  If every disjoint probe
captures at least `m` and `m>tau`, then 17 probes capture at least `17m>M`,
contradicting total mass `M`.  Equality `m=tau` is insufficient.

This threshold must be frozen before any pilot or full sweep.  It may not be
selected after seeing the new rows.

## Candidate certificate

The future certificate should use the following top-level structure:

```json
{
  "schema": "n17.m17.refined-direction-certificate.v1",
  "status": "CANDIDATE_AWAITING_INDEPENDENT_CHECK",
  "bindings": {},
  "premise": {},
  "grid": {},
  "mass_counting": {},
  "coverage": {},
  "support_lemma": {},
  "strict_family": {},
  "endpoint": {},
  "claim_boundary": ""
}
```

### `bindings`

At minimum bind complete bytes of:

- T-019 source certificate;
- inherited 181-row direction output;
- M12 independent audit;
- M14 certificate and independent formal report;
- the frozen M17 protocol;
- producer source and independent checker source;
- the 180-row odd-direction output and final run report.

### `premise`

```json
{
  "n": 17,
  "L": "459/100",
  "B": "9977/10000",
  "total_mass": "423327/25000",
  "atom_count": 1184,
  "symmetry": "D4",
  "closed_probe": true,
  "nonnegative_weights": true
}
```

### `grid`

```json
{
  "old_h": "207107/90000000",
  "new_step": "207107/180000000",
  "indices": [0, 360],
  "direction_count": 361,
  "inherited_even_rows": 181,
  "new_odd_rows": 180,
  "D": "207107/180000000",
  "terminal": "207107/500000",
  "terminal_polynomial": "309449/250000000000"
}
```

The checker must regenerate every `t_j`, prove even row `2k` equals old row
`k`, and recompute

```text
max_j (t_(j+1)-t_j)/(1+t_j*t_(j+1)) = h/2.
```

It must also verify `terminal^2+2*terminal-1>0`, which is the exact endpoint
condition covering the D4 fundamental orientation interval through `pi/4`.

### `mass_counting`

```json
{
  "threshold": "423327/425000",
  "comparison": "strict_greater_than",
  "old_global_minimum": "200009/200000",
  "new_odd_global_minimum": "...",
  "all_361_global_minimum": "...",
  "counting_margin": "17*global_minimum-total_mass"
}
```

`counting_margin` must be a positive exact Fraction.

### Odd-row output

The 180-row JSONL output must contain exactly the odd indices in increasing
order.  Each row requires at least:

```json
{
  "grid_index": 1,
  "t": "207107/180000000",
  "minimum": "...",
  "minimum_minus_threshold": "...",
  "cell": ["...", "...", "...", "..."],
  "centre_uv": ["...", "..."],
  "centre_xy": ["...", "..."],
  "direct_count": "...",
  "direct_count_check": true,
  "complete_feasible_domain_checked": true,
  "u_events": 0,
  "v_events": 0,
  "strips": 0
}
```

The minimum witness is only a direct-attainment check.  Acceptance additionally
requires exhaustive exact coverage of the full feasible centre domain, using an
independent implementation or an independently verified complete cell
certificate.  Sampling, optimizer output and a witness alone are insufficient.

### `support_lemma`, `strict_family`, `endpoint`

The M14 identity is reused with `D=207107/180000000`:

```text
(1+D)^2(1+w^2)-(1+w)^2(1+D^2)
  = 2(D-w)(1-Dw) >= 0,  0<=w<=D<1.
```

For every positive rational `q` satisfying

```text
q^2 B^2 (1+D)^2 < 1+D^2,
```

the scaled probe is strictly inside its unit square.  If the coverage condition
passes, the endpoint limit is

```text
S = L*sqrt(1+D^2)/(B*(1+D))
  = 45900*sqrt(32400042893309449)/1797926306539
  in [4.59529705908773749818, 4.59529705908773749819).
```

The corresponding positive-root polynomial is

```text
3232539003744970194158521*x^2
  - 68260734368053280247690000 = 0.
```

The accepted statement would be `s(17)>=S`.  The proof does not supply a single
strict certificate at `q=S/L` and must not claim `s(17)>S`.

## Minimum independent acceptance

An independent checker must:

1. verify every byte binding and reject missing or additional run artifacts;
2. reconstruct the T-019 measure, D4 orbits, nonnegative weights and total mass;
3. recheck all inherited old rows and exact even-row identity;
4. require exactly 180 unique odd rows with the frozen `t_j` values;
5. independently recompute or exhaustively validate every odd direction over
   the complete feasible centre domain;
6. directly recount each reported minimum witness;
7. compute the global minimum and require it to be strictly greater than
   `423327/425000`;
8. independently recompute D4 endpoint coverage, `D=h/2`, support algebra,
   strict rational family, endpoint square/root and decimal bracket;
9. report timeouts, incomplete rows and verifier errors as inconclusive;
10. preserve the claim boundary: no world-record, novelty, optimizer, or
    endpoint-strictness claim.

## Failure and pilot semantics

- `minimum > 1`: passes both the legacy target and the generalized threshold.
- `tau < minimum < 1`: fails the unnecessary legacy target but **passes** the
  generalized mass-counting condition.
- `minimum = tau`: fails the strict counting argument.
- `minimum < tau`: fails the strict counting argument.
- An exact feasible centre with direct captured mass `<=tau` is a decisive
  counterexample to this fixed T-019 measure plus uniform-minimum certificate.
- Such a counterexample does not prove that every refined grid, modified
  measure, different `B`, or different lower-bound method fails.
- A passing pilot certifies only its fixed rows; it does not license the endpoint
  theorem while any odd row remains unchecked.

The proposed four-row pilot is frozen as indices `1,199,335,359`: first-gap,
the two old-minimum transition midpoints, and terminal-adjacent.  It remains
unauthorized and unrun at stage A.
