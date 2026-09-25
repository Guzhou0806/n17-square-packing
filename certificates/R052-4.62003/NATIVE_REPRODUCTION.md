# C++ 精确全量复验 / Exact full C++ replay

此入口在包外自动编译C++源码并重新计算全部15727行，与独立BigInt账本逐行比较；它同时运行完整资源、预算、角度和严格包含检查。 / This entry builds the C++ source outside the package and recomputes all 15727 rows against the independent BigInt ledger, also checking resources, budgets, angles and strict containment.

需要Python 3.10或更新版本、支持C++17的g++及Boost头文件；此入口只使用Python标准库，不需要NumPy或Numba。已测试的本地环境为Windows MinGW64，Linux构建由本版本GitHub CI核验。 / It requires Python 3.10 or newer, a C++17-capable g++ and Boost headers; the entry uses only the Python standard library and needs neither NumPy nor Numba. The local tested environment is Windows MinGW64; Linux builds are checked by this version's GitHub CI.

```bash
# Linux dependencies / Linux 依赖
sudo apt-get update
sudo apt-get install g++ libboost-dev
# Run from the repository root / 从仓库根目录运行
python -X utf8 -B -S certificates/R052-4.62003/verify_native.py --jobs 4 --output .replay-runs/r052-continuation-native
```

Windows在PATH中提供64位MinGW g++和Boost头文件后可使用同一命令；也可用--compiler指定编译器，用--boost-include指定包含boost目录的父目录。 / On Windows, the same command works with 64-bit MinGW g++ and Boost headers on the search path; use --compiler for the compiler and --boost-include for the parent directory containing boost.

输出目录必须尚不存在且位于包外。编译记录、库、INPUT.json、ROWS.json和RESULT.json均写入该目录；任何编译、身份或逐行比较失败都不能产生成功RESULT。 / The output directory must be new and outside the package. Build logs, the library, INPUT.json, ROWS.json and RESULT.json are written there; a compilation, identity or row-comparison failure cannot produce a successful RESULT.

几何运算使用Boost任意精度整数，512位仅是内联存储容量，上限仍可扩展；收费树使用有严格绝对系数质量界的int64整数，不使用浮点几何近似。 / Geometry uses Boost arbitrary-precision integers: 512 bits is only inline storage, with an unbounded maximum. The charge tree uses int64 integers guarded by a strict absolute coefficient-mass bound, without floating-point geometric approximations.

C++源码与已验收的加速内核原字节一致；Python适配器只替换独立导入，五个几何函数原样提取。源码身份记录在SOURCE_PIN.json，编译器版本、源码与新生成库的哈希记入每次INPUT.json。 / The C++ source is byte-identical to the accepted acceleration kernel; its Python adapter only changes the standalone import, and five geometry functions are extracted unchanged. SOURCE_PIN.json pins sources, while each INPUT.json records the compiler version and source and freshly built library hashes.

C++与Python共享几何构造来源，不能把它们当作完全独立的两份证明；Node/BigInt保留为源码不同的完整复验。Python全扫入口作为参考实现仍可使用。 / C++ and Python share geometric construction lineage and are not two fully independent proofs; Node/BigInt remains the source-distinct full replay. The Python full entry remains available as a reference implementation.

本包仅分发源码，不分发预编译DLL、SO、编译器或Boost头文件；这些外部依赖保留各自许可。既有约3.75倍加速是同机同输入的有界配对实测，不保证每台机器或完整发布流程均取得相同比例。 / This package distributes source only, not prebuilt DLLs, SOs, compilers or Boost headers; external dependencies retain their licences. The earlier approximately3.75-times speedup is a bounded same-machine, same-input measurement, not a promise for every machine or the entire publication process.
