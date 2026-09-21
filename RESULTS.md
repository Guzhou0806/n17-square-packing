# Results register / 结果登记

This page records evidence published in this repository and is not a live world-record catalogue. / 本页登记本仓库已发布的证据，不是实时世界纪录目录。

Decimal text describes the stated constants and does not provide a two-sided enclosure of the unknown optimum $s(17)$. / 小数文本描述的是所列常数，并不构成对未知最优值 $s(17)$ 的双侧夹逼。

| Milestone / 里程碑 | Bound or outcome / 下界或结果 | Evidence / 证据 |
|---|---|---|
| **R038** | **$s(17)>461300000000/99974999999=4.61415353843074922268\ldots$** | [Strict parent-side proof and exact expanded-domain replay / 严格父边长证明与精确扩域复演](certificates/R038/README.md) |
| Mira analytic sharpening / Mira 解析加锐 | $46129999999859/9997499999900=4.61415353841664569680\ldots$ | [Pinned upstream source / 锁定上游来源](certificates/R038/ATTRIBUTION.md); not claimed as this project's result / 不作为本项目成果 |
| **R012** | $s(17)\ge461300/99999=4.61304613046130461304\ldots$ | [Complete parent-angle proof and exact Python replay / 完整父角证明与精确 Python 复验](certificates/R012/README.md) |
| **M19** | $4.59004266897263595052\ldots$ | [Proof / 证明](docs/M19_PROOF_EN.md), [original certificate / 原证书](evidence/M19/research/m19_work/CERTIFICATE.json) |
| M14 | $\sqrt{17065251368053280247690000/809993351783841654158521}$ | [Historical exact endpoint / 历史精确端点](evidence/M19/research/m14_work/CERTIFICATE.json) |
| M12 | $459000459/100000000$ | [Historical proof and replay / 历史证明与复验](evidence/M19/research/proofs/M12_global_lower_bound/README.md) |
| T-019 | $459/100=4.59$ | Joshua Levy's original weighted certificate / Joshua Levy 原始加权证书 |
| M17 | Fixed uniform refinement fails / 固定全加密失败 | [Exact counterexample and valid reuse / 精确反例及有效复用](docs/M17_FAILURE.md) |

## R038 scope / R038 范围

The R038 theorem uses the pinned 3,280-atom base measure and recomputes all 4,391 legal parent-centre envelopes after reducing the parent side by $10^{-11}$. / R038 定理使用锁定的 3,280 原子基础测度，并在父边长降低 $10^{-11}$ 后重新计算全部 4,391 个合法父中心包络。

The base scan has exact surplus `8866`; an augmented-orbit control has surplus `8892`, but the augmented orbit is not necessary for the R038 endpoint. / 基础扫描的精确余量为 `8866`；增广轨道对照的余量为 `8892`，但 R038 端点并不需要该增广轨道。

The complete public replay requires the SHA-pinned upstream certificate because its bytes are not redistributed in this repository. / 完整公开复演需要 SHA 锁定的上游证书，因为本仓库不重新分发其字节。

Source-session execution, local reproduction, and independent external mathematical review remain distinct levels of evidence. / 来源会话执行、本地复现与外部独立数学审查仍是不同层级的证据。
