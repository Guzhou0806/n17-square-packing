# 复验入口 / Reproduction

从本目录运行，需要C++17、Boost头文件和Node.js 22；科学验证不需要Python。输出目录必须全新。本次发布未在本地运行以下命令；Actions负责最终复验，发布者不轮询jobs。 / Run from this directory with C++17, Boost headers and Node.js 22; scientific verification needs no Python. Output directories must be fresh. These commands were not run locally for this publication; Actions performs final replay, and the publisher does not poll jobs.

```sh
node check_package.js
mkdir -p .recheck/bin
g++ -O3 -std=c++17 upstream/cpp/verify.cpp -o .recheck/bin/verify
node upstream/cpp/replay.js accepted/4.66044/certificate.json .recheck/global .recheck/bin/verify 2
```

完整目标期望状态PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION、4991区间、预算17000448944、最低1000026844及余量7404。 / Expected global output is PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION, with 4991 intervals, budget 17000448944, minimum 1000026844 and surplus 7404.

```sh
g++ -O3 -std=c++17 src/strip_sweep.cpp -o .recheck/bin/strip
g++ -O3 -std=c++17 upstream/cpp/probe.cpp -o .recheck/bin/probe
.recheck/bin/strip research/fit02/model.json research/strip/jobs.json .recheck/strip.json .recheck/strip-poses.json 32
node src/verify_strip.js research/fit02/model.json research/strip/jobs.json .recheck/strip.json .recheck/strip-independent.json
.recheck/bin/probe research/fit02/model.json research/fit02/failure_poses.json .recheck/failure-cpp.json 9321/2000
node tools/verify_finite.js research/fit02/model.json research/fit02/failure_spec.json .recheck/failure-bigint.json
```

局部期望17区域最低1000026908；反例期望开费999975439、余量−818592。两者可同时成立，不能据局部正余量推出全域结论。 / Expected local minima are 1000026908 over 17 regions; the counterexample has open charge 999975439 and surplus −818592. These statements coexist, and local positive surplus does not imply a global conclusion.

工作流在完整与局部两个独立job中执行上述命令并检查目标输出，再上传新生成记录。失败或超时表示未完成验收；历史PASS文件不会代替本次新输出。 / The workflow runs these commands in separate global and local jobs, checks expected outputs and uploads fresh records. Failure or timeout leaves acceptance incomplete; historical PASS files do not substitute for new outputs.
