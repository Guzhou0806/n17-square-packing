# Seventeen unit squares / 十七个单位正方形

## R012: a parent-angle lower-bound certificate / 父角目录下界证书

Let $s(17)$ be the infimum side of a square containing seventeen arbitrarily rotated unit squares with pairwise disjoint interiors. Boundary contact is allowed.

记 $s(17)$ 为容纳十七个可任意旋转、内部两两不交的单位正方形时，正方形容器边长的下确界，允许边界接触。

$$\boxed{s(17)\ge S_{12}:=\frac{461300}{99999}}$$

```text
4.61304613046130461304 <= S12 < 4.61304613046130461305
```

**The bracket encloses the lower-bound constant, not the unknown optimum s(17).** This is a computer-assisted result with reproducible exact arithmetic, not a claim of peer review, global optimality or established public priority.

**夹逼对象是下界常数，不是未知的 s(17)。**本仓库提供可复验的精确计算证据，不以程序通过替代外部审稿、全局最优或首发确认。

[Proof / 证明](certificates/R012/PROOF.md) · [Replay / 复验](certificates/R012/README.md) · [Results / 结果登记](RESULTS.md) · [Attribution / 来源](certificates/R012/ATTRIBUTION.md)

## Reproduce R012 / 复验 R012

Python **3.10+**, standard library only. No account, model, optimizer, compiler or network is needed after checkout. Run from the repository root:

```bash
python -X utf8 -B -S certificates/R012/test_verify.py
python -X utf8 -B -S certificates/R012/verify.py --workers 4 --output .replay-runs/r012-001
```

The output directory must be new. Reduce `--workers` for smaller machines. The public replay recomputes every one of **2925 continuous parent-angle intervals**, each over its **entire legal parent-center envelope**. Allow several minutes; these are not 2925 sampled placements.

输出目录必须尚不存在。完整入口重算 **2925 个连续父角区间**及各自的**全部合法父中心域**，不是角度或位置抽样。计算只使用 Python 标准库，应预留数分钟或更长。

The complete success marker is / 完整成功标记为：

```text
PASS_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND
```

`--records` produces `PASS_RECORDS_ONLY` and does **not** recompute coverage. Do not use `-O`, `-OO` or `PYTHONOPTIMIZE`.

## What changed / 贡献范围

The certificate keeps one fixed nonnegative measure: **1616 atoms in 206 D4 orbits**, at base side $L=4.613$. For every legal parent square of side $A=0.99999$, a complete catalogue selects one concentric closed core strictly inside it. Different parent-angle ranges can use different core directions and sizes, but all consume the same total mass. The exact contradiction gives $L/A=461300/99999$.

证书固定同一份非负测度：**1616 个原子、206 个 D4 轨道**。改进在于为每个真实父方块选择一个严格内部核，而非要求所有辅助小核都成功。不同角区间可以使用不同方向和大小的核，但没有另开或重复使用质量预算。

Relative to the pinned Mira endpoint $4.61302863588611076617\ldots$, the constant increases by approximately $0.00001749457519384687$; the proof checks a strictly positive rational squared difference. This comparison is with a specified source, not an exhaustive world-record survey.

相对锁定 Mira 端点的改进由精确正平方差验证；并不由此宣布穷尽公开纪录。加权测度、事件几何、内部核计数和父中心限制继承已有工作，具体选择目录及 N17 推论是本项目的增量。

## Earlier milestone / 历史里程碑

[M19](docs/M19_PROOF_EN.md) and its frozen evidence remain unchanged. Its original standard-library command still works:

```bash
python -X utf8 -B verify.py --output .replay-runs/m19-001
```

M19 retains its own `PASS_FULL_REPLAY` marker. It is distinct from R012 and does not verify R012. / M19 原证据与命令保留；其通过标记不代表 R012 已复验。

## Credit and verification scope / 署名与可信边界

**Guzhou0806 / N17 project, with AI assistance.** The mathematical lineage includes **Mira's 17squares** and **Joshua Levy, the squares project**. See [source versions and transformations](certificates/R012/ATTRIBUTION.md) and [repository notices](NOTICE.md).

The public Python implementation rechecks the unchanged R012 data; it does not copy the original C++ distribution. Exact-program replay and witness cross-checks are not an independently designed second full geometric proof. No upstream endorsement, external peer review, formalization or priority is implied.

公开 Python 入口重新检查同一数学对象，不分发原 C++ 包。程序复演与见证交叉检查不等于第二份独立全几何证明；来源署名不暗示作者背书、共同署名或外部验收。
