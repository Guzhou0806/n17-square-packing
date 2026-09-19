# Sources and transformations / 来源与变换

Research result: **Guzhou0806 / N17 project, with AI assistance**. R012 denotes this specific parent-angle certificate; it does not imply endorsement or coauthorship by upstream authors.

研究成果署名为 Guzhou0806 / N17 project，使用了 AI 辅助。R012 是该具体证书的标识，不暗示上游作者背书或共同署名。

## Mathematical antecedents / 数学继承

- **Mira**, [17squares, pinned commit](https://github.com/Mira-acc/17squares/tree/0266c9936a303817ac7da0802364034a34fb2558), especially [the weighted proof](https://github.com/Mira-acc/17squares/blob/0266c9936a303817ac7da0802364034a34fb2558/certificates/lower_bound_4p613/PROOF.md) and [exact result](https://github.com/Mira-acc/17squares/blob/0266c9936a303817ac7da0802364034a34fb2558/certificates/lower_bound_4p613/result.json): spatial support, weighted certificate and comparison endpoint. / 空间支撑、加权证书与对照端点。
- **Joshua Levy, the squares project**, [pinned commit](https://github.com/jlevy/squares/tree/fb14f5174fdf675b296b442c98b7127fccc8a84d): weighted covering, exact event sweeps, interior-core counting and dilation. The [parent-center contract](https://github.com/jlevy/squares/blob/fb14f5174fdf675b296b442c98b7127fccc8a84d/packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md) is prior work for parent-aware domains, not an imported N17 certificate. / 父中心限制有已有先例，其 N11 数值没有被移植为本命题。

The atomic geometry was rounded to 10^-5 coordinates and the weights rounded upward to 10^-6 before R012; coincident points were aggregated and coverage rechecked. The present export only re-encodes that fixed mathematical result as 206 integer D4 rows. Its sorted expanded atom table has canonical SHA-256 `ae469399ced8580ddddcef6edc234cf9becd7e94df7752aa8b4f9cefcbaf3643` (JSON arrays of rational strings, no spaces). The source R012 expanded input file had SHA-256 `81b3050ec6a964d4cc1eb09fa7aafadf0e478869a710f2dbc54b26d34e5c96ba`.

本公开版只是将 R012 已固定的原子表转换为整数轨道编码。此前坐标量化、权重上取整及碰撞聚合的结果保持不变；复验重建后检查规范化原子摘要，而不是信任舍入误差很小的假设。

## Code and rights / 代码与权利边界

`sweep.py` is retained byte-for-byte from the project's rational center-domain checker, adapted from its M12 event-cell lineage. SHA-256: `96efe91895ab14d80c6b7162aee91d4687e5d11a60093a9935043a88d4713965`. The earlier source code lineage is Joshua Levy's MIT-licensed code; its notice is retained in [LICENSE-MIT.txt](LICENSE-MIT.txt). `verify.py` and the public tests are publication adapters.

`sweep.py` 沿用本项目 M12 有理事件扫描路线，原文件逐字节保留。Joshua 来源代码的 MIT 声明一并保存。新入口和测试属于公开复验适配，不是原来源 C++ 的改名副本。

**No Mira C++ source, adapted C++ source, third-party source archive or internal workflow material is redistributed here.** Their public redistribution terms were not established by this export. Numerical certificate data and new explanatory text are accompanied by attribution; this file grants no blanket rights over third-party material. Existing CC BY 4.0 notices for Levy-origin non-code material remain applicable to that material; see the [upstream licensing scope](https://github.com/jlevy/squares/blob/fb14f5174fdf675b296b442c98b7127fccc8a84d/LICENSE).

本目录不再分发 Mira 的 C++、其改编版、第三方归档或内部工作材料；也不把 Joshua 的 MIT 自动延伸到其他作者的代码。数值证书和新增解释保留来源，不对第三方材料作整体再许可。

## Assurance / 可信程度

The complete public replay computes all 2925 parent-envelope obligations in Python rather than copying the original mixed-language PASS logs. This changes the implementation path, not the theorem, measure or selector. It is not independent external peer review, formal verification or an exhaustive priority search.

公开入口直接用 Python 重算 2925 项父中心域义务，不借用原混合语言日志充当新执行。实现路径改变，数学对象未改变；这不等于外部审稿、形式化验证或穷尽首发检索。
