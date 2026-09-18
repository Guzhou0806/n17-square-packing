# M12 最小归档许可提醒

正式归档至少保留：

1. `jlevy/squares` 根 `LICENSE` 的锁定快照，commit `035d84c655b4047bc9986c9a3db5106780d92f77`；本轮保存副本 SHA-256 `7428341239cf4ee78c4b951b7fd8a2284b24835aeb0ede82f032b2e95e92cc00`。
2. 按根文件分类：仓库代码为 MIT；文档、研究记录、数据和图形为 CC BY 4.0。`packing/resources/` 的第三方归档不在该根授权内，不随包再许可。
3. 署名建议：`Joshua Levy, the squares project (https://github.com/jlevy/squares)`，并注明锁定 commit。
4. 对 `certificate.json`、scaled derivative 和证明包同时记录：原文件路径/哈希、变换 `λ=1000001/1000000`、哪些字段改变、哪些权重/方向保持不变，以及本项目生成文件的作者与日期。数据衍生包按上游适用的 CC BY 4.0 条件保留署名最稳妥；verifier 源码继续保留 MIT 声明。
5. 不把根许可外推给任何 `packing/resources/` 材料；若最终包没有分发这些第三方字节，也明确写“未再分发第三方归档”。

建议归档说明最小句：

> The source certificate and verifier were derived from Joshua Levy's `squares` project at commit `035d84c655b4047bc9986c9a3db5106780d92f77`. Code is retained under the MIT terms stated in the repository root license; documentation and project data are attributed under CC BY 4.0. No material from `packing/resources/` is relicensed or redistributed here.

许可提醒不是法律意见；若公开发布完整数据包，应由维护者再次核对根许可对具体 JSON 的分类和拟发布文件清单。
