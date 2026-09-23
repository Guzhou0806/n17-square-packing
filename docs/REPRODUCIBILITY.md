# Reproducibility / 可复验性

## R043 — current milestone / R043：当前里程碑

[Full instructions / 完整说明](../certificates/R043/REPRODUCIBILITY.md) · [Proof / 证明](../certificates/R043/PROOF.md)

The fast package-local check requires Python 3.10 or later and no third-party modules. / 快速包内检查需要 Python 3.10 或更高版本，并且不需要第三方模块。

```bash
python -X utf8 -B -S certificates/R043/verify.py --output .replay-runs/r043-recorded-001
```

The independent containment replay is standard-library-only and recomputes all 31,412 exact rational inequalities. / 独立包含复演只使用标准库，并重新计算全部 31,412 个精确有理不等式。

```bash
python -X utf8 -B -S certificates/R043/verify.py --containment --output .replay-runs/r043-containment-001
```

The complete Python replay requires NumPy and Numba, and the complete BigInt replay requires Node.js plus network access to one SHA-pinned public R038 source file. / 完整 Python 复演需要 NumPy 与 Numba，完整 BigInt 复演需要 Node.js，并需要联网获取一个 SHA 锁定的公开 R038 源文件。

```bash
python -X utf8 -B certificates/R043/verify.py --python-full --jobs 4 --output .replay-runs/r043-python-001
python -X utf8 -B -S certificates/R043/verify.py --bigint-full --jobs 5 --output .replay-runs/r043-bigint-001
```

Records-only success never inherits a geometric PASS from an earlier milestone. / 仅记录检查成功从不从更早里程碑继承几何 PASS。

## Earlier milestones / 早期里程碑

R042, R038, R012, and M19 retain their original replay entry points and frozen evidence. / R042、R038、R012 与 M19 保留各自原有的复验入口与冻结证据。

## Trust boundary / 可信边界

File hashes establish byte identity and replay establishes the programmed obligations, but neither alone is external mathematical review. / 文件哈希建立字节身份，复演建立程序化义务，但二者都不能单独替代外部数学审查。

Review the mixed-charge counting rule, strict containment, complete continuous centre-domain enumeration, common budget, rescaling, and compactness arguments in the proof documents. / 应审查证明文档中的混合收费计数规则、严格包含、完整连续中心域枚举、共同预算、缩放与紧致性论证。
