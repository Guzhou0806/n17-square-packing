# Evidence map / 证据入口

## R043

`certificates/R043/CLAIMS.json` states the public theorem ledger, while `SOURCE_PIN.json` binds the inherited architecture and the source-distinct checker reconstruction chain. / `certificates/R043/CLAIMS.json` 登记公开定理账本，而 `SOURCE_PIN.json` 锁定继承架构与不同源码检查器的重建链。

`certificate/R043_CERTIFICATE.json.gz` contains the complete accepted certificate bytes in deterministic compressed form, and `verify.py` checks the decompressed SHA before use. / `certificate/R043_CERTIFICATE.json.gz` 以确定性压缩形式包含完整已接受证书字节，`verify.py` 在使用前会核验解压 SHA。

`results/R043_PYTHON_FULL_REPLAY.json.gz` and `results/R043_BIGINT_FULL_REPLAY.json` record the two completed full exact replay ledgers, while `R043_INDEPENDENT_CONTAINMENT.json` records the independent rational containment audit. / `results/R043_PYTHON_FULL_REPLAY.json.gz` 与 `results/R043_BIGINT_FULL_REPLAY.json` 记录两次已完成的完整精确复演账本，而 `R043_INDEPENDENT_CONTAINMENT.json` 记录独立有理包含审计。

`src/prepare_secondary.py` plus `secondary-adaptation.json` reconstructs the source-distinct BigInt checker from pinned public R038 source bytes without committing the derived checker. / `src/prepare_secondary.py` 与 `secondary-adaptation.json` 从锁定的公开 R038 源字节重建不同源码的 BigInt 检查器，而不提交派生检查器。

`PROOF.md` connects the finite computations to the strict global lower bound, while `ATTRIBUTION.md` and `LICENSE_SCOPE.md` state provenance and redistribution boundaries. / `PROOF.md` 将有限计算连接到严格全局下界，而 `ATTRIBUTION.md` 与 `LICENSE_SCOPE.md` 说明来源与再分发边界。

## Earlier milestones / 早期里程碑

R042, R038, R012, and M19 remain unchanged and retain their original evidence and replay paths. / R042、R038、R012 与 M19 保持不变，并继续保留各自原有的证据与复验路径。
