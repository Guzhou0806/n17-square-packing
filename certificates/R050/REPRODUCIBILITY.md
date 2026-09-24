# R050 复验 / R050 reproduction

以下命令从本目录执行；输出目录必须尚不存在。记录核查与包含检查仅需 Python 标准库；完整 Python 扫描还需 NumPy 和 Numba。 / Run the following commands from this directory; the output directory must not already exist. Recorded-evidence and containment checks use only the Python standard library; the full Python scan additionally requires NumPy and Numba.

## 记录与完整性核查 / Recorded-evidence and integrity checks

```bash
python -X utf8 -B -S verify.py --output .replay-runs/records-001
```

默认入口核对显式清单、证书身份、预算、完整 Python 保存账本、118 个 BigInt 分块的连续覆盖与逐块完整直方图；它不会重新计算全部中心。 / The default entry checks the explicit manifest, certificate identity, budget, complete saved Python ledger, and contiguous coverage and full histograms of all 118 BigInt blocks; it does not recompute every centre.

## 独立包含复算 / Independent containment recomputation

```bash
python -X utf8 -B -S verify.py --containment --output .replay-runs/containment-001
```

此命令重新计算全部 62824 条有理严格包含不等式，并检查角目录和相关中心域前提。 / This command recomputes all 62824 rational strict-containment inequalities and checks the angular catalogue and relevant centre-domain premises.

## 完整 Python 复演 / Full Python replay

```bash
python -m pip install -r requirements-full.txt
python -X utf8 -B verify.py --python-full --jobs 8 --output .replay-runs/python-001
```

此命令使用包内冻结的 Python 实现重新扫描全部 15706 行。首次研究验收在 Python 3.12.14、NumPy 2.5.3、Numba 0.67.0 下以八个工作进程用时 462.657 秒；该用时不承诺其他机器性能。 / This command rescans all 15706 rows using the package's frozen Python implementation. The initial research acceptance used Python 3.12.14, NumPy 2.5.3 and Numba 0.67.0 with eight workers and took 462.657 seconds; that timing is not a performance promise for other machines.

## 完整 BigInt 复演 / Full BigInt replay

```bash
python -X utf8 -B -S verify.py --bigint-full --jobs 8 --output .replay-runs/bigint-001
```

需要 Node.js。该入口从固定公开提交下载 SHA-256 锁定的原源，并应用随包确定性编辑配方；重建检查器再次核哈希后扫描全部 15706 行。首次重建需要网络，Python 和记录/包含检查不需要网络。 / Node.js is required. This entry downloads SHA-256-pinned source from a fixed public commit and applies the bundled deterministic edit recipe; after its hash is checked, the reconstructed checker scans all 15706 rows. Initial reconstruction requires network access; Python and recorded-evidence/containment checks do not.

派生 BigInt 检查器字节不随发布分发；来源与适用许可仍然保留。 / The derived BigInt checker bytes are not redistributed with this release; provenance and applicable licence boundaries remain in force.

## 判断成功 / Interpreting success

完整复验必须绑定原证书身份、15706 行完整覆盖、最低收费 1000271689、预算 17003093868、完整最低值直方图、零逃逸，以及正计数余量 1524845。仅命令退出或记录哈希一致不能替代完整数学验证。 / A full replay must bind the original certificate identity, all 15706 rows, minimum charge 1000271689, budget 17003093868, the complete minimum-charge histogram, zero escapes, and positive surplus 1524845. A command exit or matching recorded hashes alone does not replace complete mathematical verification.

使用正常 Python 执行模式，不得启用 -O、-OO 或 PYTHONOPTIMIZE，因为冻结程序包含必要断言。 / Use normal Python execution without -O, -OO or PYTHONOPTIMIZE because the frozen programs contain essential assertions.

发布前隔离复验的真实结果另记于公开验证记录；隔离计算使用复制后的自足包，不依赖原研究工作区。 / Actual isolated pre-publication replay results are recorded separately in the public validation record; isolated computation uses a copied self-contained package without relying on the original research workspace.
