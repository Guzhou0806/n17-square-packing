# R052 延续：十七单位正方形的严格下界 / R052 continuation: a strict lower bound for seventeen unit squares

本证书证明任意旋转、内部两两不交且允许边界接触的十七个单位正方形需要以下容器边长。 / This certificate proves the following container-side lower bound for seventeen arbitrarily rotated unit squares with pairwise disjoint interiors and permitted boundary contact.

$$s(17)>\frac{462003}{100000}=4.62003.$$

由 Guzhou0806 / N17 project 在 AI 辅助下完成；从已发布4.62002证书出发，对站点作精确D4对称变形并细分两处角区间，延续Kleddamag的公开混合证书架构。 / Produced by Guzhou0806 / N17 project with AI assistance, using an exact D4-symmetric site deformation and two angular refinements of the published 4.62002 certificate, continuing Kleddamag's public mixed-certificate architecture.

15727 个角区间、62908 条严格包含不等式及全部合法中心空间构成完整证明范围；资源共 2922 列、18585 个物理点和 4504 个阈值触发组。 / The proof covers 15727 angular intervals, 62908 strict containment inequalities and the complete legal centre space, using 2922 resource columns, 18585 physical points and 4504 threshold groups.

$$17\times999426274093-16990246659579=2>0.$$

所有收费均以 10^-12 为单位精确计数，上式的两个整数单位是严格盈余。 / All charges are counted exactly in units of 10^-12; the two integer units above form a strict surplus.

[证明 / Proof](PROOF.md) · [复验 / Reproduction](REPRODUCIBILITY.md) · [来源 / Sources](SOURCE_NOTICES.md) · [许可 / Licensing](LICENSE_SCOPE.md)

维护者获知 Kleddamag 已取得内部严格下界 4.62001；该结果属于 Kleddamag，其未公开证明未包含或独立验证于本发布。R052 数值超过这一报告值，但不声明外部优先权、最优性或真人同行评审。 / The maintainer was informed that Kleddamag obtained an internal strict bound of 4.62001; that result belongs to Kleddamag, whose unpublished proof is neither included nor independently verified here. R052 exceeds that reported value numerically but makes no claim of external priority, optimality or human peer review.

记录核查与重新计算分开：默认命令核对冻结账本；完整 Python 与 Node/BigInt 模式重新求解全部中心最小值，并与账本逐行比较。 / Recorded checks and fresh computation are separate: the default command checks frozen ledgers; the full Python and Node/BigInt modes recompute all centre minima and compare every row with the ledger.

```bash
python -X utf8 -B -S certificates/R052-4.62003/verify.py --output .replay-runs/r052-continuation-records
python -X utf8 -B -S certificates/R052-4.62003/verify.py --containment --output .replay-runs/r052-continuation-containment
```

命令从仓库根目录运行；输出目录须尚不存在。完整扫描命令和依赖见复验说明。 / Run from the repository root with a nonexistent output directory; see the reproduction instructions for full scans and dependencies.

本包是R052研究线的端点延续，原4.62002包保持不变；公开科学验收摘要见results/ACCEPTANCE.json。 / This package continues the R052 endpoint; the original 4.62002 package remains unchanged, and results/ACCEPTANCE.json records the public scientific acceptance summary.

## C++加速复验 / Accelerated C++ replay

公开包另提供自动构建的任意精度C++全量入口，保留Python参考实现及独立Node/BigInt复验；构建条件与命令见[原生复验说明 / Native reproduction](NATIVE_REPRODUCTION.md)。 / The package also provides an automatically built arbitrary-precision C++ full entry, retaining the Python reference and independent Node/BigInt replay; see the linked build requirements and commands.

```bash
python -X utf8 -B -S certificates/R052-4.62003/verify_native.py --jobs 4 --output .replay-runs/r052-continuation-native
```
