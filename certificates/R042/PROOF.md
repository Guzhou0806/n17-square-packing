# Proof interface / 证明接口

## 1. Statement / 结论

Let $s(17)$ be the infimum side length of a square containing seventeen arbitrarily rotated unit squares with pairwise disjoint interiors, with boundary contact allowed. / 记 $s(17)$ 为容纳十七个可任意旋转且内部两两不交的单位正方形时容器正方形边长的下确界，并允许边界接触。

R042 proves / R042 证明：

$$\boxed{s(17)>\frac{115325}{24963}}.$$

The certificate uses outer side $L=4613/1000$ and parent-square side $A=24963/25000$, hence $L/A=115325/24963$. / 证书使用外框边长 $L=4613/1000$ 与父正方形边长 $A=24963/25000$，因此 $L/A=115325/24963$。

## 2. Frozen mixed certificate / 冻结混合证书

The certificate contains D4-symmetric nonnegative point charges together with nonnegative two-of-three threshold charges on triples of sites. / 证书包含具有 D4 对称性的非负点收费，以及定义在三点组上的非负“三取二”阈值收费。

After D4 expansion, the frozen object has 8,988 physical point sites and 2,008 physical threshold triples, with total budget $M=16999227356/10^9$. / 经 D4 展开后，冻结对象包含 8,988 个物理点位与 2,008 个物理阈值三元组，总预算为 $M=16999227356/10^9$。

A point charge can be collected by at most one member of a family of pairwise-disjoint strict cores. / 对任意一族两两不交的严格内核，一个点收费至多被其中一个内核收取。

For a fixed three-site threshold atom, any two subsets of size at least two intersect, so two disjoint cores cannot both trigger the same two-of-three charge. / 对固定的三点阈值原子，任意两个至少含两点的子集必有交集，因此两个不交内核不可能同时触发同一个“三取二”收费。

Consequently the total charge collected by pairwise-disjoint strict cores is at most the global budget $M$. / 因而，两两不交的严格内核能够收取的总收费不超过全局预算 $M$。

## 3. Complete parent-angle catalogue / 完整父角目录

The catalogue partitions the folded orientation range into 7,853 exact rational intervals and assigns one closed square core to every interval. / 目录把折叠后的方向范围划分为 7,853 个精确有理区间，并为每个区间指定一个闭正方形内核。

The independent rational quadratic audit checks four strict-containment inequalities for every catalogue row, for 31,412 strict positive inequalities in total. / 独立有理二次审计对每个目录行检查四个严格包含不等式，共得到 31,412 个严格为正的不等式。

The frozen static ledger also records a minimum strict-containment margin of $10^{-12}$. / 冻结静态账本还记录了 $10^{-12}$ 的最小严格包含余量。

Therefore each legal parent square contains its selected closed core strictly in its interior. / 因而，每个合法父正方形都在其内部严格包含所选闭内核。

## 4. Exact all-centre coverage / 精确全中心覆盖

The required certified charge is only $\gamma_0=999954551/10^9$. / 定理所需的认证收费仅为 $\gamma_0=999954551/10^9$。

The complete exact sweeps enumerate all event cells of every legal parent-centre domain and verify that each of the 7,853 rows has minimum charge at least $\gamma_0$. / 完整精确扫描枚举每个合法父中心域的全部事件胞元，并验证 7,853 个目录行中的每一行最低收费均不小于 $\gamma_0$。

The exact counting margin required for the theorem is / 定理所需的精确计数余量为：

$$17\cdot 999954551-16999227356=11>0.$$

Thus seventeen pairwise-disjoint parent squares would contain seventeen pairwise-disjoint strict cores whose total charge is at least $17\gamma_0>M$, contradicting the global budget. / 因此，若存在十七个两两内部不交的父正方形，它们会包含十七个两两不交的严格内核，其总收费至少为 $17\gamma_0>M$，与全局预算矛盾。

## 5. Stronger observed replay margin / 更强的复演观测余量

Both completed full replays independently report the same global minimum `1000002306` units and the same complete minimum histogram. / 两次已完成的全量复演独立得到相同的全局最低值 `1000002306` 单位以及相同的完整最低值直方图。

The minimum occurs at rows 7844–7846 and gives the stronger observed surplus / 最低值出现在第 7844–7846 行，并给出更强的观测余量：

$$17\cdot 1000002306-16999227356=811846>0.$$

This stronger observed value is an additional replay result rather than a necessary premise of the theorem, whose formal counting gate uses only the 11-unit margin above. / 这个更强的观测值属于额外复演结果，并非定理的必要前提；定理的正式计数门槛只使用上面的 11 单位余量。

## 6. Scaling and strictness / 缩放与严格性

The contradiction excludes seventeen $A$-squares inside the $L$-square. / 上述矛盾排除了十七个边长为 $A$ 的正方形装入边长为 $L$ 的正方形的可能性。

Scaling by $1/A$ excludes seventeen unit squares at side $L/A=115325/24963$. / 按比例 $1/A$ 缩放后，排除了容器边长为 $L/A=115325/24963$ 时装入十七个单位正方形的可能性。

The feasible configuration space is compact under bounded centres and angles and the containment and non-overlap constraints are closed, so endpoint exclusion yields the strict inequality $s(17)>115325/24963$. / 在中心与角度有界时，可行构型空间为紧集，且包含与不重叠约束为闭约束，因此排除端点得到严格不等式 $s(17)>115325/24963$。

## 7. Assurance boundary / 可信边界

The public package records two completed exact source-session replays and provides fresh replay paths for both implementations. / 公开成果包记录两次已完成的精确来源会话复演，并为两种实现都提供冷启动复演路径。

The BigInt checker is reconstructed from a pinned R038 source file and a pinned byte-edit recipe, so its derived bytes need not be redistributed. / BigInt 检查器由锁定的 R038 源文件与锁定的字节编辑配方重建，因此无需重新分发其派生字节。

Exact replay and file hashes do not by themselves constitute external peer review, proof-assistant formalization, global optimality, or priority verification. / 精确复演与文件哈希本身不等于外部同行审查、证明助理形式化、全局最优证明或首发核验。
