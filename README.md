# N17 Square Packing — Research Notes and Certificates

Research on lower bounds for packing 17 freely rotatable unit squares into a square.
The aim is documented, reproducible progress, not a claim that the optimum has been solved.

**This is an initial, partial evidence export.** It preserves the M19 files supplied by the
project and records their precise claims. The project proof reports completed internal
independent checks and acceptance. However, this export does not yet include the atom
certificate, all direction-coverage records, or the complete replay programs needed for
third-party end-to-end verification. See [evidence status](results/M19/EVIDENCE_STATUS.json).

[中文使用说明](START_HERE.zh-CN.md) · [Result register](RESULTS.md) ·
[Reproduction scope](docs/VERIFICATION.md) · [Provenance](docs/PROVENANCE.md)

## M19: a nonuniform-direction-net lower-bound result

The supplied proof states

$$
s(17)\ge S_{19}=\frac{45900\sqrt{73062612901466039895961496449}}
{2702984545455608711},
$$

with the exact bracket

```text
4.59004266897263595052 <= S19 < 4.59004266897263595053.
```

The original [proof](results/M19/original/PROOF.md) and
[certificate](results/M19/original/CERTIFICATE.json) are preserved byte-for-byte.
The statement is a non-strict lower bound. It does not assert that the endpoint itself
is infeasible, or that the result is a world record.

The construction combines 181 old directions with 16 passing directions from M17.
The failed full-uniform refinement is [retained separately](results/M17/FAILURE.md),
not rewritten as a success. See the proof for the hypotheses supporting the continuum
coverage and counting argument.

The larger value `4.592995` is recorded only as a maintainer-reported candidate:
[its evidence has not been supplied in this export](results/candidate-4.592995/README.md).
It is not the accepted headline bound of this package.

## What runs now

Python 3.10+ and the standard library are sufficient for these limited checks:

```bash
python scripts/check_snapshot.py
python -m unittest discover -s tests -v
```

These commands check the submitted file hashes, direction-gap arithmetic, counting
arithmetic and exact square comparisons. **They do not certify minimum covered mass over
all legal centers, replay the full packing proof, or establish priority.** A green
workflow means only that these stated snapshot checks passed.

The archived producer requires its original local-project dependencies and is not a
standalone verifier. Full-replay instructions will be added only after they work in a
clean checkout. No fake `verify_all` command is supplied.

## Attribution and publication

The supplied proof credits Joshua Levy's `squares` project for the atom measure and
source coverage algorithms, pinned to commit
`035d84c655b4047bc9986c9a3db5106780d92f77`, and credits T-022/M14 for the dilation-limit
argument. M19's stated increment is the nonuniform 197-direction evidence and its
N17 consequence; see [provenance](docs/PROVENANCE.md).

[Citation metadata](CITATION.cff.example) is a template pending author approval.
[License boundaries](docs/LICENSE_NOTES.md) require review before open-source distribution.
No DOI, publication date, journal acceptance or priority finding is invented.

This package has not created or published a GitHub repository. Review it locally first.
