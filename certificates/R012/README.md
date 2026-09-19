# R012 reproducible certificate / R012 可复验证书

**s(17) >= 461300/99999 = 4.61304613046130461304...**

[Proof / 证明](PROOF.md) · [Attribution / 来源](ATTRIBUTION.md)

This is a public, Python-only representation of the R012 mathematical data. The 206-row integer orbit table expands to exactly the same 1616 atoms; all 2925 parent-angle intervals have identical rational geometry. No planning documents, private workspace, numerical optimizer, account, compiler or network is required.

本目录是 R012 数学数据的纯 Python 公开表示；1616 个原子与 2925 项父角目录的精确几何未变，不需要研究工作区、优化器、账号、编译器或网络。

## Full replay / 完整复验

Python 3.10 or later, standard library only. From the repository root:

```bash
python -X utf8 -B -S certificates/R012/test_verify.py
python -X utf8 -B -S certificates/R012/verify.py --workers 4 --output .replay-runs/r012-001
```

The output directory must not exist. Two workers are the default; reduce the count on smaller computers. Every one of the 2925 entries is recomputed over its entire continuous parent-center envelope. A new `coverage.jsonl` and `RESULT.json` are written. Runtime depends on hardware; allow several minutes rather than assuming the old C++ timing.

输出目录必须是新目录。默认两个计算进程，可按机器调整；每一条目都重新扫描完整连续父中心域，输出逐项日志与结果。纯 Python 的耗时不能沿用原 C++ 的计时，应预留数分钟或更长。

Only a complete successful run prints:

```text
PASS_COMPLETE_PARENT_CATALOGUE_GLOBAL_LOWER_BOUND
```

A non-coverage check is explicitly separate:

```bash
python -X utf8 -B -S certificates/R012/verify.py --records --output .replay-runs/r012-records-001
```

It prints `PASS_RECORDS_ONLY`, never the full marker. Do not use `-O`, `-OO` or `PYTHONOPTIMIZE`.

records 只检查文件、精确算术与五个反例，不证明覆盖；禁止用它代替完整模式，也不要使用优化模式。

## Scope / 范围

The result is a computer-assisted lower bound, not an equality for s(17), a packing construction, independent peer review, formalization or a priority claim. Public replay is independent of how the weights and selector were discovered, but not an independently designed second geometric proof.

结论是计算机辅助下界，不是 s(17) 的精确值、新装填、外部审稿、形式化证明或首发认证。复验不信任发现过程，但仍需审查共享的事件几何。
