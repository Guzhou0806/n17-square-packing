# 条件联合几何的解析桥 / Analytical bridge for conditional joint geometry

所有结论以T=9321/2000=4.6605及下述第一锚点盒为条件。容器边长L=4613/1000，父方块边长A=L/T=9226/9321；除以A即可回到单位方块。允许闭边界接触，开内部两两不交；角度彼此独立。 / All conclusions assume T=9321/2000=4.6605 and the first-anchor box below. The container side is L=4613/1000 and each parent square has side A=L/T=9226/9321; division by A gives unit squares. Closed-boundary contact is allowed and open interiors are disjoint; rotations are independent.

用有理半角t∈[0,1]表示方向u=((1−t²)/(1+t²),2t/(1+t²))，v=(−u_y,u_x)。锚点中点C=(1915223443770787,695624205775549)/10¹⁵，t=350755760770591/10¹⁵，中心半宽各1/50、t半宽1/100。只对其中合法父断言；该盒不覆盖全部低费锚点。 / Use the rational half-angle t∈[0,1] with u=((1−t²)/(1+t²),2t/(1+t²)) and v=(−u_y,u_x). The anchor midpoint is C=(1915223443770787,695624205775549)/10¹⁵, t=350755760770591/10¹⁵, with centre half-widths1/50 and t half-width1/100. Claims apply only to legal parents within this box; it does not cover all low-charge anchors.

## C028：覆盖和分量前提 / Cover and component prerequisites

令ε=1/100000、α=1−ε、d=(T−2α)/3，网格G_(4j+i)=A(α+id,α+jd)，0≤i,j≤3。父对最近容器轴的偏角为φ，m=cosφ+sinφ；其同心轴平行开核边长为1/m（单位尺度），真实壁面使中心落在[m/2,T−m/2]²。因此核任一坐标区间(a,b)满足b≥(m+1/m)/2≥1，a≤T−1。 / Set ε=1/100000, α=1−ε, d=(T−2α)/3 and G_(4j+i)=A(α+id,α+jd) for0≤i,j≤3. For tilt φ relative to the nearest container axis, put m=cosφ+sinφ. The concentric axis-aligned open core has side1/m in unit scale, and actual wall constraints place the centre in[m/2,T−m/2]². Each core coordinate interval(a,b) therefore satisfies b≥(m+1/m)/2≥1 and a≤T−1.

若d<1/(cosφ₀+sinφ₀)，则φ≤φ₀的核必在横纵各捕获一个网格坐标：端点严格内移排除两端漏点，间距小于核长排除内部漏点。取tan(φ₀/2)=1721/25000满足此严格条件。因此所有避点父都包含于中心[A/2,L−A/2]²、半角[t₀,(1−t₀)/(1+t₀)]的闭根盒。 / If d<1/(cosφ₀+sinφ₀), every core with φ≤φ₀ captures a grid coordinate in each direction: strict endpoint inset prevents escape at the ends, and spacing below core length prevents escape between points. The choice tan(φ₀/2)=1721/25000 satisfies this strict condition. Thus all point-avoiding parents lie in the closed root box with centre[A/2,L−A/2]² and half-angle[t₀,(1−t₀)/(1+t₀)].

锚点经真实壁面安全收紧后的公共开核捕获G1；原宽盒共同闭外包排除其余15点。因此每个合法锚点恰捕获G1。对实际17父装填，令v为避点父数，u为无主点数，e为非避点父捕获点数减一的总和。每点至多有一个主人，故17−v+e=16−u，即v=1+e+u，特别v≥1。 / The common open core after safe wall tightening of the anchor captures G1, while an outer enclosure of the original box excludes the other15 points. Every legal anchor therefore captures exactly G1. In an actual17-parent packing, let v count point-avoiding parents, u unowned points and e the sum of captured-point counts minus one over non-avoiding parents. Each point has at most one owner, so17−v+e=16−u, hence v=1+e+u and v≥1.

公共内核公式为B=(A−2(ex+ey))/(1+2et)>0，方向和中心取盒中点。半角差给|sin(θ−θ₀)|≤2et，中心投影误差≤ex+ey，故该开核属于所有父。相应共同闭外包边长为Aout=A(1+2et)+2(ex+ey)。 / The common inner-core side is B=(A−2(ex+ey))/(1+2et)>0 at the midpoint centre and orientation. The half-angle difference gives |sin(θ−θ₀)|≤2et and centre projection error≤ex+ey, placing the open core within every parent. The corresponding common closed outer-enclosure side is Aout=A(1+2et)+2(ex+ey).

41,215节点完整闭树按x,y,t轮流二等分，不漏公共边界。叶W用角端点最小壁面半宽严格排除不合法父；P在四个中心角点和全角区间证明严格捕获；C用真实壁面推得角部捕获；A证明候选开内切圆与锚公共核相交；K证明两个公共开核相交；J排除全部真实分离轴。未决U完整保留。 / A complete41,215-node closed tree bisects x,y,t cyclically without losing shared boundaries. Leaf W strictly excludes wall-infeasible parents using the minimum wall half-width at angle endpoints; P proves strict capture over four centre corners and the entire angle interval; C derives corner capture from actual walls; A proves intersection of the candidate open incircle with the common anchor core; K proves intersection of common open cores; J excludes every actual separating axis. All unresolved U leaves are retained.

C叶的左下角理由：若合法中心两坐标≤αA，则到角点差非负且≤A(α−m/2)；u投影≤A(αm−m²/2)≤A(α−1/2)<A/2，v绝对投影也<A/2，因为(m−1)((m+1)/2−α)≥0。其余角反射同理。A叶利用到凸核的距离为凸函数，中心四角距离均<A/2便覆盖整个中心盒。所有删除必须对盒中每个锚点成立。 / For a lower-left C leaf, legal centre coordinates≤αA give nonnegative corner displacements≤A(α−m/2). The u projection is≤A(αm−m²/2)≤A(α−1/2)<A/2 and the absolute v projection is also<A/2, using(m−1)((m+1)/2−α)≥0. Other corners follow by reflection. An A leaf uses convexity of distance to the convex core: distances<A/2 at every centre corner cover the entire box. Every deletion must be valid for every anchor in the box.

树的W/P/C/A/K/J/U叶数为1668/7103/16/66/9/160/11586。保留11,586个深度18小盒，每坐标64格；闭盒相交等价于三个格指标分别相差≤1。26邻接的18个分量由两实现独立计算。每个中心外包矩形扩大A/10⁶后仍有直径<A，而不交父的内切圆中心距≥A，因此每分量容量≤1。真实双方块见证不等于18分量可共同占据。 / Leaf counts W/P/C/A/K/J/U are1668/7103/16/66/9/160/11586. The11,586 retained depth18 boxes form a64-cell grid in each coordinate; closed boxes intersect exactly when each grid index differs by≤1. Two implementations independently compute18 components under26-neighbour adjacency. Each centre-enclosing rectangle, expanded by A/10⁶, still has diameter<A, whereas disjoint parents' incircle centres are at distance≥A. Thus each component has capacity≤1. Real two-square witnesses do not imply joint occupancy of all18 components.

## C029：连续冲突与强制空点 / Continuous conflicts and forced holes

任意两个父不交必有分离轴来自任一父的u/v方向。设相对角δ∈[−π/2,π/2]，f(δ)=cosδ+|sinδ|。角区间重叠时取qmin=1；否则f在同号区间凹，取两个相对端点较小值为下界。分离要求某轴|n·(C₂−C₁)|≥A(1+qmin)/2。若全部轴的中心差盒四角投影在全角区间严格小于该阈值，就排除所有分离选择，接触等号不删。 / Any disjoint pair has a separating axis along a u/v direction of one parent. For relative angle δ∈[−π/2,π/2], let f(δ)=cosδ+|sinδ|. Overlapping angle intervals allow qmin=1; otherwise f is concave on the same-sign interval, so the smaller relative-endpoint value is a lower bound. Separation requires |n·(C₂−C₁)|≥A(1+qmin)/2 on some axis. Strictly smaller projections at all centre-difference corners over the full angle intervals exclude every axis; contact equality is retained.

C++以端点及内部驻点求投影极值；BigInt乘1+t²化为二次多项式，在端点及可能的凸二次顶点检查严格正性。不得仅查角端点。配对树从两个分量的完整三维包围盒开始，S保留严格二等分的两个子盒；X为全分离轴矛盾，W为壁面，P为避点父严格捕获，A为与所有第一锚点冲突。拒绝未决叶、截断和额外节点。 / C++ checks projection extrema at endpoints and interior stationary points. BigInt multiplies by1+t² and checks quadratic positivity at endpoints and any interior convex vertex. Angle endpoints alone are insufficient. Pair trees start from both components' complete three-dimensional enclosing boxes. S retains both exact halves; X is an all-axis contradiction, W a wall contradiction, P strict capture by an avoiding parent, and A conflict with every first anchor. Unresolved leaves, truncation and extra nodes are rejected.

17条冲突边如下，共76,449节点，仅适用于避点父： / The following17 conflict edges total76,449 nodes and apply only to point-avoiding parents:

```
(0,1) (0,3) (1,2) (1,4) (2,5) (3,4) (5,6)
(6,9) (8,9) (9,13) (10,14) (10,15)
(11,13) (11,17) (12,16) (15,16) (16,17)
```

分量0占用迫使G0无主；分量10占用迫使G2无主。潜在点主人的完整中心域取[A/2,L−A/2]²∩(G+[−3A/4,3A/4]²)，因内部点到中心每坐标距离<A/√2<3A/4；其角保留全部[0,1]，不能对它用避点捕获删除。两棵完整树分别8,225和10,543节点。 / Occupancy of component0 forces G0 unowned; occupancy of component10 forces G2 unowned. A potential owner's complete centre domain is[A/2,L−A/2]²∩(G+[−3A/4,3A/4]²), since each coordinate distance from an interior point to its centre is<A/√2<3A/4. Its angle retains the full[0,1] range, and avoiding-parent capture deletion cannot be applied to it. The two complete trees have8,225 and10,543 nodes.

新增N叶只在整个主人盒对所需点具有统一外侧面时删除。C++检查有向投影在角两端>A/2；中间方向是端方向的非负组合，系数和≥1，所以正阈值下安全。BigInt独立检查二次正性。令zᵢ为分量占用指标，两个不同强制空点给u≥z₀+z₁₀，从而v≥1+e+z₀+z₁₀。 / The new N leaf deletes an owner box only when one uniform outside face excludes the required point. C++ checks directed projections>A/2 at both angle endpoints: each intermediate unit direction is a nonnegative combination of endpoint directions with coefficient sum≥1, making the positive threshold safe. BigInt independently checks quadratic positivity. If zᵢ indicates occupancy, the distinct forced holes give u≥z₀+z₁₀ and hence v≥1+e+z₀+z₁₀.

## 容量、见证与剩余未知 / Capacity, witnesses and remaining unknowns

七条不相交边(1,2),(3,4),(5,6),(9,13),(10,14),(11,17),(15,16)使14顶点贡献至多7，其余4顶点各至多1，因此避点父总数≤11。独立集按大小0..18计数如下；C++位掩码递推与BigInt递归枚举独立重算。 / Seven vertex-disjoint edges(1,2),(3,4),(5,6),(9,13),(10,14),(11,17),(15,16) limit14 vertices to7 occupants, with at most1 on each of the remaining4, giving at most11 avoiding parents. Independent-set counts by size0..18 below are recomputed by C++ bitmask recurrence and BigInt recursive enumeration.

```
[1,18,136,564,1413,2225,2227,1406,548,128,17,1,0,0,0,0,0,0,0]
```

唯一大小11抽象独立集为{0,2,4,6,7,8,12,13,14,15,17}，不是实际11父构型。加入非空及v≥1+z₀+z₁₀，大小1/2项变16/135，共8,680个必要子集，不是装填枚举。 / The unique abstract independent set of size11 is{0,2,4,6,7,8,12,13,14,15,17}; it is not an actual11-parent configuration. Nonemptiness and v≥1+z₀+z₁₀ change size1/2 counts to16/135, leaving8,680 necessary subsets, not an enumeration of packings.

153对分量分为17排除、128个真实三方块见证、8未知：(4,5),(4,7),(5,8),(7,8),(7,12),(8,11),(10,12),(11,12)。见证重算墙面、严格避点、实际分量小盒并集成员关系及全部三对分离；不能只查分量包围盒。未找到数值解不等于不相容。 / The153 component pairs split into17 exclusions,128 actual three-square witnesses and8 unknowns:(4,5),(4,7),(5,8),(7,8),(7,12),(8,11),(10,12),(11,12). Witness checks recompute walls, strict avoidance, membership in the actual component-box union and all three pair separations, not merely membership in a bounding box. Failure to find a numerical solution does not prove incompatibility.

分量{0,2,4,6,8,12,13,14,17}的9避点父加第一锚点构成10父部分装填。每父中心可独立变±10⁻⁶、半角±10⁻⁷；共同外包在容器内，全部45对严格分离，9父外包严格避点，锚小盒仍在原宽盒中。因此存在30参数非零宽部分装填族，给Vmax≥9；没有证明还能加入7父。 / Nine avoiding parents in components{0,2,4,6,8,12,13,14,17}, together with the anchor, form a10-parent partial packing. Each centre varies independently by±10⁻⁶ and each half-angle by±10⁻⁷. Common outer enclosures remain inside the container, all45 pairs strictly separate, the9 avoiding enclosures strictly exclude grid points, and the anchor's small box remains within the original box. This gives a30-parameter positive-width partial-packing family and Vmax≥9; adding another7 parents has not been proved possible.

Vmax上界对原宽盒中全部合法锚点成立，下界由一个具体小盒族达到。仍未知Vmax是9、10还是11；v=1尚有16分量未排除，多避点分支尚未闭合，更未覆盖全部第一锚点。这些结论不能转换成4.6605的全局排除。 / The upper bound on Vmax applies to every legal anchor in the original box; the lower bound is attained by one specific small-box family. Whether Vmax is9,10 or11 remains unknown. The v=1 branch retains16 components, multiple-avoider branches remain open, and all first anchors are not covered. These results cannot be converted into a global exclusion at4.6605.
