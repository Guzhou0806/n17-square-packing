# Seventeen unit squares / 十七个单位正方形

## R043: current strict lower bound / R043：当前严格下界

Let $s(17)$ be the infimum side length of a square containing seventeen arbitrarily rotated unit squares with pairwise disjoint interiors, with boundary contact allowed. / 记 $s(17)$ 为容纳十七个可任意旋转且内部两两不交的单位正方形时容器正方形边长的下确界，并允许边界接触。

$$\boxed{s(17)>\frac{461300}{99851}}$$

```text
4.61988362660363942273988242481297... < s(17)
```

This is a computer-assisted exact lower bound, not a claim of maximality, global optimality, established public priority, external peer review, or proof-assistant formalization. / 这是计算机辅助的精确下界，不主张端点已达极限、全局最优、已确认公开首发、外部同行审查或证明助理形式化。

[Proof / 证明](certificates/R043/PROOF.md) · [Replay / 复验](certificates/R043/README.md) · [Results / 结果登记](RESULTS.md) · [Attribution / 来源](certificates/R043/ATTRIBUTION.md)

## Reproduce R043 / 复验 R043

A package-local recorded check requires Python 3.10 or later and no third-party modules or network access. / 包内记录检查需要 Python 3.10 或更高版本，不需要第三方模块或网络访问。

```bash
python -X utf8 -B -S certificates/R043/verify.py --output .replay-runs/r043-recorded-001
```

An independent standard-library containment replay recomputes all 31,412 exact rational inequalities. / 独立的纯标准库包含复演会重新计算全部 31,412 个精确有理不等式。

```bash
python -X utf8 -B -S certificates/R043/verify.py --containment --output .replay-runs/r043-containment-001
```

The complete Python exact replay requires NumPy and Numba, while the source-distinct BigInt replay requires Node.js and reconstructs its checker from SHA-pinned public R038 source bytes. / 完整 Python 精确复演需要 NumPy 与 Numba，而不同源码的 BigInt 复演需要 Node.js，并从 SHA 锁定的公开 R038 源字节重建检查器。

```bash
python -X utf8 -B certificates/R043/verify.py --python-full --jobs 4 --output .replay-runs/r043-python-001
python -X utf8 -B -S certificates/R043/verify.py --bigint-full --jobs 5 --output .replay-runs/r043-bigint-001
```

The reconstructed BigInt checker bytes are not committed to this repository. / 重建后的 BigInt 检查器字节不提交到本仓库。

## What R043 proves / R043 证明了什么

R043 fixes $L=4613/1000$ and $A=99851/100000$, hence $L/A=461300/99851$. / R043 固定 $L=4613/1000$ 与 $A=99851/100000$，因此 $L/A=461300/99851$。

The accepted certificate changes no point coordinates and no threshold orbit relative to R042; it activates four previously zero-weight point orbits on the existing support. / 相对 R042，已接受证书不改变 point 坐标或 threshold orbit，只在既有支撑上激活四个此前权重为零的 point orbit。

The global budget is `17003093868` units and both complete exact replay engines report the common minimum `1000181993` over all 7,853 catalogue rows. / 全局预算为 `17003093868` 单位，两套完整精确复演引擎都在全部 7,853 个目录行上得到共同最低值 `1000181993`。

The exact counting surplus is `17 × 1000181993 − 17003093868 = 13 > 0`. / 精确计数余量为 `17 × 1000181993 − 17003093868 = 13 > 0`。

The complete Python and BigInt row-minimum histograms are identical, and the BigInt replay has zero escape rows. / 完整 Python 与 BigInt 的逐行最低值直方图完全一致，并且 BigInt 复演的 escape rows 为零。

An independent rational audit proves strict containment for all 31,412 catalogue inequalities. / 独立有理审计证明全部 31,412 个目录包含不等式均严格成立。

## Earlier public milestones / 早期公开里程碑

R042 remains unchanged and proves $s(17)>115325/24963$. / R042 保持不变，并证明 $s(17)>115325/24963$。

R038 remains unchanged and proves $s(17)>65900000000/14282142857$. / R038 保持不变，并证明 $s(17)>65900000000/14282142857$。

R012 remains unchanged and proves $s(17)\ge461300/99999$. / R012 保持不变，并证明 $s(17)\ge461300/99999$。

M19 and its frozen evidence also remain unchanged. / M19 及其冻结证据同样保持不变。

## Credit and verification scope / 署名与可信边界

R043 is published by the Guzhou0806 / N17 project with AI assistance and continues the pinned Kleddamag v1.0.0 mixed-certificate architecture. / R043 由 Guzhou0806 / N17 project 在 AI 辅助下发布，并延续锁定的 Kleddamag v1.0.0 混合证书架构。

Source attribution does not imply upstream endorsement or coauthorship, and exact replay does not replace independent mathematical review. / 来源署名不代表上游作者背书或共同署名，精确复演也不能替代独立数学审查。
