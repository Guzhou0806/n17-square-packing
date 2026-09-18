# M19 发布包：从这里开始

这是可上传 GitHub 的仓库目录，不是需要再补证据的旧版模板。
范围是 **M19 + M12 依赖 + M17 失败记录**；不把 M20 或其他未打包阶段混入本次结论。
英文首页是 `README.md`，给 Joshua 阅读的正文是 `docs/M19_PROOF_EN.md`。

## 1. 解压和检查

建议解压到较短路径，例如 `C:\N17-public`，避免 Windows 深层目录问题。
进入含有 `README.md` 和 `verify.py` 的目录，而不是停留在它的父目录。
保留 `.github`、`.gitattributes`、`.gitignore` 这些点开头的文件/目录。

在 PowerShell 中依次运行：

```powershell
python -X utf8 -B verify.py --quick --output .replay-runs/quick-001
python -X utf8 -B verify.py --output .replay-runs/full-001
python -X utf8 -B -S -m unittest discover -s tests -v
```

若你的 Python 命令是 `py`，把命令开头的 `python` 换成 `py`。
默认复验只需 Python 标准库，不用 API Key、模型、优化器或原项目环境。
二次运行请换新的输出目录名；脚本不会覆盖已有结果。
不要加 `-O` 或 `-OO`，也不要启用 `PYTHONOPTIMIZE`。

完整命令应该输出 `PASS_FULL_REPLAY`。它重算 181 个旧方向和 17 个 M17 新方向：
16 个新方向通过、1 个预期失败，因此 M19 采用的是 197 节点，而不是 198。
`--quick` 不做全域覆盖计算，只会输出 `PASS_QUICK_CHECK_ONLY`。

可选的 NumPy 第二实现说明见 `docs/REPRODUCIBILITY.md`。
实际在打包环境执行了什么，请看 `verification/PACKAGING_REPORT.md`，不要把历史
验收文件误认成刚运行的结果，也不要把复演当成新写一套数学证明。

## 2. 作为新仓库上传

以下命令只用于这个**新解压的发布目录**。若已有同名 GitHub 仓库或已有 `.git`，
先检查现有历史，不要直接覆盖科研目录、删除仓库、强制推送或重复初始化。

```powershell
gh auth status
git init -b main
git add .
git status --short
git diff --cached --stat
```

确认只包含本发布包内容后：

```powershell
git commit -m "Publish M19 evidence with full M12 dependency and replay"
gh repo create n17-square-packing --private --source=. --remote=origin --push
```

这里默认创建 **Private**。要先私信 Joshua，可以先分享证据包；私有仓库链接本身
不会自动给他访问权限。准备公开且确定没有敏感内容时，可在创建命令中将
`--private` 换成 `--public`，或之后在 GitHub 设置中自行改变可见性。
两种创建命令不要重复执行。

若选择网页上传，请上传**解压后的目录内容**，不要只上传一个 ZIP 就结束；否则首页
和可浏览源码不能按设计呈现。官方网页对单次上传文件数量有限制，完整目录建议走 Git。
原始 ZIP 已另放在 `archives/` 供查验，无需你额外加一次。

`.gitattributes` 禁止自动换行转换，以保留证据哈希。不要对 `evidence/` 下的 JSON
重新排版、改状态或保存成其他编码。证书中的旧生产状态和后来的最终验收同时保留是有意设计。

## 3. 发布前的表述

本结果是 `s(17) >= S19`，其中
`4.59004266897263595052 <= S19 < 4.59004266897263595053`。
小数夹住的是**下界常数 S19**，不是 s(17) 本身。

不要写“s(17) 等于这个值”、端点不可装填、已证明最优或世界纪录。
本次不建立外部优先权。贡献与继承关系见 `NOTICE.md`，它保留原始 MIT/CC BY 4.0
许可边界，不对所有文件一键重授权。

仓库名、公开状态和署名由你确认。`CITATION.cff` 使用你的 GitHub 名称，未编造真名、
机构、DOI 或远端地址。导出包版本号 `0.1.0-m19` 不代表已经在 GitHub 创建 Release。

## 4. 给 Joshua 的入口

发送 `communication/X_DM_EN.txt` 中的私信，并附仓库或证据包。
建议他先读英文首页和 `docs/M19_PROOF_EN.md`，再执行完整复验命令。
任何新版本的证据应追加，不要覆盖旧的 M19 证书和 M17 失败记录。

## 5. 与旧发布模板的区别

本版已包含上一轮缺少的原子数据、覆盖算法、181+17 行记录、原始审查和最终验收。
旧模板里“还未收到完整证据”的说明已被本版的明确复验记录取代；原证据文件本身未更改。
如果已上传旧模板，先在本地独立目录检查本包，再以一次清楚的提交更新展示层；不要
直接覆盖旧历史或改写旧提交。T0 的操作任务见 `docs/T0_PUBLISH_HANDOFF.md`。

官方操作参考：
- https://cli.github.com/manual/gh_repo_create
- https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- https://git-scm.com/docs/gitattributes
