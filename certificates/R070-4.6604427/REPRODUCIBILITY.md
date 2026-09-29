# C++与BigInt复验 / C++ and BigInt replay

从本目录执行。需要C++17、Boost头文件、Node.js22；科学验证不调用Python。所有输出须为新路径。 / Run from this directory with C++17, Boost headers and Node.js22; scientific replay uses no Python. All output paths must be fresh.

## 新完整目标 / New complete target

```sh
node check_package.js
mkdir -p .recheck/bin
g++ -O3 -std=c++17 project/base/upstream/cpp/verify.cpp -o .recheck/bin/verify
node project/base/upstream/cpp/replay.js project/followup_c016/results/target_4.6604427/certificate.json .recheck/global .recheck/bin/verify 2
node assert_results.js global
```

## 319规则及增强类障碍 / 319 rules and enhancement-class obstruction

```sh
node check_package.js
mkdir -p .recheck/bin
g++ -O3 -std=c++17 project/followup_c016/src/geometric_rules.cpp -o .recheck/bin/geometry
g++ -O3 -std=c++17 project/followup_c016/src/parent_hull_obstruction.cpp -o .recheck/bin/barrier
.recheck/bin/geometry project/followup_c015/data/lifted_accepted_model.json project/followup_c016/data/geometric_overlay_all.json .recheck/all-cpp.json
node project/followup_c016/src/verify_geometric_rules.js project/followup_c015/data/lifted_accepted_model.json project/followup_c016/data/geometric_overlay_all.json .recheck/all-cpp.json .recheck/all-bigint.json
.recheck/bin/barrier project/followup_c015/data/lifted_accepted_model.json project/followup_c015/results/angular_cell/short_pose.json 186417711/40000000 .recheck/barrier-cpp.json
node project/followup_c016/src/verify_parent_hull_obstruction.js project/followup_c015/data/lifted_accepted_model.json project/followup_c015/results/angular_cell/short_pose.json .recheck/barrier-cpp.json .recheck/barrier-bigint.json
node assert_results.js geometry
```

上述两组由GitHub Actions分别执行并上传新生成记录；失败/超时不是通过。此次接收只做原文件身份与5107配对行一致性检查，没有运行上述几何复验，也不观察CI结果。 / GitHub Actions runs these two groups separately and uploads fresh records; failures/timeouts are not passes. Reception only checked original file identities and5107 paired rows, without running the geometry replay above or observing CI outcomes.
