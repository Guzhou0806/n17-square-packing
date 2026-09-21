# R038 strict lower-bound certificate / R038 严格下界证书

**The current public result is $s(17)>461300000000/99974999999=4.614153538430749222689979987\ldots$. / 当前公开结果为 $s(17)>461300000000/99974999999=4.614153538430749222689979987\ldots$。**

[Proof / 证明](PROOF.md) · [Reproduction / 复验](REPRODUCIBILITY.md) · [Attribution / 来源](ATTRIBUTION.md) · [Claims / 结果账本](CLAIMS.json)

This directory publishes the R038 endpoint push while keeping the upstream Mira certificate external and SHA-pinned. / 本目录发布 R038 端点推进，同时将上游 Mira 证书作为外部依赖并以 SHA 锁定。

The theorem itself uses the original pinned Mira measure at the smaller parent side $A'=99974999999/100000000000$; the additional orbit `[64477,68039,1]` is retained only as a separate augmented control. / 定理本身使用锁定的原 Mira 基础测度，并将父边长缩小到 $A'=99974999999/100000000000$；额外轨道 `[64477,68039,1]` 仅作为独立增广对照保留。

The base measure passes all 4,391 parent-angle rows with minimum `1000000030`, mass `16999991644`, exact surplus `8866`, and zero escape rows. / 基础测度在全部 4,391 个父角目录行上取得最低 `1000000030`、总质量 `16999991644`、精确余量 `8866`，且逃逸行数为零。

The augmented control also passes, with minimum `1000000032`, mass `16999991652`, and surplus `8892`; because the base measure already passes, the endpoint improvement is not attributed to the augmented orbit. / 增广对照同样通过，最低为 `1000000032`、总质量为 `16999991652`、余量为 `8892`；由于基础测度已经通过，本次端点提升不归因于该增广轨道。

## Replay modes / 复验模式

A local records-and-integrity check needs only Python 3.10 or later. / 本地账本与完整性检查仅需要 Python 3.10 或更高版本。

```bash
python -X utf8 -B -S certificates/R038/verify.py --output .replay-runs/r038-records-001
```

Only a replay with the exact pinned upstream certificate recomputes all geometric obligations. / 只有提供精确锁定的上游证书后，复验才会重新计算全部几何义务。

```bash
python -X utf8 -B -S certificates/R038/verify.py \
  --certificate path/to/certificate.json \
  --output .replay-runs/r038-full-001
```

Windows users may use the bundled PowerShell helper, which downloads only the pinned upstream file and checks its SHA-256 before replay. / Windows 用户可使用随附的 PowerShell 辅助脚本；它只下载锁定的上游文件，并在复验前检查 SHA-256。

```powershell
powershell -ExecutionPolicy Bypass -File certificates/R038/fetch_and_replay.ps1 -OutputDir .replay-runs/r038-full-001
```

The complete success marker is `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`; `PASS_R038_RECORDS_ONLY` is deliberately weaker and is not a geometric proof replay. / 完整成功标记为 `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`；`PASS_R038_RECORDS_ONLY` 被有意设置为更弱的账本检查，不能当作几何证明复演。

## Scope / 范围

This is a computer-assisted lower bound and not an equality for $s(17)$, a new packing construction, an optimality proof, external peer review, formal verification, or a priority claim. / 这是计算机辅助下界，不代表 $s(17)$ 的精确值、新装填构造、最优性证明、外部同行审查、形式化验证或首发确认。

The raw upstream certificate is not redistributed in this directory; reproducibility therefore depends on the pinned public source remaining obtainable or on the reader supplying identical bytes. / 本目录不重新分发上游证书原字节，因此冷启动复验依赖锁定公开来源仍可取得，或由读者自行提供完全相同的字节。
