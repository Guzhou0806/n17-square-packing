# HANDOFF｜M12 source-faithful replay

状态：`SOURCE_AND_SCALED_PASS_AWAITING_INDEPENDENT_REVIEW`

- 锁 commit `035d84c655b4047bc9986c9a3db5106780d92f77`。
- source 与 fixed-λ scaled 各单工重放 181 方向、全部五条件通过。
- source/scaled minimum 均 `200009/200000`，worst label 均 `0`；181 项逐方向 tuple 完全一致。
- scaled `L=459000459/100000000=4.59000459`；粗 containment 余量 `2793464693461/900000000000000000>0`。
- 逐方向比较：`results/DIRECTIONS_COMPARISON.jsonl`，SHA-256 `F639E846...96BE1`；mismatch `[]`。
- source 结果 SHA-256 `4AD6D4FF...1E3E0`；scaled 结果 `D0725160...EE02`；scaled certificate `6979561E...5980C`。
- 环境 Python 3.12.13 / NumPy 2.5.3；项目声明 Python 3.14。首次因缺失 `os.process_cpu_count` 在 0 方向失败并保留。唯一获批 wrapper 映射到 `os.cpu_count`；显式 workers=1，数学计算未变。无第二 shim。
- wall 38.85 s + 40.96 s；实际 PeakWorkingSet unknown；输出约 179 KB。
- 获取 8 requests / 204,883 bytes；无优化、λ 搜索、调参或并行。
- 等待 T2 将本逐方向文件与 T0 独立 sweep 比较并审查缩放定理后再登记；当前不单方面更新全局界。

完整证据和限制见 `M12_REPORT.md`、`PROTOCOL.md`、`COMPATIBILITY_ADDENDUM.md` 与 `results/`。
