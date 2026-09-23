# R043 proof / R043 证明

Let $s(17)$ be the infimum side length of a square containing seventeen arbitrarily rotated unit squares with pairwise disjoint interiors, with boundary contact allowed. / 记 $s(17)$ 为容纳十七个可任意旋转且内部两两不交的单位正方形时容器正方形边长的下确界，并允许边界接触。

R043 proves / R043 证明：

$$\boxed{s(17)>\frac{461300}{99851}}.$$

The outer side is $L=4613/1000$ and the parent-square side is $A=99851/100000$, so $L/A=461300/99851$. / 外框边长为 $L=4613/1000$，父正方形边长为 $A=99851/100000$，因此 $L/A=461300/99851$。

R043 continues the R042 mixed point + two-of-three threshold certificate language, keeps all 253 threshold orbits unchanged, and changes no point-support coordinates. / R043 延续 R042 的 point + two-of-three threshold 混合证书语言，保持全部 253 个 threshold orbit 不变，并且不改变 point support 坐标。

Four previously zero-weight D4 point orbits are activated: 71, 177, 490, and 614, with prototype weight increments `297687`, `67695`, `56186`, and `61746` in $10^{-9}$ units. / 四个此前权重为零的 D4 point orbit 被激活：71、177、490、614，其 prototype 权重增量分别为 `297687`、`67695`、`56186`、`61746` 个 $10^{-9}$ 单位。

Each of these four D4 orbits has size 8, so the total budget increases by / 这四个 D4 orbit 的大小均为 8，因此总预算增加：

$$8(297687+67695+56186+61746)=3866512$$

weight units, giving $M=17003093868/10^9$. / 个权重单位，从而得到 $M=17003093868/10^9$。

All 7,853 catalogue rows are retargeted at the new parent side, and the independent rational quadratic audit checks four strict containment inequalities per row. / 全部 7,853 个目录行都在新的父边长下重新定向，独立有理二次审计对每行检查四个严格包含不等式。

All `31,412/31,412` containment inequalities pass, with positive minimum rational margin, so every legal parent square strictly contains its selected closed core. / `31,412/31,412` 个包含不等式全部通过，最小有理余量严格为正，因此每个合法父正方形都严格包含其所选闭内核。

A point charge can be collected by at most one member of a family of pairwise-disjoint strict cores. / 对一族两两不交的严格内核，一个 point charge 至多只能被其中一个内核收取。

For a two-of-three threshold atom, two triggering cores would each contain at least two sites of the same three-site set; any two such subsets intersect, so two disjoint cores cannot both trigger the same atom. / 对一个 two-of-three threshold atom，若两个内核都触发，则它们分别包含同一三点集合中的至少两点；任意两个这样的二元子集必有交集，因此两个不交内核不可能同时触发同一原子。

Hence the total collected charge of pairwise-disjoint strict cores is at most the global budget $M$. / 因而，两两不交的严格内核能够收取的总收费不超过全局预算 $M$。

Both complete exact event-cell replay engines cover all 7,853 rows and agree on the entire row-minimum histogram. / 两套完整精确事件胞元复演引擎都覆盖全部 7,853 行，并对完整的逐行最低值直方图完全一致。

Their common global minimum is / 它们共同得到的全局最低收费为：

$$\gamma=1000181993/10^9,$$

attained at row 2552. / 该最低值出现在 row 2552。

The exact counting surplus is / 精确计数余量为：

$$17\cdot1000181993-17003093868=13>0.$$

A hypothetical packing of seventeen $A$-squares in the $L$-square would therefore yield seventeen pairwise-disjoint strict cores collecting at least $17\gamma>M$, contradicting the global budget. / 因此，若十七个边长为 $A$ 的正方形能够装入边长为 $L$ 的正方形，则会得到十七个两两不交的严格内核，其总收费至少为 $17\gamma>M$，与全局预算矛盾。

Thus the parent-square endpoint is infeasible, and scaling by $1/A$ excludes seventeen unit squares at side $L/A=461300/99851$. / 因而该父正方形端点不可行，按比例 $1/A$ 缩放后，边长为 $L/A=461300/99851$ 的容器不能装入十七个单位正方形。

The bounded centre-angle configuration space is compact and the containment/non-overlap constraints are closed, so endpoint exclusion yields the strict lower bound above. / 中心与角度参数有界，因此构型空间为紧集，且包含与不重叠约束为闭约束，所以排除端点即可得到上述严格下界。

The Python and source-distinct BigInt engines use different slab-counting conventions, so their slab totals are not required to agree; certificate identity, global minimum, complete row-minimum histogram, budget, full row coverage, and zero escape rows do agree. / Python 与不同源码的 BigInt 引擎采用不同的 slab 计数口径，因此不要求 slab 总数相等；证书身份、全局最低值、完整逐行最低值直方图、预算、完整行覆盖以及零 escape rows 均一致。

R043 makes no maximality claim and does not claim that external priority or world-record status has been independently established. / R043 不主张达到该架构的极限，也不主张外部首发或世界纪录状态已经独立确认。
