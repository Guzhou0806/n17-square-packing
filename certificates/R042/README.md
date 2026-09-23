# R042 strict lower-bound certificate / R042 严格下界证书

R042 is a computer-assisted exact certificate for seventeen arbitrarily rotated unit squares. / R042 是关于十七个可任意旋转单位正方形的计算机辅助精确证书。

$$\boxed{s(17)>\frac{115325}{24963}=4.6198373592917517926531266274\ldots}$$

The frozen parent side is $A=24963/25000$ inside the outer side $L=4613/1000$, so $L/A=115325/24963$. / 冻结父方块边长为 $A=24963/25000$，外框边长为 $L=4613/1000$，因此 $L/A=115325/24963$。

The public certificate bytes are stored as deterministic gzip and decompress to SHA-256 `ad47686fdc49121d23b335a1d0cbfc8aa706a5d34bb0eb896aea6992db3d59de`. / 公开证书字节以确定性 gzip 存储，解压后的 SHA-256 为 `ad47686fdc49121d23b335a1d0cbfc8aa706a5d34bb0eb896aea6992db3d59de`。

[Proof / 证明](PROOF.md) · [Reproducibility / 可复验性](REPRODUCIBILITY.md) · [Attribution / 来源](ATTRIBUTION.md) · [Claims / 结论账本](CLAIMS.json)

## Fast records check / 快速账本检查

Python 3.10 or later is sufficient for the package-local identity, arithmetic, ledger, and manifest checks. / 包内身份、算术、账本与清单检查只需要 Python 3.10 或更高版本。

```bash
python -X utf8 -B -S certificates/R042/verify.py --output .replay-runs/r042-records-001
```

The records-only success marker is `PASS_R042_RECORDS_ONLY`, and it is intentionally not a fresh geometric replay. / 仅账本检查的成功标记为 `PASS_R042_RECORDS_ONLY`，并且它被有意设置为不代表新的几何复演。

## Independent containment replay / 独立包含复验

The independent containment path uses only the Python standard library and recomputes all 31,412 rational quadratic inequalities. / 独立包含路径只使用 Python 标准库，并重新计算全部 31,412 个有理二次不等式。

```bash
python -X utf8 -B -S certificates/R042/verify.py --containment --output .replay-runs/r042-containment-001
```

## Complete exact replays / 完整精确复演

The Python exact sweep requires NumPy and Numba and recomputes all 7,853 parent-angle rows. / Python 精确扫描需要 NumPy 与 Numba，并重新计算全部 7,853 个父角目录行。

```bash
python -X utf8 -B certificates/R042/verify.py --python-full --jobs 4 --output .replay-runs/r042-python-001
```

The source-distinct BigInt replay requires Node.js and reconstructs its checker from SHA-pinned R038 source bytes before scanning all 7,853 rows. / 不同源码的 BigInt 复演需要 Node.js，并在扫描全部 7,853 行之前从 SHA 锁定的 R038 源字节重建检查器。

```bash
python -X utf8 -B -S certificates/R042/verify.py --bigint-full --jobs 4 --output .replay-runs/r042-bigint-001
```

The reconstructed BigInt checker is never committed in this package; only the pinned reconstruction recipe is distributed. / 重建后的 BigInt 检查器从不提交到本成果包；公开分发的只有锁定的重建配方。

R042 does not assert maximality, global optimality, established priority, external peer review, or proof-assistant formalization. / R042 不主张端点已达极限、全局最优、已确认首发、外部同行审查或证明助理形式化。
