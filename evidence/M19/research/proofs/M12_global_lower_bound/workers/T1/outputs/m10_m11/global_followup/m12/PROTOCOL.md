# M12 source-faithful fixed replay protocol

状态：计算前冻结，2026-09-17。

## 目标与非目标

按 commit `035d84c655b4047bc9986c9a3db5106780d92f77` 的 source verifier，单工重放：

1. 原 T-019 `certificate.json` 的 181 个方向；
2. 固定 `λ=1000001/1000000` 后的 scaled certificate 的同 181 个方向。

无优化、无 λ 搜索、无参数调整、无失败后重试。结果独立于 T0 的新 range-add/min sweep；本任务不读取其实现。

## 锁定输入

- certificate 原字节 SHA-256：`461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652`。
- source commit：`035d84c655b4047bc9986c9a3db5106780d92f77`。
- `certificate.py` SHA-256：`174ae7c3f6081684afd2cbaa6459211bf05971755df753359064a540a84ab1ba`。
- 其余 closure 的下载字节/哈希以 `NETWORK_LOG.jsonl` 为准；共 8 个新请求，远低于 10 MB。
- 许可沿用已锁根文件：代码 MIT；本地保存原字节仅用于验证。

## 静态副作用审查

直接 closure：`certificate.py -> model.py, sweep.py, workers.py`；`sweep.py -> numpy`。检查到：

- 无网络、subprocess、文件写入、删除或动态下载调用；
- `certificate.py` 含 multiprocessing，但 `workers=1` 路径不建立进程池；
- 计算只分配内存并读取输入；输出由本地 harness 写入 `results/`；
- source 根 `sqpack/__init__.py` 会导入与本任务无关、未下载的 `field`/`verify`。harness 以 namespace package 注入绕过该聚合入口，但不修改 `fractional` 三个模块正文；这是显式环境适配，不改变 verifier 算法。

## 环境

- Python：工作区现有 LibreOffice Python `3.12.13`。
- NumPy：工作区 `.deps/m2/site-packages` 中 `2.5.3`。
- 锁定 `pyproject.toml` 声明 Python `>=3.14,<3.15`，故本次 Python 版本是明确偏差；若代码导入或语义失败，停止，不安装/调源码。成功结果仍须在报告中披露此偏差。
- `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`，verifier `workers=1`。

## 单次运行语义

本地 harness 精确复刻 `replay.py` 的 JSON→`Certificate` 构造。为同时得到 source `verify()` verdict 和逐方向数据，它临时包装模块全局 `sweep_all_directions`：包装器只调用原函数一次、原样返回不可变 tuple，并保存该 tuple 到输出；不改任何 minimum、顺序或条件。随后调用原 `verify(certificate, workers=1)`。

source 模式使用原对象。scaled 模式只作：

- `outer_side`, `square_side`, 每个 atom 的 x/y 乘 λ；
- n、label、weight、half_tangents、D4 不变。

每个模式独立进程恰好一次，先 source 后 scaled。输出：逐方向 exact minima、五个 condition、worst direction/mass、总质量、输入/源码哈希、Python/NumPy、wall/CPU/PeakWorkingSet。scaled 模式另存 canonical JSON。

## 验收

source：

- `accepted=true`；方向数 181；total `423327/25000`；worst `200009/200000`；声明字段一致。

scaled：

- `accepted=true`；方向数 181；`outer_side=459000459/100000000`；粗 Condition 4 通过；total 与 source 相同；逐方向 minima tuple 与 source 完全一致。

两个结果哈希绑定。任何异常、超 15 分钟总执行、输出趋近 200 MB、或上述比较失败：保存输出并停止，不调 λ、workers、算法或数据。

## 运行命令

分别执行：

`python run_replay.py source`

`python run_replay.py scaled`

命令由 shell 设置 NumPy 路径和三个线程环境变量。不会执行仓库 CLI、测试或其他第三方入口。

