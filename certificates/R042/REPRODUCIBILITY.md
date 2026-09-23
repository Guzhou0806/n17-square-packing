# Reproducibility / 可复验性

## Frozen identity / 冻结身份

The deterministic gzip file `certificate/R042_CERTIFICATE.json.gz` decompresses to the exact accepted certificate bytes with SHA-256 `ad47686fdc49121d23b335a1d0cbfc8aa706a5d34bb0eb896aea6992db3d59de`. / 确定性 gzip 文件 `certificate/R042_CERTIFICATE.json.gz` 解压后得到精确的已接受证书字节，其 SHA-256 为 `ad47686fdc49121d23b335a1d0cbfc8aa706a5d34bb0eb896aea6992db3d59de`。

The compressed file itself has SHA-256 `ec79424e30c65bbf31ad1f020b55cc8acebd0cb0f4fbea3e1841fa2b6dda8e28`. / 压缩文件本身的 SHA-256 为 `ec79424e30c65bbf31ad1f020b55cc8acebd0cb0f4fbea3e1841fa2b6dda8e28`。

## Records-only check / 仅账本检查

The records-only path needs Python 3.10 or later and no third-party modules or network access. / 仅账本路径需要 Python 3.10 或更高版本，不需要第三方模块或网络访问。

```bash
python -X utf8 -B -S certificates/R042/verify.py --output .replay-runs/r042-records-001
```

It checks the decompressed certificate identity, theorem arithmetic, compact replay ledgers, cross-implementation histogram agreement, and the package manifest. / 它检查解压证书身份、定理算术、精简复演账本、跨实现直方图一致性以及成果包清单。

## Independent rational containment / 独立有理包含

The independent containment checker is standard-library-only and shares no sweep implementation with the all-centre replay. / 独立包含检查器只使用标准库，并且不与全中心复演共享扫描实现。

```bash
python -X utf8 -B -S certificates/R042/verify.py --containment --output .replay-runs/r042-containment-001
```

Fresh output must agree exactly with the frozen 31,412-inequality ledger. / 新鲜输出必须与冻结的 31,412 个不等式账本完全一致。

## Python full exact replay / Python 完整精确复演

The Python full path requires NumPy and Numba and is intentionally much heavier than the records check. / Python 完整路径需要 NumPy 与 Numba，并且有意比账本检查显著更重。

```bash
python -m pip install numpy numba
python -X utf8 -B certificates/R042/verify.py --python-full --jobs 4 --output .replay-runs/r042-python-001
```

The verifier recomputes all 7,853 rows and checks every deterministic aggregate plus a SHA-256 digest of the complete row ledger. / 验证器重新计算全部 7,853 行，并检查每个确定性汇总以及完整逐行账本的 SHA-256 摘要。

## BigInt full exact replay / BigInt 完整精确复演

The BigInt full path requires Node.js and network access to fetch one SHA-pinned R038 source file. / BigInt 完整路径需要 Node.js，并需要联网获取一个 SHA 锁定的 R038 源文件。

```bash
python -X utf8 -B -S certificates/R042/verify.py --bigint-full --jobs 4 --output .replay-runs/r042-bigint-001
```

`src/prepare_secondary.py` verifies the R038 source SHA, applies the published byte-edit recipe, verifies the reconstructed checker SHA, and writes the checker only to an untracked local cache. / `src/prepare_secondary.py` 会核验 R038 源文件 SHA、应用公开字节编辑配方、核验重建检查器 SHA，并且只把检查器写入未跟踪的本地缓存。

The repository never contains the reconstructed checker bytes. / 本仓库从不包含重建后的检查器字节。

## Output discipline / 输出纪律

Every verifier mode requires a new output directory and rejects Python optimization mode. / 验证器的每种模式都要求使用全新的输出目录，并拒绝 Python 优化模式。

Source-session timing is not an acceptance condition because runtime depends on hardware and runner load. / 来源会话耗时不属于验收条件，因为运行时间取决于硬件与执行器负载。
