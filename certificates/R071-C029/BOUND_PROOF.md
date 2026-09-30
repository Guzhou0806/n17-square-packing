# 4.66044275的严格收费证明 / Strict charging proof for 4.66044275

以下为随回包提供的完整证明论证；本次接收未重验，完整机器复演交给Actions。 / This is the complete proof argument supplied with the return; it was not revalidated on receipt, and complete machine replay is delegated to Actions.

取L=4613/1000、T=18641771/4000000及A=L/T=18452000/18641771。T容器内17个单位方块装填缩放为L容器内17个边长A、内部互不相交的父方块；允许边界接触。 / Set L=4613/1000, T=18641771/4000000 and A=L/T=18452000/18641771. A packing of seventeen unit squares in a T-container rescales to seventeen interior-disjoint A-side parents in an L-container; boundary contact is allowed.

收费使用非负整数点权与单调Boolean资源。每个点只能被一个不交核捕获；阈值资源容量为floor(sum(coefficients)/threshold)，两两相交获胜集资源容量为1。检查器重构D4图像、站点及容量，不直接信任优化器预算。 / Charges use nonnegative integer site weights and monotone Boolean resources. A point belongs to at most one disjoint core; threshold-resource capacity is floor(sum(coefficients)/threshold), and a resource with pairwise-intersecting winning sets has capacity one. The checker reconstructs D4 images, sites and capacities rather than trusting the optimizer's budget.

相对原4.66001费用，移动一个点轨道并增加四个权重11734的物理点，得到M=17000402008+4×11734=17000448944；原889个规则轨道及权重不变。 / Moving one site orbit and adding four physical sites of weight 11734 to the original 4.66001 charge gives M=17000402008+4×11734=17000448944; the original 889 rule orbits and their weights remain unchanged.

令c(t)=(1−t²)/(1+t²)、s(t)=2t/(1+t²)。每个半角区间[a,b]配置代表t和有理核边长B，定义h=max over u=a,b of c(t)c(u)+s(t)s(u)+|c(t)s(u)−s(t)c(u)|及r=A min over u=a,b of (c(u)+s(u))/2。 / Define c(t)=(1−t²)/(1+t²) and s(t)=2t/(1+t²). Each half-angle interval [a,b] has a representative t and rational core side B, with h=max over u=a,b of c(t)c(u)+s(t)s(u)+|c(t)s(u)−s(t)c(u)| and r=A min over u=a,b of (c(u)+s(u))/2.

精确检查端点dot>0、|cross|≤dot、B>0、B<A、A−Bh>0及B(c(t)+s(t))/2≤r<L/2，保证同中心闭核严格位于整个角区间对应父的开内部，[r,L−r]²包络所有合法父中心。 / Exact checks of endpoint dot>0, |cross|≤dot, B>0, B<A, A−Bh>0 and B(c(t)+s(t))/2≤r<L/2 ensure that the concentric closed core lies strictly inside every corresponding parent's open interior, while [r,L−r]² encloses all legal parent centres.

5114区间无缝覆盖0至207107/500000>sqrt(2)−1，D4对称覆盖其余方向。全部核与包络按新的A构造，旧目标最低费不能替用。 / The 5114 intervals cover zero to 207107/500000>sqrt(2)−1 without gaps; D4 symmetry covers the remaining orientations. All cores and envelopes are constructed for the new A; minima for an older target cannot substitute.

整数Möbius展开把规则化为带符号的全子集捕获矩形。任意精度有理端点排列及完整中心扫线覆盖保守包络，额外中心只可能降低最低费。累加整数的绝对权重界受检查；原始单调闭捕获费用使事件边界不低于邻侧开单元下界。 / Integer Möbius inversion expands the rules into signed all-subset capture rectangles. Arbitrary-precision rational endpoint arrangements and complete centre sweeps cover the conservative envelope; extra centres can only reduce the minimum. An absolute-weight bound protects integer accumulation, and the original monotone closed-capture charge bounds event boundaries from below by neighboring open-cell bounds.

保留的完成摘要报告C++与独立BigInt已覆盖5114行、实际Γ=1000026844；旧逐行分区未恢复，本公开入口须重新生成并逐行比较，证书请求下限1000026409与实际最低费不同。17个父的严格内部核彼此不交，总费须同时≤M和≥17Γ，而17Γ−M=7404>0，矛盾。 / The retained completion summary reports C++ and independent BigInt coverage of5114 rows and actual Γ=1000026844; old row partitions remain missing and this public launcher must regenerate and compare them row by row; the requested certificate threshold 1000026409 differs from that actual minimum. Seventeen packed parents would have disjoint strict interior cores with total charge both ≤M and ≥17Γ, contradicting 17Γ−M=7404>0.

中心与角度取于紧配置空间，容纳及内部不重叠为闭条件，故最小容器边长可取到。排除T处装填即得到严格s(17)>T。上述计算前提将在公开CI中重新求值；此发布本身不宣告CI成功。 / Centres and orientations range over a compact configuration space, with closed containment and interior-nonoverlap conditions, so the minimum container side is attained. Excluding a packing at T yields strict s(17)>T. The computational premises are recomputed by public CI; publication itself does not declare CI success.


本端点原始证书身份为15b6bf6a936eba71338c9ea3e3b9966ae21db8116a6f5a92a8b5da5ccabed469；完整旧分区缺失，本次公开重放将重新生成全部5114区间记录。原费用体系不变。本地未重扫，发布时CI未知。 / The endpoint certificate has SHA25615b6bf6a936eba71338c9ea3e3b9966ae21db8116a6f5a92a8b5da5ccabed469. Old full partition records are missing; public replay regenerates all5114 interval records. The charge system is unchanged. No local rescan was performed, and CI is unknown at publication.
