# M12 Python 3.12 compatibility addendum

原冻结 harness 的 source 模式在进入第一个方向前失败：锁定 `certificate.py::_worker_count` 调用 Python 3.13 新增的 `os.process_cpu_count()`，本机 Python 3.12.13 不含该属性。没有 direction minimum 或结果文件产生；scaled 未运行。

T0 明确授权唯一兼容 wrapper `run_replay_py312_compat.py`：

- 仅当 `os.process_cpu_count` 缺失时设置 `os.process_cpu_count=os.cpu_count`；若属性已存在则 wrapper 拒绝运行。
- 不修改锁定源码、JSON、NumPy 或 frozen `run_replay.py`。
- source 调用仍显式 `workers=1`。`_worker_count` 只把 available cores、requested workers、direction count、固定 cap 和 memory cap 取最小；其中 requested 已为 1，因此 compatibility API 的具体正整数返回值不会改变结果，最终必为单工。
- 该 API 不被 `model.py`、`sweep.py` 的方向、Fraction 几何、整数权重或 event-grid 运算引用。
- 若之后出现任何第二种版本不兼容，停止，不增加 shim。

此 addendum 取代 `PROTOCOL.md` 中“版本失败即结束”的单一条款，其余输入、两次运行、预算和拒绝条件不变。首次失败作为环境证据保留，不冒充 verifier 失败。
