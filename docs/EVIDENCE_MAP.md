# 证据入口 / Evidence map

## R050

[证书包 / Certificate package](../certificates/R050/README.md) 与 [证明 / proof](../certificates/R050/PROOF.md) 连接资源预算、连续覆盖和严格下界。 / The linked package and proof connect resource budgets, continuous coverage and the strict lower bound.

`certificate/R050_CERTIFICATE.json.gz` 保存完整原证书，解压 SHA-256 为 84283b2af955b85184dc4793ae2b65e08aae5f3817a611038598dd54f479f400。 / `certificate/R050_CERTIFICATE.json.gz` preserves the original complete certificate, with decompressed SHA-256 84283b2af955b85184dc4793ae2b65e08aae5f3817a611038598dd54f479f400.

`results/R050_PYTHON_FULL_REPLAY.json.gz` 保存完整 Python 行账本，`results/bigint-parts/` 保存 118 个完整连续分块，`verify.py` 核查每块完整直方图。 / `results/R050_PYTHON_FULL_REPLAY.json.gz` preserves the full Python row ledger, `results/bigint-parts/` preserves 118 complete contiguous blocks, and `verify.py` checks each full block histogram.

`SOURCE_PIN.json` 锁定源码，`MANIFEST.json` 是显式允许文件及哈希表，`R050_PUBLICATION.json` 在仓库根登记本次集成发布字节。 / `SOURCE_PIN.json` pins source identities, `MANIFEST.json` lists allowed files and hashes, and root `R050_PUBLICATION.json` records this publication's integration bytes.

[来源 / Sources](../certificates/R050/SOURCE_NOTICES.md) 明确上游贡献与 Kleddamag 尚未公开的 4.62001 下界归属，该项未公开证明不属于本包。 / The source notice identifies upstream contributions and credits Kleddamag's unpublished 4.62001 lower bound, whose proof is not part of this package.

## 历史证据 / Historical evidence

R043、R042、R038、R012 和 M19 的科学证据保持不变。 / Scientific evidence for R043, R042, R038, R012 and M19 is unchanged.
