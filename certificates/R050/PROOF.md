# R050 证明 / R050 proof

记 s(17) 为容纳十七个可任意旋转、内部两两不交的单位正方形时，容器正方形边长的下确界；允许边界接触。 / Let s(17) be the infimum container side length for seventeen arbitrarily rotated unit squares with pairwise disjoint interiors; boundary contact is allowed.

$$\boxed{s(17)>4613000/998509}.$$

## 有理证书与严格内核 / Rational certificate and strict cores

固定外框边长 L=4613/1000、父正方形边长 A=998509/1000000、余量 rho=10^-15。点资源及三取二阈值资源的坐标和权重与 R043 完全相同，整数权重单位为 10^-9。 / Fix outer side L=4613/1000, parent-square side A=998509/1000000 and margin rho=10^-15. Point and two-of-three threshold resource coordinates and weights are identical to R043, with integer weight units of 10^-9.

R043 的 7853 个角参数区间各均分为二，共 15706 个连续覆盖区间；区间 [a,b] 取 t=(a+b)/2。半角参数 u 对应的精确方向为下式。 / Each of R043's 7853 angular parameter intervals is bisected, giving 15706 contiguous covering intervals; use t=(a+b)/2 on [a,b]. The exact direction associated with the half-angle parameter u is as follows.

$$c_u=\frac{1-u^2}{1+u^2},\qquad s_u=\frac{2u}{1+u^2}.$$

各行构造以父中心为中心、方向为 t 的闭正方形内核，其边长 B 由下式给定。 / For each row, construct a closed square core centred at the parent centre and oriented at t, with side B given by the following formula.

$$F=\max_{u\in\{a,b\}}(c_tc_u+s_ts_u+|c_ts_u-s_tc_u|),\qquad B=(A-\rho)/F.$$

此构造公式本身不替代区间证明。独立有理检查器在每个完整区间上检查四个相应二次不等式的端点及内部极值，全部 62824 个不等式严格成立，从而内核位于对应父正方形的开内部。结合证书的对称性与角目录覆盖，这对任意父方向都成立。 / The construction formula does not replace an interval proof. The independent rational checker tests endpoints and interior extrema of four relevant quadratic inequalities on every complete interval; all 62824 inequalities hold strictly, placing each core inside its parent's open interior. Together with certificate symmetry and angular catalogue coverage, this applies to every parent orientation.

## 全中心收费与预算 / All-centre charge and budget

证书包含 1134 个点轨道和 253 个三取二阈值资源轨道，展开为 8988 个站点及 2008 个阈值三点集合。各资源权重非负，全局预算为 M=17003093868 个整数单位。 / The certificate contains 1134 point orbits and 253 two-of-three threshold resource orbits, expanding to 8988 sites and 2008 threshold triples. All resource weights are nonnegative, with total budget M=17003093868 integer units.

当闭核含有一个点资源时收取其权重；当其包含某阈值三点集合中的至少两点时收取该阈值资源的权重。完整精确事件胞元扫描覆盖所有合法父中心所需的核中心域，包括边界与退化事件。 / A closed core collects a point resource's weight when it contains that point, and a threshold resource's weight when it contains at least two of its three sites. Complete exact event-cell scans cover the core-centre domain required for every legal parent centre, including boundaries and degenerate events.

独立 Python 复演检查全部 15706 行；其逐行账本与 BigInt 的 118 个连续完整分块在逐块完整直方图及最低值上相同，完整行覆盖和无逃逸条件均通过。两个实现的条带计数口径不同，不以条带总数相等作为对照条件。 / The independent Python replay checks all 15706 rows; its row ledger agrees with BigInt's 118 contiguous complete blocks on every block's full histogram and minimum, with complete coverage and no escapes verified. The implementations count slabs differently, so equal slab totals are not a comparison requirement.

每个合法父正方形因此有一个收费至少 gamma=1000271689 的严格内核，最低值出现在行 10115 至 10121。 / Every legal parent square therefore has a strict core charging at least gamma=1000271689, with the minimum attained on rows 10115 through 10121.

若父正方形内部两两不交，则其严格闭核彼此不交。因此每个点资源至多被一个核收费；对于同一三点集合，两个至少含两点的子集必有交点，所以两个不交核不可能同时触发同一个三取二资源。 / If parent interiors are pairwise disjoint, their strict closed cores are disjoint. Thus each point resource is charged at most once; two subsets containing at least two sites of the same triple must intersect, so two disjoint cores cannot both trigger that two-of-three resource.

任意十七个这样的核总收费至多为 M，但统一最低收费要求总收费至少为 17gamma，产生矛盾。 / Any seventeen such cores collect at most M in total, but the universal minimum requires at least 17gamma, a contradiction.

$$17\gamma-M=17\times1000271689-17003093868=1524845>0.$$

## 端点排除与严格不等式 / Endpoint exclusion and strict inequality

故边长 L 的外框不能容纳十七个边长 A 的父正方形；按 1/A 缩放，边长 L/A=4613000/998509 的容器不能容纳十七个单位正方形。 / Thus an outer square of side L cannot contain seventeen parent squares of side A; scaling by 1/A excludes seventeen unit squares in a container of side L/A=4613000/998509.

若下确界恰为此端点，则可取容器边长趋于端点的可行装填序列。所有中心位于共同有界域，角参数属于紧集，因此存在收敛子列。顶点包含与内部不重叠条件在极限下保持，得到已排除的端点装填，矛盾。因此下界严格。 / If the infimum equalled this endpoint, there would be feasible packings with container sides tending to it. Their centres lie in a common bounded domain and their orientations lie in a compact set, yielding a convergent subsequence. Vertex containment and interior non-overlap persist in the limit, producing the excluded endpoint packing, a contradiction. The lower bound is therefore strict.

## 成果地位 / Status of the result

R050 延续 R043 的资源结构并改变父边长和角度内核，不依赖其他未接受证书。R050 已不是目前已知最优下界：维护者获知 Kleddamag 已取得尚未公开的 4.62001 下界，该成果归 Kleddamag 所有，其证明与验证不在本包范围内。 / R050 continues R043's resource structure while changing the parent side and angular cores; it does not rely on other unaccepted certificates. R050 is no longer the best currently known lower bound: the maintainer has learned of Kleddamag's unpublished 4.62001 lower bound, which is Kleddamag's result and whose proof and verification are outside this package.
