# 首次冻结运行失败记录

模式：`source`  
结果：退出码 1；0 个方向完成；未生成 `source_result.json`；scaled 未启动。

异常链：

`run_replay.py -> certificate.verify -> sweep_all_directions -> _worker_count -> os.process_cpu_count()`

Python 3.12.13 报告：

`AttributeError: module 'os' has no attribute 'process_cpu_count'`

该失败发生在方向列表计算前，只表明锁定项目要求的 Python 3.14 API 与现有 Python 不匹配，不是几何/覆盖 verdict。后续唯一授权兼容措施见 `COMPATIBILITY_ADDENDUM.md`。
