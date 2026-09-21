# Seventeen unit squares / 十七个单位正方形

## R038: current strict lower bound / R038：当前严格下界

Let $s(17)$ be the infimum side length of a square containing seventeen arbitrarily rotated unit squares with pairwise disjoint interiors, with boundary contact allowed. / 记 $s(17)$ 为容纳十七个可任意旋转且内部两两不交的单位正方形时容器正方形边长的下确界，并允许边界接触。

$$\boxed{s(17)>\frac{461300000000}{99974999999}=\frac{65900000000}{14282142857}}$$

```text
4.614153538430749222689979987... < s(17)
```

This is a computer-assisted exact lower bound, not a claim of global optimality, external peer review, formal verification, or established public priority. / 这是计算机辅助的精确下界，不主张全局最优、外部同行审查、形式化验证或已确认的公开首发。

[Proof / 证明](certificates/R038/PROOF.md) · [Replay / 复验](certificates/R038/README.md) · [Results / 结果登记](RESULTS.md) · [Attribution / 来源](certificates/R038/ATTRIBUTION.md)

## Reproduce R038 / 复验 R038

A package-local records check requires Python 3.10 or later and no network access. / 包内账本检查需要 Python 3.10 或更高版本，且不需要网络访问。

```bash
python -X utf8 -B -S certificates/R038/verify.py --output .replay-runs/r038-records-001
```

A complete geometric replay additionally requires Node.js and the SHA-pinned upstream Mira certificate. / 完整几何复演还需要 Node.js 与以 SHA 锁定的上游 Mira 证书。

```bash
python -X utf8 -B -S certificates/R038/verify.py \
  --certificate path/to/certificate.json \
  --output .replay-runs/r038-full-001
```

Windows users can fetch exactly the pinned upstream file and run the full replay with the bundled helper. / Windows 用户可用随附脚本仅获取锁定的上游文件并运行完整复演。

```powershell
powershell -ExecutionPolicy Bypass -File certificates/R038/fetch_and_replay.ps1 -OutputDir .replay-runs/r038-full-001
```

The complete success marker is `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`; the records-only marker is intentionally not a coverage proof. / 完整成功标记为 `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`；仅账本标记被有意设置为不能代表覆盖证明。

## What R038 proves / R038 证明了什么

R038 keeps the pinned outer side $L=4613/1000$ and reduces the parent side to $A'=99974999999/100000000000$. / R038 保持锁定外框边长 $L=4613/1000$，并将父边长缩小到 $A'=99974999999/100000000000$。

All 4,391 selected cores remain strictly inside their parents, and the exact expanded-domain event-cell replay for the pinned base measure has minimum `1000000030`, mass `16999991644`, surplus `8866`, and zero escape rows. / 全部 4,391 个选定内核仍严格位于父方块内部，且锁定基础测度在扩大后的合法中心域上进行精确事件胞元复演后，最低为 `1000000030`、总质量为 `16999991644`、余量为 `8866`，逃逸行数为零。

An additional D4 orbit `[64477,68039,1]` raises the recorded surplus to `8892`, but the base measure already proves the same endpoint, so R038 does not attribute the numerical endpoint gain to that extra orbit. / 额外 D4 轨道 `[64477,68039,1]` 将记录余量提高到 `8892`，但基础测度已经证明同一端点，因此 R038 不把该数值端点提升归因于这个额外轨道。

The exact source bytes are pinned to Mira commit `ac464dd06ded72e2f6eb2c2f3d510b01391c056d` and SHA-256 `5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3`; those third-party bytes are not redistributed here. / 精确来源字节锁定到 Mira 提交 `ac464dd06ded72e2f6eb2c2f3d510b01391c056d` 与 SHA-256 `5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3`；本仓库不重新分发这些第三方字节。

## Earlier public milestones / 早期公开里程碑

R012 remains unchanged and proves $s(17)\ge461300/99999$ with a self-contained Python-only parent-angle certificate. / R012 保持不变，并以自包含的纯 Python 父角证书证明 $s(17)\ge461300/99999$。

```bash
python -X utf8 -B -S certificates/R012/test_verify.py
python -X utf8 -B -S certificates/R012/verify.py --workers 4 --output .replay-runs/r012-001
```

M19 and its frozen evidence also remain unchanged, with the original `PASS_FULL_REPLAY` path retained at the repository root. / M19 及其冻结证据同样保持不变，仓库根目录继续保留原 `PASS_FULL_REPLAY` 复验路径。

## Credit and verification scope / 署名与可信边界

The R038 result is published by the Guzhou0806 / N17 project with AI assistance and uses mathematical data from Mira's `17squares`, whose lineage includes Joshua Levy's weighted-covering work. / R038 结果由 Guzhou0806 / N17 project 在 AI 辅助下发布，并使用 Mira `17squares` 的数学数据；其研究路线包含 Joshua Levy 的加权覆盖工作。

Source attribution does not imply upstream endorsement or coauthorship, and exact replay does not replace independent mathematical review. / 来源署名不代表上游作者背书或共同署名，精确复演也不能替代独立数学审查。
