# R043 reproducibility / R043 可复验性

A package-local recorded check requires Python 3.10 or later and no third-party modules. / 包内记录检查需要 Python 3.10 或更高版本，并且不需要第三方模块。

```bash
python -X utf8 -B -S verify.py --output .replay-runs/r043-recorded-001
```

A fresh independent containment replay also uses only the Python standard library. / 新鲜的独立包含复演同样只使用 Python 标准库。

```bash
python -X utf8 -B -S verify.py --containment --output .replay-runs/r043-containment-001
```

The complete Python exact replay requires NumPy and Numba. / 完整 Python 精确复演需要 NumPy 与 Numba。

```bash
python -m pip install numpy numba
python -X utf8 -B verify.py --python-full --jobs 4 --output .replay-runs/r043-python-001
```

The source-distinct BigInt replay requires Node.js and reconstructs its checker from a SHA-pinned public R038 source file plus the committed deterministic adaptation recipe. / 不同源码的 BigInt 复演需要 Node.js，并从 SHA 锁定的公开 R038 来源文件与本包提交的确定性 adaptation recipe 现场重建检查器。

```bash
python -X utf8 -B -S verify.py --bigint-full --jobs 5 --output .replay-runs/r043-bigint-001
```

The reconstructed BigInt checker itself is not redistributed in this package. / 本包不重新分发重建后的 BigInt 检查器本体。

Complete acceptance requires the final certificate SHA, all 7,853 rows, identical Python/BigInt global minimum and complete row-minimum histogram, zero BigInt escape rows, all 31,412 independent strict-containment inequalities, and a strictly positive counting surplus. / 完整验收要求最终证书 SHA 一致、全部 7,853 行完成、Python/BigInt 的全局最低值与完整逐行最低值直方图一致、BigInt escape rows 为零、31,412 个独立严格包含不等式全部通过，并且计数余量严格为正。
