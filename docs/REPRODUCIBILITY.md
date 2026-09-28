# R067：4.66018 / R067: 4.66018

Kleddamag4.66001收费保持不变，新的严格核与2808个角区间完成4.66018；旧证书包保留。 / Retaining Kleddamag's 4.66001 charge, new strict cores and2808 angular intervals establish4.66018; earlier certificate packages remain intact.

[证明与复验 / Proof and replay](../certificates/R067-4.66018/README.md) · [来源 / Attribution](../certificates/R067-4.66018/ATTRIBUTION.md)

> 以下为历史发布记录，关于内部结果、未公开状态或尚未证明目标的文字仅描述各次发布当时的状态，不是当前结论；当前已接受R067的4.66018及Kleddamag公开4.66001基线。 / The following historical release records describe the status at their respective publication dates, including private results and then-unproved targets; they are not current conclusions. The current accepted result is R067 at4.66018, continuing Kleddamag's public4.66001 baseline.

# 可复验性 / Reproducibility

## R052 延续历史发布 / R052 continuation historical publication

记录、包含及完整Python/BigInt命令见[4.62003复验说明 / 4.62003 reproduction](../certificates/R052-4.62003/REPRODUCIBILITY.md)。 / See the linked instructions for records, containment and complete Python/BigInt commands.

## R052 原发布 / R052 original publication

标准库记录核查、包含重算及完整 Python/BigInt 命令见 [R052 复验说明 / R052 reproduction](../certificates/R052/REPRODUCIBILITY.md)。 / See the linked R052 instructions for standard-library recorded checks, containment recomputation and full Python/BigInt commands.

## R050 历史发布 / R050 historical publication

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
