# Reproducibility / 可复验性

## R038 — current milestone / R038：当前里程碑

[Full instructions / 完整说明](../certificates/R038/REPRODUCIBILITY.md) · [Proof / 证明](../certificates/R038/PROOF.md)

A records-only check requires Python 3.10 or later and no external source file. / 仅账本检查需要 Python 3.10 或更高版本，不需要外部来源文件。

```bash
python -X utf8 -B -S certificates/R038/verify.py --output .replay-runs/r038-records-001
```

A complete replay requires the pinned upstream certificate and Node.js. / 完整复演需要锁定的上游证书与 Node.js。

```bash
python -X utf8 -B -S certificates/R038/verify.py \
  --certificate path/to/certificate.json \
  --output .replay-runs/r038-full-001
```

The full path checks the upstream SHA, recomputes five exact chunks for the base measure and five exact chunks for the augmented control, and compares every chunk with the frozen ledgers. / 完整路径检查上游 SHA，为基础测度重算五个精确分块、为增广对照重算五个精确分块，并逐块与冻结账本比较。

Only complete agreement produces `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`; the records-only marker never implies geometric coverage. / 只有全部一致时才输出 `PASS_R038_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`；仅账本标记从不代表几何覆盖成立。

## R012 — unchanged earlier milestone / R012：未改动的早期里程碑

R012 remains fully self-contained and Python-only after checkout. / R012 在检出仓库后仍保持完全自包含且只需 Python。

```bash
python -X utf8 -B -S certificates/R012/test_verify.py
python -X utf8 -B -S certificates/R012/verify.py --workers 4 --output .replay-runs/r012-001
```

Its complete marker remains `PASS_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`. / 其完整成功标记仍为 `PASS_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`。

## M19 — unchanged historical entry / M19：未改动的历史入口

```bash
python -X utf8 -B verify.py --output .replay-runs/m19-001
```

M19 retains its original `PASS_FULL_REPLAY` path and frozen evidence. / M19 保留原 `PASS_FULL_REPLAY` 路径与冻结证据。

## Trust boundary / 可信边界

File hashes establish byte identity and replay establishes the programmed obligations, but neither alone is external mathematical review. / 文件哈希建立字节身份，复演建立程序化义务，但二者都不能单独替代外部数学审查。

Review the strict containment, complete continuous centre-domain enumeration, common-measure counting, rescaling, and compactness arguments in the proof documents. / 应审查证明文档中的严格内含、完整连续中心域枚举、共同测度计数、缩放与紧致性论证。
