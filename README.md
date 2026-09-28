# R068 / C010：提交最终CI复验 / Submitted for final CI replay

公开C009保留的4.66044完整证明材料及C010的局部连续方法；C010没有新增更高全域下界。本次不做额外本地科学验证，最终复验交给Actions，尚未观察其结果；原R067的本地接受状态保持。 / This publishes C009's retained complete proof materials for4.66044 and C010's local continuous method; C010 adds no higher global bound. No additional local scientific validation was run; final replay is delegated to Actions and its outcome has not been observed. R067 retains its previous local acceptance status.

[证明与复验 / Proof and replay](certificates/R068-C010/README.md) · [工作流 / Workflow](.github/workflows/r068-c010.yml)

> 以下为此前发布内容，状态按各次发布当时解释。 / The following material belongs to earlier publications; status statements refer to those publication dates.

# R067：十七单位正方形的严格下界4.66018 / R067: strict lower bound 4.66018 for seventeen unit squares

本证书证明17个任意旋转、内部两两不交且允许边界接触的单位正方形满足以下严格下界。 / This certificate proves the following strict lower bound for seventeen arbitrarily rotated unit squares with pairwise disjoint interiors and permitted boundary contact.

$$s(17)>233009/50000=4.66018.$$

这是Kleddamag公开4.66001的延续：保持其站点、规则、整数权重和总预算不变，重建严格核与2808个角区间。新增端点由Guzhou0806 / N17 project在AI辅助下完成；原收费和基线仍归Kleddamag。 / This continues Kleddamag's public 4.66001 result, retaining its sites, rules, integer weights and budget while reconstructing strict cores and 2808 angular intervals. Guzhou0806 / N17 project with AI assistance produced the new endpoint; the charge and baseline remain attributed to Kleddamag.

$$M=17000402008,\qquad\Gamma=1000026844,\qquad17\Gamma-M=54340>0.$$

完整C++与独立BigInt运行记录逐行一致。接收验收复用了这些完整记录和未改验证器，重新检查全部前提及4个区间，没有再次进行本地完整扫描。 / Complete C++ and independent BigInt run records agree row by row. Non-proposer acceptance reused these complete records and unchanged checkers, freshly checked every premise and four intervals, and did not repeat the full local sweep.

[证明 / Proof](certificates/R067-4.66018/PROOF.md) · [复验 / Reproduction](certificates/R067-4.66018/REPRODUCIBILITY.md) · [来源和许可 / Sources and licensing](certificates/R067-4.66018/ATTRIBUTION.md) · [接受范围 / Acceptance scope](certificates/R067-4.66018/evidence/ACCEPTANCE.json)

```sh
node check_records.js
g++ -O3 -std=c++17 src/verify.cpp -o verify
./verify certificate.json fresh-cpp.json
node src/replay.js certificate.json fresh-paired-run ./verify 2
```

从certificates/R067-4.66018目录运行；需要C++17、Boost开发头文件和Node.js，证明复验不需要Python。输出文件或目录须为新的。 / Run from certificates/R067-4.66018 with C++17, Boost development headers and Node.js; proof replay does not require Python. Output files or directories must be new.

只发布已完成的4.66018证明；4.6605探索失败，不是下界。未声明世界纪录、最优性、外部人类同行评审或证明助手形式化。 / Only the completed 4.66018 proof is published; the unsuccessful 4.6605 exploration is not a lower bound. No world-record, optimality, external human peer-review or proof-assistant formalization claim is made.

## 历史发布 / Historical releases

[R052 4.62003](certificates/R052-4.62003/README.md) · [R052 4.62002](certificates/R052/README.md) · [R050](certificates/R050/README.md) · [完整登记 / Full register](RESULTS.md)
