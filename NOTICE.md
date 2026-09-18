# Attribution, provenance and licensing scope

The supplied mathematical material attributes the atom certificate, source coverage
algorithm and general dilation-limit argument to **Joshua Levy, the squares project**:
https://github.com/jlevy/squares

The source version recorded by the project is
`035d84c655b4047bc9986c9a3db5106780d92f77`.
The original T-019 certificate has SHA-256
`461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652`.

The N17 project, maintained by Guzhou0806 with AI assistance, records the incremental
197-node coverage evidence, the retained M17 counterexample, and the resulting M19
numerical corollary. No upstream endorsement, new general dilation method,
coauthorship, or external priority is implied.

## Retained original notices

- [Original upstream license text](evidence/M19/research/proofs/M12_global_lower_bound/UPSTREAM_LICENSE.txt)
- [M12 attribution and exact transformations](evidence/M19/research/proofs/M12_global_lower_bound/ATTRIBUTION.md)
- [M19 source/contribution statement](evidence/M19/PROOF.md)

These source files describe MIT terms for code and CC BY 4.0 for upstream
non-code documentation/research/data. The upstream third-party `packing/resources/`
archive is not included. The original notices are preserved, not replaced with
a blanket license for every file in the release.

## What packaging changed

No byte of the 129 files extracted from the supplied M19 archive was changed.
The separate M12 archive was found identical to its already nested copy. Individual
supplementary uploads were deduplicated only after byte equality checks.

New presentation/integration files are at the repository root, `docs/`,
`communication/`, `scripts/`, `tests/`, `provenance/` and `.github/`.
They include English presentation, Chinese usage instructions, reproducibility
adapters, and new execution records under `verification/`. They do not rewrite the
original mathematical proofs, producer statuses, code, data or acceptance records.
No additional blanket relicensing is performed here; the maintainer should state
an explicit grant for new packaging material if broader reuse permission is desired.

AI assistance was used in the research workflow and in preparing this release.
Model output is not a proof authority. See [reproduction scope](docs/REPRODUCIBILITY.md)
and the actual reports for what was run.
