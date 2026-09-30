# R071：4.66044275证书与条件联合几何 / Certificate at4.66044275 and conditional joint geometry

保留C027的4.66044275完整证书；C029新增固定锚点条件下17条冲突、2条强制空点及9≤Vmax≤11，不是4.6605全局下界。本次仅核对文件和已有记录，最终C++/BigInt复验交Actions，结果未观察。 / The retained C027 certificate states4.66044275. C029 adds17 conflicts,2 forced holes and9≤Vmax≤11 under a fixed-anchor condition, not a global bound of4.6605. Reception checked files and saved records only; final C++/BigInt replay is delegated to Actions and its outcome is unobserved.

[证明、数据与复验 / Proof, data and replay](../certificates/R071-C029/README.md)

> 以下为历史发布记录，状态按其发布日期理解。 / Below are historical publications; status statements refer to their publication dates.

# R070：4.6604427 / R070: 4.6604427

最新公开完整证明材料为s(17)>4.6604427，附5107区间双实现记录、319同预算增强规则及限定的方法类障碍。接收仅核对身份和记录，最终几何复验交Actions，结果未观察。 / The latest published complete proof materials state s(17)>4.6604427, with5107 paired interval records,319 same-budget enhanced rules and a scoped method-class obstruction. Reception checked identities and records only; final geometry replay is delegated to Actions and outcomes are unobserved.

[证明、数据与复验 / Proof, data and replay](../certificates/R070-4.6604427/README.md)

> 以下为历史发布内容，状态按各次发布时间解释。 / The following material is historical; status statements refer to each publication date.

# R068 / C010：提交最终CI复验 / Submitted for final CI replay

公开C009保留的4.66044完整证明材料及C010的局部连续方法；C010没有新增更高全域下界。本次不做额外本地科学验证，最终复验交给Actions，尚未观察其结果；原R067的本地接受状态保持。 / This publishes C009's retained complete proof materials for4.66044 and C010's local continuous method; C010 adds no higher global bound. No additional local scientific validation was run; final replay is delegated to Actions and its outcome has not been observed. R067 retains its previous local acceptance status.

[证明与复验 / Proof and replay](../certificates/R068-C010/README.md) · [工作流 / Workflow](../.github/workflows/r068-c010.yml)

> 以下为此前发布内容，状态按各次发布当时解释。 / The following material belongs to earlier publications; status statements refer to those publication dates.

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
