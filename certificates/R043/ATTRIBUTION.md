# Sources and attribution / 来源与署名

R043 is published by the N17 project with AI assistance and directly continues the frozen R042 mixed-certificate architecture. / R043 由 N17 project 在 AI 辅助下发布，并直接延续冻结的 R042 mixed-certificate 架构。

The primary upstream architecture is Kleddamag `17-squares-certified-bound` v1.0.0 at commit `a499e2c739ce7853fa04c8bcdc85caf1c2b01b37`. / 主要上游架构来自 Kleddamag `17-squares-certified-bound` v1.0.0，锁定提交为 `a499e2c739ce7853fa04c8bcdc85caf1c2b01b37`。

The R043 certificate introduces no new third-party point or threshold coordinates; its numerical change is confined to the smaller parent side, retargeted core sides, and nonnegative weights on four existing zero-weight point orbits. / R043 证书不引入新的第三方 point 或 threshold 坐标；其数值变化仅包括更小的父边长、重新定向的 core side，以及四个既有零权 point orbit 上的非负权重。

The source-distinct BigInt checker is deterministically reconstructed from `certificates/R038/src/exact_parent_side_scan.js` at public commit `32edfd3da78bf80a309398f552b3b602b9c45d6c`, SHA-256 `63e858e28c4dee40f5763a832e1cfdf1f1fce3a1e5c632d087525bf1ee20ed14`, plus `src/secondary-adaptation.json`. / 不同源码的 BigInt 检查器从公开提交 `32edfd3da78bf80a309398f552b3b602b9c45d6c` 中的 `certificates/R038/src/exact_parent_side_scan.js` 确定性重建，该来源文件 SHA-256 为 `63e858e28c4dee40f5763a832e1cfdf1f1fce3a1e5c632d087525bf1ee20ed14`，并应用 `src/secondary-adaptation.json`。

The reconstructed checker bytes are intentionally not redistributed. / 重建后的检查器字节被有意排除，不进行重新分发。

This attribution does not imply upstream endorsement, coauthorship, independent external review, global optimality, or established public priority. / 此署名不暗示上游作者背书、共同署名、独立外部审查、全局最优或已确认的公开首发。
