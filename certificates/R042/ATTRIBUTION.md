# Sources and attribution / 来源与署名

R042 is published by **Guzhou0806 / N17 project, with AI assistance**, and builds on the explicitly pinned Kleddamag v1.0.0 mixed-certificate architecture. / R042 由 **Guzhou0806 / N17 project（使用 AI 辅助）** 发布，并建立在明确锁定的 Kleddamag v1.0.0 混合证书架构之上。

The primary upstream implementation source is **Kleddamag/17-squares-certified-bound**, release `v1.0.0`, commit `a499e2c739ce7853fa04c8bcdc85caf1c2b01b37`, whose frozen baseline certificate has SHA-256 `0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec`. / 主要上游实现来源为 **Kleddamag/17-squares-certified-bound** 的 `v1.0.0` 发布版与提交 `a499e2c739ce7853fa04c8bcdc85caf1c2b01b37`，其冻结基线证书 SHA-256 为 `0288aaac680131aa675adb63ea6a67e3d363fcca6061d4c788301da7c5d69cec`。

Kleddamag's repository credits the earlier R038 parent-side checker from this repository and the upstream weighted-covering lineage documented there. / Kleddamag 仓库对本仓库更早的 R038 父边长检查器及其文档中记录的上游加权覆盖路线进行了来源说明。

R042 contributes the parent side `24963/25000`, the retargeted 7,853-row core catalogue, the threshold-orbit-22 weight change, the resulting frozen certificate, independent rational containment checks, and two completed exact full replays. / R042 的增量包括父边长 `24963/25000`、重新定向的 7,853 行内核目录、阈值轨道 22 的权重变化、由此得到的冻结证书、独立有理包含检查以及两次已完成的精确全量复演。

The public Python sweep sources retained here are Kled-derived MIT-licensed files, with the upstream license reproduced in [KLED_MIT_LICENSE.zh-en.md](KLED_MIT_LICENSE.zh-en.md). / 本目录保留的公开 Python 扫描源码是源自 Kled、按 MIT 许可发布的文件，上游许可完整保留于 [KLED_MIT_LICENSE.zh-en.md](KLED_MIT_LICENSE.zh-en.md)。

The secondary BigInt checker is not redistributed; it is reconstructed at replay time from R038 commit `32edfd3da78bf80a309398f552b3b602b9c45d6c`, source SHA-256 `63e858e28c4dee40f5763a832e1cfdf1f1fce3a1e5c632d087525bf1ee20ed14`, and the pinned adaptation recipe. / 第二套 BigInt 检查器不被重新分发；复演时会从 R038 提交 `32edfd3da78bf80a309398f552b3b602b9c45d6c`、源文件 SHA-256 `63e858e28c4dee40f5763a832e1cfdf1f1fce3a1e5c632d087525bf1ee20ed14` 与锁定适配配方现场重建。

The reconstructed checker must have SHA-256 `b145b1ebbb2d3a0dccba62ee7b5ed64403bf0542ce5e8ee87113977df917faa4` before it is executed. / 重建后的检查器只有在 SHA-256 为 `b145b1ebbb2d3a0dccba62ee7b5ed64403bf0542ce5e8ee87113977df917faa4` 时才会被执行。

No upstream endorsement, coauthorship, external review, general-method priority, or global optimality is implied by this attribution. / 此署名不暗示上游作者背书、共同署名、外部审查、通用方法首创或全局最优。
