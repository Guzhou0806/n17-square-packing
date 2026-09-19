# Reproducibility / 可复验性

## R012 — current milestone / 当前里程碑

[Full instructions / 完整说明](../certificates/R012/README.md) · [Proof / 证明](../certificates/R012/PROOF.md)

Requirements: Python 3.10+, no third-party modules. From the repository root:

```bash
python -X utf8 -B -S certificates/R012/test_verify.py
python -X utf8 -B -S certificates/R012/verify.py --workers 4 --output .replay-runs/r012-001
```

The output must be new. The public replay expands 206 integer D4 orbit rows, checks exact measure identity, builds all 2925 parent-angle entries, proves interval containment/closure, and scans each complete parent-center envelope. Every returned minimum is directly recounted. Five unsuccessful core recipes are independently checked as controls. Only completion of every obligation produces `PASS_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND`.

输出目录必须尚不存在。公开入口重建原子、目录、严格包含及接缝，扫描每项完整连续父中心域，并逐原子核对最小见证。五个失败配方作为控制保留，全部完成后才输出全局证明标记。

`--records` checks metadata, arithmetic and witnesses only; it is never equivalent to full replay. Numerical search and optimization are not part of acceptance. Multiple computation workers do not constitute independent research reviewers.

records 没有几何覆盖重算；计算进程数量不代表独立审查人数。新公开入口只用 Python，不能沿用原 C++ 耗时或把两者误称为不同理论证明。

## M19 — unchanged historical entry / 未改动的历史入口

```bash
python -X utf8 -B verify.py --output .replay-runs/m19-001
```

This separately recomputes 181 old directions and 17 trial directions, preserving 197 certified directions and one exact failure. Its marker is `PASS_FULL_REPLAY`. The optional source implementation uses NumPy:

```bash
python scripts/source_crosscheck.py --help
```

M19 仍独立重算旧方向和新增试验方向，保留失败；原科学文件、哈希和默认入口不变。

## Trust / 可信边界

File hashes establish identity, not mathematical validity. Exact program execution is not external peer review or a proof-assistant formalization. Review strict interior containment, complete center enumeration and use of a common measure in the proofs.

哈希只绑定文件，不能替代数学检查；审查重点包括严格内部核、连续中心完备性与共同质量预算。
