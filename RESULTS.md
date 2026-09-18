# Results register — scope of this release

This is a versioned record of the supplied stages, not a live survey or world-record
claim. A decimal below is a display of a lower-bound constant, not an equality for
$s(17)$. Exact expressions or rational squares define the claims.

| Stage | Lower-bound constant / outcome | Evidence in this snapshot |
|---|---|---|
| Upstream T-019 | $459/100=4.59$ | Original 1,184-atom certificate; attributed to Joshua Levy |
| M12 | $459000459/100000000=4.59000459$ | Full historical package and standard-library replay |
| M14 | $\sqrt{17065251368053280247690000/809993351783841654158521}$, approximately $4.59003098986653245118\ldots$ | Exact endpoint certificate and formal report inherited by M19 |
| M17 | Fixed full refinement rejected; not a lower-bound improvement | 17 new directions evaluated; exact failure at refined index 29 |
| **M19 / CL-M19-001** | **$S_{19}=4.59004266897263595052\ldots$** | Proof, certificate, both implementations, complete direction data, acceptance and fresh replay |

M19 increases the M14 constant by approximately `0.00001167910610349934`.
Its certificate stores the strictly positive **exact squared difference**.
The decimal difference is a display, not the defining comparison.

M20 and the stronger `4.592995...` statement are **not released or verified by this
snapshot**. This does not make a claim about their current status in the private
project. Add a separate evidence-backed entry when that stage is prepared.

## Stable entry points

- [M19 theorem](docs/M19_PROOF_EN.md)
- [Original Chinese M19 proof](evidence/M19/PROOF.md)
- [M19 certificate](evidence/M19/research/m19_work/CERTIFICATE.json)
- [M19 final acceptance](evidence/M19/FINAL_ACCEPTANCE.json)
- [M12 theorem and replay](evidence/M19/research/proofs/M12_global_lower_bound/README.md)
- [M14 certificate](evidence/M19/research/m14_work/CERTIFICATE.json)
- [M17 negative result](docs/M17_FAILURE.md)

Do not edit a frozen certificate to update its status. Append a hash-bound audit or
new milestone, and leave the original result available.
