# 复验与边界 / Replay and scope

在本目录运行，依赖C++17、Boost头文件和Node.js22。数学验证不使用Python。所有输出目录必须为新路径。 / Run from this directory with C++17, Boost headers and Node.js22. Mathematical verification uses no Python. Every output directory must be new.

```sh
node check_package.js
node run_public.js geometry .recheck-geometry
node run_public.js bound .recheck-bound
```

geometry重新编译7个C++程序，执行C028的4对前提任务、C029的20对新增任务及两轮的数学破坏/有效替代控制，并逐字节比较所有确定性结果。C028的有限对偶输入仅用于原程序诊断，不将该输入的完整旧LP证明认作本包新验结论。 / geometry recompiles7 C++ programs and executes4 paired C028 prerequisite tasks,20 paired C029 new tasks, and both rounds' mathematical mutation/valid-alternative controls, comparing all deterministic results byte for byte. C028's finite-dual input is used only by the original diagnostic; its full historical LP proof is not newly certified by this package.

bound重新编译原C++全域验证器并用独立BigInt重算C027全部5114角区间，生成新分区记录及THEOREM.json，最后核对目标、最低费和严格余量。没有把validate-only当全扫。 / bound recompiles the original C++ global verifier and independently replays all5114 C027 angular intervals with BigInt, generating fresh partitions and THEOREM.json and checking target, minimum charge and strict surplus. A validate-only run is not treated as a full sweep.

公开启动器为选定科学子集重新编写；源码、输入和冻结数学输出不变，SOURCE_MAP.json绑定回包身份。旧的全包CHECK/RUN和研究提示词不在本公开子集中。`node run_public.js geometry --plan-only`只检验计划和依赖，不执行数学。 / The public launcher is new packaging for the selected scientific subset; source, inputs and frozen mathematical outputs are unchanged, with SOURCE_MAP.json binding their returned identities. Old whole-archive CHECK/RUN scripts and research prompts are excluded. `node run_public.js geometry --plan-only` checks only the plan and dependencies, not mathematics.

GitHub Actions分别执行bound和geometry，失败/超时不算通过；输出作为artifact保存。接收方未重跑几何，未查看、轮询或等待Action jobs。机器双实现一致仍不等于形式化或独立人类同行评审。 / GitHub Actions executes bound and geometry separately; failures/timeouts are not passes, and outputs are saved as artifacts. Reception did not recompute geometry or inspect, poll or wait for Action jobs. Agreement between two implementations is not formalization or independent human peer review.

完整C029累计包留本地；历史C020有276缺项、C027完整旧ZIP/分区仍缺失，均未伪称恢复。C029文档引用的包外封存重放审计未随本次附件收到，因此不借用其通过状态。新复验可验证本包选定命题，不能找回缺失历史。 / The complete cumulative C029 return is retained locally. The276 historical C020 omissions and the missing full C027 archive/partitions are not claimed recovered. The external sealed-archive replay audit referenced by C029 documents was not received with this attachment, so its success is not assumed. Fresh replay can verify the selected claims but cannot recover missing history.
