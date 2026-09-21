# Evidence map / 证据入口

## R038

`certificates/R038/CLAIMS.json` states the public theorem ledger, while `SOURCE_PIN.json` binds the exact upstream certificate by repository, commit, path, byte count, and SHA-256. / `certificates/R038/CLAIMS.json` 登记公开定理账本，而 `SOURCE_PIN.json` 通过仓库、提交、路径、字节数与 SHA-256 锁定精确上游证书。

`results/R038_CONTAINMENT.json` records the strict-containment transfer, and the two chunk ledgers record the base and augmented exact scans. / `results/R038_CONTAINMENT.json` 记录严格内含转移，两个分块账本分别记录基础与增广精确扫描。

`src/exact_parent_side_scan.js` is the source-distinct exact event-cell scanner, and `verify.py` binds the frozen records to an optional cold geometric replay. / `src/exact_parent_side_scan.js` 是不同源码的精确事件胞元扫描器，`verify.py` 将冻结记录与可选的冷启动几何复演绑定。

`PROOF.md` connects those computations to the strict global lower bound, while `ATTRIBUTION.md` and `LICENSE_SCOPE.md` state provenance and redistribution boundaries. / `PROOF.md` 将这些计算连接到严格全局下界，而 `ATTRIBUTION.md` 与 `LICENSE_SCOPE.md` 说明来源与再分发边界。

The upstream certificate bytes are intentionally absent from this repository, so full replay obtains them separately and accepts only the pinned SHA. / 上游证书字节被有意排除在本仓库之外，因此完整复演需另行取得，并且只接受锁定 SHA。

## R012

`certificates/R012/orbits.json` and `catalogue.json` define the self-contained R012 mathematical object, while its verifier recomputes all 2,925 complete parent-centre envelopes. / `certificates/R012/orbits.json` 与 `catalogue.json` 定义自包含的 R012 数学对象，其验证器重新计算全部 2,925 个完整父中心包络。

R012 remains unchanged by R038 and retains its own manifest, proof, attribution, and negative controls. / R012 未被 R038 修改，并继续保留自己的清单、证明、署名与负对照。

## M19

[Proof / 证明](M19_PROOF_EN.md) · [original package / 原包](../evidence/M19/README.md) · [machine certificate / 机器证书](../evidence/M19/research/m19_work/CERTIFICATE.json) · [acceptance record / 验收记录](../evidence/M19/FINAL_ACCEPTANCE.json)

The M19 historical package remains unchanged, and no R038 success marker is inherited from M19 or R012. / M19 历史包保持不变，R038 不从 M19 或 R012 继承任何成功标记。
