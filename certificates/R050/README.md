# R050：十七单位正方形的严格下界 / R050: a strict lower bound for seventeen unit squares

本发布证明以下下界，其中正方形可任意旋转、内部两两不交，并允许边界接触。 / This release proves the following bound for arbitrarily rotated squares with pairwise disjoint interiors and permitted boundary contact.

$$s(17)>\frac{4613000}{998509}=4.6198882533857982251537041729\ldots.$$

**R050 已不是目前已知的最优下界：据维护者获知的信息，Kleddamag 已取得尚未公开的 4.62001 下界。该成果属于 Kleddamag，不属于本项目；其证明不包含在本发布中，本发布也未对其进行独立验证。** / **R050 is no longer the best currently known lower bound: according to information received by the maintainer, Kleddamag has obtained an unpublished lower bound of 4.62001. That result belongs to Kleddamag, not this project; its proof is not included or independently verified in this release.**

本发布由 Guzhou0806 / N17 project 在 AI 辅助下整理，延续 Kleddamag 的公开混合证书架构及 R043。 / This release is prepared by Guzhou0806 / N17 project with AI assistance, continuing Kleddamag's public mixed-certificate architecture and R043.

[证明 / Proof](PROOF.md) · [复验 / Reproduction](REPRODUCIBILITY.md) · [来源 / Sources](SOURCE_NOTICES.md) · [许可 / Licensing](LICENSE_SCOPE.md)

## 数学变化 / Mathematical change

保持 R043 的全部点资源、三取二阈值资源及权重不变，将父边长改为 998509/1000000，并将每个原角区间均分为二，重新构造严格内核。 / All R043 point resources, two-of-three threshold resources and weights are unchanged; the parent side becomes 998509/1000000, each original angular interval is bisected, and strict cores are reconstructed.

15706 个角区间覆盖全部所需方向，62824 个有理包含不等式严格成立。每个父正方形的内核收费至少 1000271689，而全局预算为 17003093868 个整数单位。 / The 15706 angular intervals cover all required directions, and all 62824 rational containment inequalities hold strictly. Every parent square has a core charging at least 1000271689, while the global budget is 17003093868 integer units.

$$17\times1000271689-17003093868=1524845>0.$$

因此十七个父正方形的装填不可能存在；缩放与紧致性给出上述严格下界。 / Hence a packing of seventeen parent squares is impossible; scaling and compactness yield the stated strict lower bound.

## 验证范围 / Verification scope

已完成全部 15706 行的独立 Python 扫描，并将逐行账本与另一套 BigInt 实现的全部 118 个分块逐一对照完整直方图及最低值。BigInt 原件由先保存的 11400 行前缀与后补的 4306 行构成；不声称原始 BigInt 全目录来自一次新执行。 / A complete independent Python scan of all 15706 rows was completed, and its row ledger was compared against every complete histogram and minimum of the other BigInt implementation's 118 blocks. The original BigInt evidence consists of a previously saved 11400-row prefix and a subsequently completed 4306-row suffix; the original full BigInt coverage is not presented as one fresh execution.

记录核查、重新计算包含、完整 Python 复演及完整 BigInt 复演是不同验证层级，具体命令和真实发布复验记录见复验说明。 / Recorded-evidence checks, recomputed containment, full Python replay and full BigInt replay are distinct verification levels; see the reproduction instructions for commands and actual publication-validation records.

该计算机辅助证明没有主张全局最优、外部同行评审或证明助理形式化。 / This computer-assisted proof makes no claim of global optimality, external peer review or proof-assistant formalization.
