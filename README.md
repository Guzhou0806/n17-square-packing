# Seventeen unit squares / 十七个单位正方形

## R042: current strict lower bound / R042：当前严格下界

Let $s(17)$ be the infimum side length of a square containing seventeen arbitrarily rotated unit squares with pairwise disjoint interiors, with boundary contact allowed. / 记 $s(17)$ 为容纳十七个可任意旋转且内部两两不交的单位正方形时容器正方形边长的下确界，并允许边界接触。

$$\boxed{s(17)>\frac{115325}{24963}}$$

```text
4.61983735929175179265312662740856... < s(17)
```

This is a computer-assisted exact lower bound, not a claim of maximality, global optimality, established public priority, external peer review, or proof-assistant formalization. / 这是计算机辅助的精确下界，不主张端点已达极限、全局最优、已确认公开首发、外部同行审查或证明助理形式化。

[Proof / 证明](certificates/R042/PROOF.md) · [Replay / 复验](certificates/R042/README.md) · [Results / 结果登记](RESULTS.md) · [Attribution / 来源](certificates/R042/ATTRIBUTION.md)

## Reproduce R042 / 复验 R042

A package-local records check requires Python 3.10 or later and no third-party modules or network access. / 包内账本检查需要 Python 3.10 或更高版本，不需要第三方模块或网络访问。

```bash
python -X utf8 -B -S certificates/R042/verify.py --output .replay-runs/r042-records-001
```

An independent standard-library containment replay recomputes all 31,412 exact quadratic inequalities. / 独立的纯标准库包含复验会重新计算全部 31,412 个精确二次不等式。

```bash
python -X utf8 -B -S certificates/R042/verify.py --containment --output .replay-runs/r042-containment-001
```

The complete Python exact replay requires NumPy and Numba, while the source-distinct BigInt replay requires Node.js and reconstructs its checker from SHA-pinned R038 source bytes. / 完整 Python 精确复演需要 NumPy 与 Numba，而不同源码的 BigInt 复演需要 Node.js，并从 SHA 锁定的 R038 源字节重建检查器。

```bash
python -X utf8 -B certificates/R042/verify.py --python-full --jobs 4 --output .replay-runs/r042-python-001
python -X utf8 -B -S certificates/R042/verify.py --bigint-full --jobs 4 --output .replay-runs/r042-bigint-001
```

The records-only marker never implies a fresh full replay, and the reconstructed BigInt checker bytes are never committed. / 仅账本标记从不代表已经完成新的全量复演，且重建后的 BigInt 检查器字节从不提交到仓库。

## What R042 proves / R042 证明了什么

R042 fixes $L=4613/1000$ and $A=24963/25000$, hence $L/A=115325/24963$. / R042 固定 $L=4613/1000$ 与 $A=24963/25000$，因此 $L/A=115325/24963$。

The frozen mixed certificate has global budget `16999227356` units and requires only `999954551` units from every legal parent-angle row. / 冻结混合证书的全局预算为 `16999227356` 单位，并且只要求每个合法父角目录行提供 `999954551` 单位收费。

The theorem's exact counting gap is `17 × 999954551 − 16999227356 = 11 > 0`. / 定理的精确计数余量为 `17 × 999954551 − 16999227356 = 11 > 0`。

Both completed full exact replays report the stronger observed global minimum `1000002306` and identical complete minimum histograms, giving an observed surplus of `811846` units. / 两次已完成的精确全量复演都得到更强的观测全局最低值 `1000002306` 与完全相同的完整最低值直方图，对应观测余量 `811846` 单位。

An independent rational audit proves strict containment for all 31,412 catalogue inequalities. / 独立有理审计证明全部 31,412 个目录包含不等式均严格成立。

## Earlier public milestones / 早期公开里程碑

R038 remains unchanged and proves $s(17)>65900000000/14282142857=4.61415353843074922268\ldots$. / R038 保持不变，并证明 $s(17)>65900000000/14282142857=4.61415353843074922268\ldots$。

R012 remains unchanged and proves $s(17)\ge461300/99999$ with a self-contained Python-only parent-angle certificate. / R012 保持不变，并以自包含的纯 Python 父角证书证明 $s(17)\ge461300/99999$。

M19 and its frozen evidence also remain unchanged, with the original `PASS_FULL_REPLAY` path retained at the repository root. / M19 及其冻结证据同样保持不变，仓库根目录继续保留原 `PASS_FULL_REPLAY` 复验路径。

## Credit and verification scope / 署名与可信边界

R042 is published by the Guzhou0806 / N17 project with AI assistance and builds on the pinned Kleddamag v1.0.0 certificate architecture, whose own lineage includes earlier work documented in the attribution files. / R042 由 Guzhou0806 / N17 project 在 AI 辅助下发布，并建立在锁定的 Kleddamag v1.0.0 证书架构之上；其更早研究路线见来源文件。

Source attribution does not imply upstream endorsement or coauthorship, and exact replay does not replace independent mathematical review. / 来源署名不代表上游作者背书或共同署名，精确复演也不能替代独立数学审查。
