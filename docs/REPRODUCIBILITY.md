# Reproducibility / 可复验性

## R042 — current milestone / R042：当前里程碑

[Full instructions / 完整说明](../certificates/R042/REPRODUCIBILITY.md) · [Proof / 证明](../certificates/R042/PROOF.md)

The fast package-local check requires Python 3.10 or later and no third-party modules. / 快速包内检查需要 Python 3.10 或更高版本，并且不需要第三方模块。

```bash
python -X utf8 -B -S certificates/R042/verify.py --output .replay-runs/r042-records-001
```

The independent containment replay is also standard-library-only and recomputes all 31,412 exact rational inequalities. / 独立包含复验同样只使用标准库，并重新计算全部 31,412 个精确有理不等式。

```bash
python -X utf8 -B -S certificates/R042/verify.py --containment --output .replay-runs/r042-containment-001
```

The complete Python replay requires NumPy and Numba, and the complete BigInt replay requires Node.js plus network access to one SHA-pinned R038 source file. / 完整 Python 复演需要 NumPy 与 Numba，完整 BigInt 复演需要 Node.js，并需要联网获取一个 SHA 锁定的 R038 源文件。

```bash
python -X utf8 -B certificates/R042/verify.py --python-full --jobs 4 --output .replay-runs/r042-python-001
python -X utf8 -B -S certificates/R042/verify.py --bigint-full --jobs 4 --output .replay-runs/r042-bigint-001
```

Only the selected fresh full-replay path can produce its corresponding fresh full-replay marker; records-only success never inherits a geometric PASS from an earlier milestone. / 只有实际完成所选冷启动完整复演路径才能产生对应的新鲜完整复演标记；仅账本成功从不从更早里程碑继承几何 PASS。

## R038 — unchanged earlier milestone / R038：未改动的早期里程碑

R038 retains its original replay entry points and frozen source pins. / R038 保留原有复演入口与冻结来源锁定信息。

## R012 — unchanged earlier milestone / R012：未改动的早期里程碑

R012 remains fully self-contained and Python-only after checkout. / R012 在检出仓库后仍保持完全自包含且只需 Python。

## M19 — unchanged historical entry / M19：未改动的历史入口

M19 retains its original `PASS_FULL_REPLAY` path and frozen evidence. / M19 保留原 `PASS_FULL_REPLAY` 路径与冻结证据。

## Trust boundary / 可信边界

File hashes establish byte identity and replay establishes the programmed obligations, but neither alone is external mathematical review. / 文件哈希建立字节身份，复演建立程序化义务，但二者都不能单独替代外部数学审查。

Review the mixed-charge counting rule, strict containment, complete continuous centre-domain enumeration, common budget, rescaling, and compactness arguments in the proof documents. / 应审查证明文档中的混合收费计数规则、严格包含、完整连续中心域枚举、共同预算、缩放与紧致性论证。
