# 复验与证据范围 / Reproduction and evidence scope

记录核对：在本目录运行node check_records.js，检查清单、完整区间覆盖、两实现每行相等及严格预算。它读取已保存结果，不重新求解几何。 / Recorded check: run node check_records.js here to check identities, complete interval coverage, row agreement and strict budget. It reads saved results without recomputing geometry.

新鲜全量C++：g++ -O3 -std=c++17 src/verify.cpp -o verify，然后./verify certificate.json fresh-cpp.json。需C++17及Boost头文件。 / Fresh full C++: g++ -O3 -std=c++17 src/verify.cpp -o verify, followed by ./verify certificate.json fresh-cpp.json. C++17 and Boost headers are required.

完整双实现：node src/replay.js certificate.json fresh-paired-run ./verify 2。两个C++和两个Node进程覆盖全部区间，再逐行比较；完整成功才写THEOREM.json。默认进程超时60分钟，可用N17_TIMEOUT_MINUTES调整。 / Full paired replay: node src/replay.js certificate.json fresh-paired-run ./verify 2. Two C++ and two Node processes cover all intervals and are compared row by row; THEOREM.json is written only on complete success. The default process timeout is 60 minutes, adjustable with N17_TIMEOUT_MINUTES.

Windows将./verify替换为./verify.exe，编译输出改为verify.exe。也可cmake -S src -B build -DCMAKE_BUILD_TYPE=Release后cmake --build build --config Release。 / On Windows replace ./verify with ./verify.exe and compile to verify.exe. Alternatively run cmake -S src -B build -DCMAKE_BUILD_TYPE=Release and cmake --build build --config Release.

前提模式--validate-only不扫描中心，分区模式--range start count不代表完整定理。只有完整覆盖、最低费足够、严格预算及前提全部通过才成立。 / --validate-only does not scan centres, and --range start count does not establish the full theorem. Complete coverage, sufficient minima, strict budget and all premises are required.

原完整运行环境为GCC14.2.0、Boost1.83、Node22.16.0，Linux x86-64；六个分区全部结束，配对用时528.137秒。本地接收用未改动且已审阅的Windows构建重新检查全部前提和区间0、849、1404、2807，其余完整结果复用身份匹配的双实现记录。没有宣称再次全扫或远端CI已通过。 / The original complete run used GCC14.2.0, Boost1.83 and Node22.16.0 on Linux x86-64; all six partitions completed, with paired wall time 528.137 seconds. Local acceptance used an unchanged reviewed Windows build for all premises and intervals 0,849,1404,2807, reusing identity-matched complete paired records for the remainder. No repeated full local sweep or successful remote CI is claimed.

证书及继承代码保持原字节；输入JSON中的构造阶段source文字、历史元数据或旧注释不替代最终收据。当前检查器支持1至12站点的阈值或相交Boolean规则，代表角需满足C≥S≥0；本证书全部满足。 / The certificate and inherited code retain their bytes; construction-stage source text, historical metadata and old comments do not override final receipts. The current checker supports threshold or intersecting Boolean rules on 1..12 sites and representative angles C≥S≥0; this certificate satisfies these conditions.
