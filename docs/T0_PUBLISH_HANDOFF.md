# 给本地 T0：M19 发布导出集成任务

任务只是检查与发布准备，不开启新的 packing 搜索，不重新生成原证书，不使用子代理。
常规文件整理用实际可用的较经济模型；只有证明冲突才升级。是否创建/公开/推送远端
由用户明确决定。本任务书本身不构成公开授权。

1. 在新的发布目录读取 README、NOTICE、EVIDENCE_MAP 和 PACKAGING_REPORT。
2. 完整运行 `python -X utf8 -B verify.py --output .replay-runs/t0-001`。
3. 运行 `python -X utf8 -B -S -m unittest discover -s tests -v`。
4. 不修改 `evidence/` 和 `archives/`。核对旧证书和新验收哈希，保持 M17 失败。
5. 若已有公开仓库，先读取远端与本地状态，用新提交集成；不覆盖 `.git`、不 force-push。
6. 给用户确认上传清单、仓库名、可见性、署名和新增包装材料许可。
7. 得到上传授权后再建仓/推送；不要虚报已上传。

报告应分别说明 quick / full / optional source replay 中实际运行了哪些。
没有执行的不能通过复述旧日志标记为已执行。把本地新输出留在独立目录，并记录哈希。
不要把本次 M19 发布暗中替换为更强但证据不在包内的 M20。
