# 严格收费证明 / Strict charging proof

令L=4613/1000、T=233009/50000、A=L/T=32950/33287。若17个单位方块能装入边长T的方框，缩放后得到L容器内17个边长A、内部互不相交的父方块。 / Set L=4613/1000, T=233009/50000 and A=L/T=32950/33287. A hypothetical packing at T rescales to seventeen interior-disjoint A-side parent squares in the L-container.

证书保留Kleddamag全部2620点轨道、889规则轨道及整数权重。检查器重构20856个物理站点与完整D4图像，检查站点互异、正系数、非负权重、图像重数和相交获胜集合。 / The certificate retains Kleddamag's 2620 point orbits, 889 rule orbits and integer weights. The checker reconstructs 20856 physical sites and complete D4 images, checking distinct sites, positive coefficients, nonnegative weights, image multiplicities and intersecting winning subsets.

阈值图像的预算为floor(sum(coefficients)/threshold)：每次触发消耗至少threshold单位互不重复的站点供给。相交规则的获胜集合两两相交，因此不交核至多有一个触发该图像。按整数权重求和得到M=17000402008。 / A threshold image has budget floor(sum(coefficients)/threshold): each firing consumes at least threshold units of disjoint site supply. Pairwise-intersecting winning subsets allow at most one disjoint core to fire an intersecting-rule image. Summing with integer weights gives M=17000402008.

设c(t)=(1−t²)/(1+t²)、s(t)=2t/(1+t²)。对每个半角区间[a,b]及代表t，定义h=max over u=a,b of c(t)c(u)+s(t)s(u)+|c(t)s(u)−s(t)c(u)|，r=A min over u=a,b of (c(u)+s(u))/2。 / Set c(t)=(1−t²)/(1+t²) and s(t)=2t/(1+t²). For every half-angle interval [a,b] and representative t, define h=max over u=a,b of c(t)c(u)+s(t)s(u)+|c(t)s(u)−s(t)c(u)| and r=A min over u=a,b of (c(u)+s(u))/2.

精确检查端点的dot>0及|cross|≤dot确保端点旋转支撑界覆盖整个区间；证书逐项满足B>0、B<A、A−Bh>0，以及B(c(t)+s(t))/2≤r<L/2。因此代表角闭核严格位于父开内部，且[r,L−r]²覆盖所有合法父中心。 / Exact endpoint checks dot>0 and |cross|≤dot make the endpoint support bound valid throughout each interval. Every entry satisfies B>0, B<A, A−Bh>0 and B(c(t)+s(t))/2≤r<L/2. Thus the closed representative core lies strictly inside its parent, and [r,L−r]² covers all legal parent centres.

2808个区间无缝从0覆盖到207107/500000>sqrt(2)−1，D4不变性覆盖其余方向。角区间来自原2168根区间，其中640个二分，1528个保持；严格核按新父边长重建。 / The 2808 intervals form a gapless chain from zero to 207107/500000>sqrt(2)−1, with D4 invariance covering other orientations. Of the original 2168 root intervals, 640 are bisected and 1528 retained; strict cores are rebuilt for the new parent side.

整数Möbius展开把单调捕获规则化为带符号的全子集捕获矩形。任意精度整数端点排序及完整事件扫线，遍历保守中心包络；多余中心只能压低最低费。原子绝对权重和小于2^50保证费用精确累加。单调闭捕获保证事件边界费用不低于邻近开单元的下界。 / Integer Möbius inversion expresses monotone capture rules as signed all-subset capture rectangles. Arbitrary-precision endpoint sorting and complete event sweeps cover the conservative centre envelope; extra centres can only lower the minimum. An absolute atom-weight sum below 2^50 guarantees exact charge accumulation. Monotone closed capture extends open-cell lower bounds to event boundaries.

全部2808个区间的C++与独立BigInt记录在最低费和单元数上逐行一致，得到Γ=1000026844。若17个父存在，其严格核互不相交，总费既≤M又≥17Γ；而17Γ−M=54340>0，矛盾。 / C++ and independent BigInt records agree on the minimum and cell count for every one of the 2808 intervals, giving Γ=1000026844. Seventeen packed parents would have disjoint strict cores with total charge both ≤M and ≥17Γ, contradicting 17Γ−M=54340>0.

有界中心与角度配置空间紧致，容纳及内部不重叠条件闭合，故最小容器边长可取到。排除T处装填因此证明严格的s(17)>T。数值优化、有限样本或CI状态都不是证明前提。 / Bounded centre and orientation configuration space is compact, and containment and interior non-overlap conditions are closed, so the minimum side is attained. Exclusion at T therefore proves the strict inequality s(17)>T. Numerical optimization, finite samples and CI status are not proof premises.
