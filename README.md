# n = 17 square packing — M19 lower-bound evidence

A research evidence snapshot for packing seventeen rotatable unit squares into a square.
**This release concerns M19, not a claim of the strongest currently known bound.**

[English proof](docs/M19_PROOF_EN.md) ·
[Results](RESULTS.md) · [Reproduction](docs/REPRODUCIBILITY.md) ·
[Evidence map](docs/EVIDENCE_MAP.md) · [Attribution](NOTICE.md)

## Result

Let $s(17)$ be the infimum of container side lengths that can hold 17 unit squares
with arbitrary rotations and disjoint interiors; boundary contact is allowed.
The released M19 statement is

$$
s(17)\ge S_{19}:=
\frac{45900\sqrt{73062612901466039895961496449}}
{2702984545455608711}.
$$

The exact enclosure of **the constant $S_{19}$**, not of $s(17)$, is

```text
4.59004266897263595052 <= S19 < 4.59004266897263595053.
```

The project acceptance is [CL-M19-001](evidence/M19/FINAL_ACCEPTANCE.json).
It binds the [original certificate](evidence/M19/research/m19_work/CERTIFICATE.json)
to the accepted audit. The certificate's older producer-stage status is intentionally
unchanged. No endpoint infeasibility, global optimality, external priority, or
new general method is asserted.

## Reproduce from a clean checkout

Python **3.10+**; the standard path uses **no third-party package, network access,
model call, optimizer, or original workspace**. Python 3.13.5 is the version
actually tested when this release was assembled; other versions are not claimed
to have been tested here. Run from this directory:

```bash
python -X utf8 -B verify.py --output .replay-runs/full-001
```

The default command recomputes **all 181 inherited directions**, then **all 17
M17 trial directions**. The latter contain 16 accepted directions and one retained
counterexample: **198 coverage checks, 197 directions in the certified M19 net**.
It then checks the exact gap/endpoint calculations and the acceptance binding.
The expected final status is `PASS_FULL_REPLAY`.

The output directory must not already exist. Choose `full-002` on a second run.
Do not run with `python -O`, `python -OO`, or `PYTHONOPTIMIZE`; the supplied programs
use assertions, and the release adapter rejects optimized execution.

For a quick integrity and saved-evidence check **without recomputing coverage**:

```bash
python -X utf8 -B verify.py --quick --output .replay-runs/quick-001
```

Its status is deliberately `PASS_QUICK_CHECK_ONLY`, never a full-replay success.

An optional second implementation is available through
[scripts/source_crosscheck.py](scripts/source_crosscheck.py). It loads the
retained upstream NumPy sweep unchanged and rechecks all 198 directions;
see [reproduction instructions](docs/REPRODUCIBILITY.md). It is not required
by the default standard-library command.

## What changed mathematically

The 1,184 atoms, their weights, and probe side $B=9977/10000$ are unchanged.
M19 combines the original 181-direction net with 16 completely checked midpoints,
forming a 197-node nonuniform net. Its maximum adjacent half-angle tangent is

$$D=\frac{621321000000}{270300253166143}.$$

The smaller angular gap strengthens the inherited dilation-limit bound.
The earlier full 361-node refinement, **M17, failed** and remains recorded as
failed. M19 is a separately documented reuse of its passed directions, not a
rewrite of that failed experiment. See the [failure record](docs/M17_FAILURE.md).

## Evidence and verification status

The supplied M19 archive and its nested M12 dependency are retained byte-for-byte
under [evidence/M19](evidence/M19/). Both original ZIP files are also retained in
[archives](archives/); separately supplied duplicates are mapped in
[provenance/INPUTS.json](provenance/INPUTS.json), not silently replaced.

[verification/PACKAGING_REPORT.md](verification/PACKAGING_REPORT.md) records the
checks actually executed during assembly, with fresh outputs kept separate from
the project's historic acceptance. Running supplied exact programs again is not
a proof-assistant formalization or a newly authored independent geometric verifier.
It does not establish peer review or priority.

## Credit and reuse

Research project: **Guzhou0806 / N17 project**, with AI assistance.
The weighted certificate, source coverage algorithm, and dilation argument derive
from **Joshua Levy, the squares project**. The supplied work pins upstream commit
`035d84c655b4047bc9986c9a3db5106780d92f77`.

See [NOTICE.md](NOTICE.md) for the original MIT/CC BY 4.0 notices, transformations,
and the distinction between upstream and incremental contributions. No endorsement
or coauthorship by Joshua Levy is implied. Cite a fixed commit or release of this
snapshot; [CITATION.cff](CITATION.cff) provides metadata without inventing a DOI or
a public repository URL.
