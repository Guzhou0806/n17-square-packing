# 0.1.0-m19 — release text prepared for GitHub

This evidence snapshot presents the M19 bound

`s(17) >= 45900*sqrt(73062612901466039895961496449)/2702984545455608711`.

The constant is enclosed by
`4.59004266897263595052 <= S19 < 4.59004266897263595053`.
This interval is not a two-sided enclosure of `s(17)`.

The complete M12 dependency, 1,184-atom source, 181 old directions, 17 M17 trials,
exact M17 failure witness, M19 certificate and final acceptance are included.
The 197-node M19 net retains 16 passing midpoint directions; the failed full
uniform refinement remains failed.

Run `python -X utf8 -B verify.py --output .replay-runs/full-001` from the root.
A separate optional adapter reruns the unchanged upstream NumPy sweep.
Packaging-time runs of both implementations agreed on all 198 checked directions,
including the expected failure. See `verification/PACKAGING_REPORT.md` for scope,
actual environment and outputs.

Credit: Joshua Levy's squares project supplies the weighted certificate, source
coverage method and dilation-limit argument. The incremental M19 content is the
specified nonuniform-net coverage evidence, preserved failure and numerical
corollary. No external priority, new general method, endpoint infeasibility,
optimality, or upstream endorsement is claimed.

This file is a proposed Release description; creating the actual GitHub Release
is a separate maintainer action.
