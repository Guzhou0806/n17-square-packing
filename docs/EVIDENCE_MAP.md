# Evidence map / 证据入口

## R012

`certificates/R012/orbits.json` + `catalogue.json` define the exact mathematical object. `verify.py` checks identity, full interval assembly, geometry, coverage and the bound. `sweep.py` enumerates all continuous center cells. `counterexamples.json` contains five scientific negative controls. `PROOF.md` connects the computations to the packing statement. `MANIFEST.json` binds only this scientific package.

整数轨道与目录定义数学对象；验证入口和有理扫描承担全部检查；五个失败见证防止误把原配方宣称成功；证明说明将计算连接至全局下界。科学清单不依赖协调或授权文件。

The public implementation path differs from the original mixed Python/C++ replay, but the exact atoms and catalogue geometry are unchanged. No original C++ source is required or redistributed.

## M19

[Proof / 证明](M19_PROOF_EN.md), [original package / 原包](../evidence/M19/README.md), [machine certificate / 机器证书](../evidence/M19/research/m19_work/CERTIFICATE.json), [acceptance record / 验收记录](../evidence/M19/FINAL_ACCEPTANCE.json).

The historical package is unchanged; its producer statuses and later acceptance have not been rewritten. The root `EVIDENCE_MANIFEST.json` continues to bind M19's frozen inputs. R012 has a separate scientific manifest and never inherits M19's PASS.

M19 原科学包保持不变，旧生产状态与后续验收不重写。R012 使用独立清单，不能继承 M19 的 PASS 作为新覆盖证明。
