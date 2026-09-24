# Results register / 结果登记

This page records evidence published in this repository and is not a live world-record catalogue. / 本页登记本仓库已发布的证据，不是实时世界纪录目录。

Decimal text describes the stated constants and does not provide a two-sided enclosure of the unknown optimum $s(17)$. / 小数文本描述的是所列常数，并不构成对未知最优值 $s(17)$ 的双侧夹逼。

| Milestone / 里程碑 | Bound or outcome / 下界或结果 | Evidence / 证据 |
|---|---|---|
| **R050** | **$s(17)>4613000/998509=4.61988825338579822515\ldots$** | [角目录细分与严格内核证明 / Refined-angle strict-core proof](certificates/R050/README.md) |
| **R043** | **$s(17)>461300/99851=4.61988362660363942273\ldots$** | [Point-weight continuation with two complete exact replay paths / 点权推进与两条完整精确复演路径](certificates/R043/README.md) |
| **R042** | $s(17)>115325/24963=4.61983735929175179265\ldots$ | [Mixed-certificate proof and two complete exact replay paths / 混合证书证明与两条完整精确复演路径](certificates/R042/README.md) |
| Kled v1.0.0 baseline / Kled v1.0.0 基线 | $461300/99853=4.61979109290657266181\ldots$ | [Pinned upstream source / 锁定上游来源](certificates/R042/ATTRIBUTION.md); not claimed as this project's result / 不作为本项目成果 |
| **R038** | $s(17)>65900000000/14282142857=4.61415353843074922268\ldots$ | [Strict parent-side proof and exact expanded-domain replay / 严格父边长证明与精确扩域复演](certificates/R038/README.md) |
| **R012** | $s(17)\ge461300/99999=4.61304613046130461304\ldots$ | [Complete parent-angle proof and exact Python replay / 完整父角证明与精确 Python 复验](certificates/R012/README.md) |
| **M19** | $4.59004266897263595052\ldots$ | [Proof / 证明](docs/M19_PROOF_EN.md), [original certificate / 原证书](evidence/M19/research/m19_work/CERTIFICATE.json) |

**R050 已不是目前已知的最优下界：据维护者获知的信息，Kleddamag 已取得尚未公开的 4.62001 下界。该成果属于 Kleddamag，不属于本项目；其证明不包含在本发布中，本发布也未独立验证该证明。** / **R050 is no longer the best currently known lower bound: according to information received by the maintainer, Kleddamag has obtained an unpublished lower bound of 4.62001. That result belongs to Kleddamag, not this project; its proof is neither included nor independently verified in this release.**

## R050 范围 / R050 scope

全部 15706 行与 62824 个严格包含不等式通过验证，统一最低收费 1000271689、预算 17003093868、计数余量 1524845。 / All 15706 rows and 62824 strict-containment inequalities pass verification, with universal minimum 1000271689, budget 17003093868 and surplus 1524845.

## R043 scope / R043 范围

The R043 theorem uses the inherited mixed point-plus-two-of-three-threshold certificate language at parent side `99851/100000` and its complete 7,853-row catalogue. / R043 定理使用父边长 `99851/100000` 下继承的“点收费 + 三取二阈值收费”混合证书语言及其完整 7,853 行目录。

The accepted certificate has budget `17003093868` units and common full-replay minimum `1000181993`, giving the exact positive counting surplus `13`. / 已接受证书的预算为 `17003093868` 单位，两套全量复演共同最低值为 `1000181993`，因此得到精确正计数余量 `13`。

Both complete replay engines agree on the full row-minimum histogram, while the independent containment audit proves 31,412 strict rational inequalities. / 两套完整复演引擎对完整逐行最低值直方图一致，同时独立包含审计证明 31,412 个严格有理不等式。

Local reproduction, GitHub Actions reproduction, and independent external mathematical review remain distinct levels of evidence. / 本地复现、GitHub Actions 复现与外部独立数学审查仍是不同层级的证据。
