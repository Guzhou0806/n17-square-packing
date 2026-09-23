# Evidence map / 证据入口

## R042

`certificates/R042/CLAIMS.json` states the public theorem ledger, while `SOURCE_PIN.json` binds the frozen R042 certificate, the Kled baseline identity, and the secondary-checker reconstruction chain. / `certificates/R042/CLAIMS.json` 登记公开定理账本，而 `SOURCE_PIN.json` 锁定冻结 R042 证书、Kled 基线身份与第二套检查器重建链。

`certificate/R042_CERTIFICATE.json.gz` contains the complete accepted certificate bytes in deterministic compressed form, and `verify.py` checks the decompressed SHA before using them. / `certificate/R042_CERTIFICATE.json.gz` 以确定性压缩形式包含完整已接受证书字节，`verify.py` 在使用前会核验解压 SHA。

`results/R042_PYTHON_FULL_REPLAY.json` and `results/R042_BIGINT_FULL_REPLAY.json` record the two completed full exact replay ledgers, while `R042_INDEPENDENT_CONTAINMENT.json` records the independent rational containment audit. / `results/R042_PYTHON_FULL_REPLAY.json` 与 `results/R042_BIGINT_FULL_REPLAY.json` 记录两次已完成的完整精确复演账本，而 `R042_INDEPENDENT_CONTAINMENT.json` 记录独立有理包含审计。

`src/prepare_secondary.py` plus `secondary-adaptation.json` reconstructs the source-distinct BigInt checker from pinned R038 source bytes without committing the derived checker. / `src/prepare_secondary.py` 与 `secondary-adaptation.json` 从锁定的 R038 源字节重建不同源码的 BigInt 检查器，而不提交派生检查器。

`PROOF.md` connects the finite computations to the strict global lower bound, while `ATTRIBUTION.md` and `LICENSE_SCOPE.md` state provenance and redistribution boundaries. / `PROOF.md` 将有限计算连接到严格全局下界，而 `ATTRIBUTION.md` 与 `LICENSE_SCOPE.md` 说明来源与再分发边界。

## R038

R038 remains unchanged and retains its SHA-pinned source, strict-containment transfer, exact expanded-domain replay, proof, and attribution files. / R038 保持不变，并继续保留其 SHA 锁定来源、严格内含转移、精确扩域复演、证明与来源文件。

## R012

R012 remains unchanged and retains its self-contained Python parent-angle certificate and negative controls. / R012 保持不变，并继续保留其自包含 Python 父角证书与负对照。

## M19

The M19 historical package remains unchanged, and no R042 success marker is inherited from M19, R012, or R038. / M19 历史包保持不变，R042 不从 M19、R012 或 R038 继承任何成功标记。
