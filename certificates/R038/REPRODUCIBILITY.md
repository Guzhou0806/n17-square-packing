# Reproducibility / 可复验性

## Local records check / 本地账本检查

Python 3.10 or later is sufficient for the package-local arithmetic, result-ledger, and manifest checks. / 包内精确算术、结果账本与清单检查只需要 Python 3.10 或更高版本。

```bash
python -X utf8 -B -S certificates/R038/verify.py --output .replay-runs/r038-records-001
```

This mode prints `PASS_R038_RECORDS_ONLY` and does not recompute the 4,391 geometric rows. / 此模式输出 `PASS_R038_RECORDS_ONLY`，不会重新计算 4,391 个几何目录行。

## Full geometric replay / 完整几何复演

A full replay additionally requires Node.js and the exact pinned upstream certificate. / 完整复演还需要 Node.js 与精确锁定的上游证书。

```bash
python -X utf8 -B -S certificates/R038/verify.py \
  --certificate path/to/certificate.json \
  --output .replay-runs/r038-full-001
```

The verifier first checks the certificate SHA-256, then invokes `src/exact_parent_side_scan.js` over five fixed row ranges for the base measure and the augmented control, and finally compares every chunk with the frozen result ledgers. / 验证器首先检查证书 SHA-256，随后对基础测度与增广对照分别在五个固定行区间上调用 `src/exact_parent_side_scan.js`，最后逐块与冻结结果账本比较。

Only complete agreement produces `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`. / 只有全部一致时才输出 `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`。

The output directory must not exist before a run, and optimized Python execution with `-O`, `-OO`, or `PYTHONOPTIMIZE` is rejected. / 每次运行前输出目录必须不存在，并拒绝使用 `-O`、`-OO` 或 `PYTHONOPTIMIZE` 的 Python 优化执行。

## Windows helper / Windows 辅助脚本

The PowerShell helper downloads the exact pinned file from the pinned commit, verifies its SHA-256, and starts the full replay. / PowerShell 辅助脚本从锁定提交下载精确文件、核验 SHA-256，并启动完整复演。

```powershell
powershell -ExecutionPolicy Bypass -File certificates/R038/fetch_and_replay.ps1 -OutputDir .replay-runs/r038-full-001
```

The helper does not install Python or Node.js and does not substitute a newer upstream certificate. / 该脚本不会安装 Python 或 Node.js，也不会用更新版本的上游证书替代锁定文件。

## Trust boundary / 可信边界

The replay checks the published computational obligations and file identity, but it is not external peer review or a proof-assistant formalization. / 复演检查已发布的计算义务与文件身份，但不等于外部同行审查或证明助理形式化。

The proof should also be reviewed for the finite-to-continuous event-cell argument, strict interior containment, common-measure counting, and compactness step used to make the endpoint exclusion strict. / 证明仍应审查有限到连续的事件胞元论证、严格内部包含、共同测度计数，以及将端点排除提升为严格下界所使用的紧致性步骤。
