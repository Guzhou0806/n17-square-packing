# Results register / 结果登记

This page records evidence published in this repository and is not a live world-record catalogue. / 本页登记本仓库已发布的证据，不是实时世界纪录目录。

Decimal text describes the stated constants and does not provide a two-sided enclosure of the unknown optimum $s(17)$. / 小数文本描述的是所列常数，并不构成对未知最优值 $s(17)$ 的双侧夹逼。

| Milestone / 里程碑 | Bound or outcome / 下界或结果 | Evidence / 证据 |
|---|---|---|
| **R042** | **$s(17)>115325/24963=4.61983735929175179265\ldots$** | [Mixed-certificate proof and two complete exact replay paths / 混合证书证明与两条完整精确复演路径](certificates/R042/README.md) |
| Kled v1.0.0 baseline / Kled v1.0.0 基线 | $461300/99853=4.61979109290657266181\ldots$ | [Pinned upstream source / 锁定上游来源](certificates/R042/ATTRIBUTION.md); not claimed as this project's result / 不作为本项目成果 |
| **R038** | $s(17)>65900000000/14282142857=4.61415353843074922268\ldots$ | [Strict parent-side proof and exact expanded-domain replay / 严格父边长证明与精确扩域复演](certificates/R038/README.md) |
| **R012** | $s(17)\ge461300/99999=4.61304613046130461304\ldots$ | [Complete parent-angle proof and exact Python replay / 完整父角证明与精确 Python 复验](certificates/R012/README.md) |
| **M19** | $4.59004266897263595052\ldots$ | [Proof / 证明](docs/M19_PROOF_EN.md), [original certificate / 原证书](evidence/M19/research/m19_work/CERTIFICATE.json) |
| M14 | $\sqrt{17065251368053280247690000/809993351783841654158521}$ | [Historical exact endpoint / 历史精确端点](evidence/M19/research/m14_work/CERTIFICATE.json) |
| M12 | $459000459/100000000$ | [Historical proof and replay / 历史证明与复验](evidence/M19/research/proofs/M12_global_lower_bound/README.md) |
| T-019 | $459/100=4.59$ | Joshua Levy's original weighted certificate / Joshua Levy 原始加权证书 |
| M17 | Fixed uniform refinement fails / 固定全加密失败 | [Exact counterexample and valid reuse / 精确反例及有效复用](docs/M17_FAILURE.md) |

## R042 scope / R042 范围

The R042 theorem uses the frozen mixed point-plus-two-of-three-threshold certificate at parent side `24963/25000` and its complete 7,853-row catalogue. / R042 定理使用父边长 `24963/25000` 下的冻结“点收费 + 三取二阈值收费”混合证书及其完整 7,853 行目录。

The formal theorem gate needs minimum `999954551` units per row against budget `16999227356` units, giving the exact positive margin `11`. / 正式定理门槛要求每行至少 `999954551` 单位收费，对应预算 `16999227356` 单位，因此得到精确正余量 `11`。

Both completed full replays record the stronger observed minimum `1000002306` and identical full histograms, while the independent containment audit proves 31,412 strict rational inequalities. / 两次已完成的全量复演记录了更强的观测最低值 `1000002306` 与相同的完整直方图，同时独立包含审计证明 31,412 个严格有理不等式。

Source-session execution, local reproduction, GitHub Actions reproduction, and independent external mathematical review remain distinct levels of evidence. / 来源会话执行、本地复现、GitHub Actions 复现与外部独立数学审查仍是不同层级的证据。
