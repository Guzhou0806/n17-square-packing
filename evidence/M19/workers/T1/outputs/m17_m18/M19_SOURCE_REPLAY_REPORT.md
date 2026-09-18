# M19 原来源 sweep 独立复演报告

日期：2026-09-17。状态：**PASS_EXACT_MATCH_17**。

按 `coord/m17_m18/M19_COMPUTE_AUTHORIZATION.json`，执行冻结的
`m19_source_replay_v2.py`，仅重算 M17 已经产生的 17 个中点方向；没有计算其余方向、运行搜索或调用旧 v1。

## 结果

- 完成 `17/17` 行，用时 `3.6047356000635773` 秒，低于 30 秒软上限。
- 行序严格为 `[0,89,179,1,2,...,14]`。
- 16 个通过方向的来源 NumPy 二维差分 sweep 最小质量均与 M17 标准库 segment-tree 结果精确相同；通过索引为 `{0,...,13,89,179}`。
- 失败方向 `k=14` 的来源结果为 `197153/200000`，与 M17 精确相同，仍不超过严格门槛 `423327/425000`。
- 17 行全部 `minimum_matches=true`。
- 对来源 sweep 返回的 17 个 `(u,v)` 见证中心逐原子直接精确计数，全部 `direct_witness_matches=true`。
- NumPy 从工作区 `.deps/m2/site-packages/numpy/__init__.py` 加载，版本 `2.5.3`；namespace shim 已启用，没有执行保留的 `sqpack/__init__.py`。

## 证据绑定

- `m19_replay/RESULT.json` SHA-256：`052b4dbbacdc0ddf5c08c569516d90cf7e7238deb9919e8e02d518e705f0a3fe`
- `m19_replay/ROWS.jsonl` SHA-256：`f480412ee29b4da83141a8666f96161a10d96868cc5ed612050b350b5c4eed8f`
- 授权 SHA-256：`4e584e474d7f3b4f590877aeaa467d1f403bd5fb077c9a8b9ab81be8e758d79e`
- 执行 harness SHA-256：`61bf58e4f6d64c9ef016dfe1ee3c53ea1182f93b91be390181876847b4ba6e8d`
- T0 已生产的 `research/m19_work/CERTIFICATE.json` SHA-256：`4326a84caec0a60c0f70226c7a79bf4bbede2d1c032af8ca2aef319d2c91c806`；其当前自声明为 `PRODUCED_AWAITING_INDEPENDENT_AUDIT`。

## 审查结论

本复演独立支持两项事实：M19 纳入的全部 16 个中点都严格通过质量门槛；M17 的 `k=14` 缺口也由不同覆盖实现复现，不是生产 sweep 的单实现假象。因此 M19 预审所述 197 节点非均匀网的新增覆盖前提已获本轮来源实现交叉验证。

本报告不替代 T2 对 M19 完整证书、197 节点集合、最大隙、缩放代数和最终下界的独立验收；在该验收完成前，不把 T0 生产证书的待审状态升级为正式项目下界。
