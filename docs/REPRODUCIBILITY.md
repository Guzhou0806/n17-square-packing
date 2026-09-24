# 可复验性 / Reproducibility

## R050 当前发布 / R050 current publication

完整命令、依赖、记录核查与重新扫描的区别，见 [R050 复验说明 / R050 reproduction instructions](../certificates/R050/REPRODUCIBILITY.md)。 / See the linked instructions for complete commands, dependencies and the distinction between recorded checks and rescans.

```bash
python -X utf8 -B -S certificates/R050/verify.py --output .replay-runs/r050-records-001
python -X utf8 -B -S certificates/R050/verify.py --containment --output .replay-runs/r050-containment-001
python -m pip install -r certificates/R050/requirements-full.txt
python -X utf8 -B certificates/R050/verify.py --python-full --jobs 8 --output .replay-runs/r050-python-001
python -X utf8 -B -S certificates/R050/verify.py --bigint-full --jobs 8 --output .replay-runs/r050-bigint-001
```

## 历史入口 / Historical entry points

[R043](../certificates/R043/REPRODUCIBILITY.md) · [R042](../certificates/R042/REPRODUCIBILITY.md) · [R038](../certificates/R038/REPRODUCIBILITY.md) · [R012](../certificates/R012/README.md)

历史证据保持原始字节。文件身份、程序复验与外部数学审查是不同层级。 / Historical evidence retains its original bytes. File identity, computational replay and external mathematical review are distinct levels.
