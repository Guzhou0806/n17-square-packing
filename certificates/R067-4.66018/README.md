# R067：十七单位正方形的严格下界4.66018 / R067: strict lower bound 4.66018 for seventeen unit squares

本证书证明17个任意旋转、内部两两不交且允许边界接触的单位正方形满足以下严格下界。 / This certificate proves the following strict lower bound for seventeen arbitrarily rotated unit squares with pairwise disjoint interiors and permitted boundary contact.

$$s(17)>233009/50000=4.66018.$$

这是Kleddamag公开4.66001的延续：保持其站点、规则、整数权重和总预算不变，重建严格核与2808个角区间。新增端点由Guzhou0806 / N17 project在AI辅助下完成；原收费和基线仍归Kleddamag。 / This continues Kleddamag's public 4.66001 result, retaining its sites, rules, integer weights and budget while reconstructing strict cores and 2808 angular intervals. Guzhou0806 / N17 project with AI assistance produced the new endpoint; the charge and baseline remain attributed to Kleddamag.

$$M=17000402008,\qquad\Gamma=1000026844,\qquad17\Gamma-M=54340>0.$$

完整C++与独立BigInt运行记录逐行一致。接收验收复用了这些完整记录和未改验证器，重新检查全部前提及4个区间，没有再次进行本地完整扫描。 / Complete C++ and independent BigInt run records agree row by row. Non-proposer acceptance reused these complete records and unchanged checkers, freshly checked every premise and four intervals, and did not repeat the full local sweep.

[证明 / Proof](PROOF.md) · [复验 / Reproduction](REPRODUCIBILITY.md) · [来源和许可 / Sources and licensing](ATTRIBUTION.md) · [接受范围 / Acceptance scope](evidence/ACCEPTANCE.json)

```sh
node check_records.js
g++ -O3 -std=c++17 src/verify.cpp -o verify
./verify certificate.json fresh-cpp.json
node src/replay.js certificate.json fresh-paired-run ./verify 2
```

从本目录运行；需要C++17、Boost开发头文件和Node.js，证明复验不需要Python。输出文件或目录须为新的。 / Run from this directory with C++17, Boost development headers and Node.js; proof replay does not require Python. Output files or directories must be new.

只发布已完成的4.66018证明；4.6605探索失败，不是下界。未声明世界纪录、最优性、外部人类同行评审或证明助手形式化。 / Only the completed 4.66018 proof is published; the unsuccessful 4.6605 exploration is not a lower bound. No world-record, optimality, external human peer-review or proof-assistant formalization claim is made.
