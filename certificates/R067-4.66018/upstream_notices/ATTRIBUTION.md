# Attribution and source identity

The release extends established weighted-covering, strict-core transport and
exact geometric-sweep methods. It does not claim independent invention of
those methods or an exhaustive literature-priority result.

## Mira / 17squares

The numerical support and parent-angle catalogue lineage comes from
[Mira-acc/17squares at ac464dd](https://github.com/Mira-acc/17squares/tree/ac464dd06ded72e2f6eb2c2f3d510b01391c056d),
specifically `certificates/lower_bound_4p614153/certificate.json` with SHA-256
`5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3`.
The pinned source attribution is retained in `NOTICES/Mira-ATTRIBUTION.md`.
The original upstream certificate and source code are not bundled here.

Our certificate changes and enlarges the spatial support, introduces weighted
two-of-three site charges, changes weights, and refines the angle catalogue.
Its final geometry and weights are exact rational data and are checked afresh.

## Guzhou0806 / N17 project

The audited baseline is
[R038 at 32edfd3](https://github.com/Guzhou0806/n17-square-packing/tree/32edfd3da78bf80a309398f552b3b602b9c45d6c/certificates/R038),
published by **Guzhou0806 / N17 project, with AI assistance**. R038 reports
the strict lower bound `461300000000/99974999999`. Its parent-side reduction,
strict containment and expanded-centre-domain replay are part of this
continuation's direct lineage.

The secondary checker adapts R038's
[`src/exact_parent_side_scan.js`](https://github.com/Guzhou0806/n17-square-packing/blob/32edfd3da78bf80a309398f552b3b602b9c45d6c/certificates/R038/src/exact_parent_side_scan.js).
We added support for the finer coordinate denominator, point-orbit format,
weighted two-of-three rectangles, generalized input identity and budget checks.
The distributed adaptation contains this project's edits; unchanged upstream
source is fetched locally from the pinned public revision.

| Item | SHA-256 |
|---|---|
| Pinned R038 checker | `63e858e28c4dee40f5763a832e1cfdf1f1fce3a1e5c632d087525bf1ee20ed14` |
| Reconstructed checker used in completed verification | `b145b1ebbb2d3a0dccba62ee7b5ed64403bf0542ce5e8ee87113977df917faa4` |

R038's attribution and licence-scope notices, and the repository notice at
that commit, are preserved verbatim under `NOTICES/`.

## Joshua Levy / the squares project

Credit **Joshua Levy, the squares project
([github.com/jlevy/squares](https://github.com/jlevy/squares))** for the
weighted-covering, strict-core, event-cell and threshold-budget lineage
documented by the upstream projects. An explicitly cited antecedent is the
[parent-centre contract](https://github.com/jlevy/squares/blob/fb14f5174fdf675b296b442c98b7127fccc8a84d/packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md).
The upstream attribution also identifies Levy's
[threshold certificate](https://github.com/jlevy/squares/blob/main/packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md).

The upstream MIT notice and the archived code/documentation licence distinction
are retained in `NOTICES/Joshua-Levy-MIT.txt` and
`NOTICES/Joshua-Levy-LICENSE-source.txt`. Those grants do not license unrelated
third-party works or extend to Guzhou/Mira material merely by association.

## The established packing

The upper-bound construction is a rational reconstruction of the established
[Bidwell 17-square packing](https://kingbird.myphotos.cc/packing/square-17.svg).
We verified the supplied rational coordinates exactly. This is not a newly
discovered packing and does not improve that established construction.

## This continuation

The new milestone is the certificate for `s(17) > 461300/99853`, together with
the exact charge argument, the independently written Python polygon-edge
checker, the adapted secondary checker, independent premise controls and
completed verification records. Numerical optimization and AI exploration
found the input; they are not premises of the proof. The human/AI division of
work is explained in [AUTHORS.md](AUTHORS.md).

## The 4.640020 continuation (v1.1.0)

The current certificate proves `s(17)>232001/50000`. It continues the same attributed weighted-covering and strict-core lineage, with larger charge dictionaries, ordinary k-of-n thresholds, weighted thresholds and pairwise-intersecting winning-subset rules. Separate Codex tasks combined completed geometry and counterexamples before reoptimization and exact verification. We make no claim that these general mathematical ideas were newly invented here.

The newly bundled `bounds/4.640020/verify_global_variable.js` is this project's separately implemented general-rule BigInt checker, paired with the general-rule Python polygon sweep. It is distinct from the legacy R038 download/adaptation path retained for v1.0.0. The new certificate and both engines were fully replayed together before release. No code from the colleague's later R052/C++ repository was used. The earlier source pins and notices above remain part of the historical lineage.

## The 4.66001 continuation

The package under `bounds/4.66001/` continues the same attributed weighted-covering and strict-core method. It preserves the general-rule Python and separately implemented BigInt engines from the 4.640020 package byte-for-byte. It combines two completed charge candidates and regenerates strict cores for refined orientation intervals. No novelty claim is made for the general method, and no external Guzhou source or C++ code is included in or executed by this proof path.
