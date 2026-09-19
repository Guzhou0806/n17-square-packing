# R012 — Complete parent-angle certificate / 完整父角证书

## Statement / 命题

Let s(17) be the infimum containing-square side for seventeen unit squares with arbitrary rotations and pairwise disjoint interiors. Boundary contact is permitted. The computer-assisted result is

$$s(17)\ge S=\frac{461300}{99999}.$$

记 s(17) 为十七个可旋转、内部两两不交的单位正方形的最小容器边长之下确界，允许边界接触。本证书给出上述普通下界。小数夹逼针对常数 S，**不是**未知的 s(17)：

```text
4.61304613046130461304 <= S < 4.61304613046130461305.
```

No global optimality, new packing, independent peer review or priority is asserted. Exact geometry and the finite-to-continuous argument remain review obligations. / 不主张最优装填、新上界、外部同行审查或首发。精确程序与有限到连续的论证均需审查。

## 1. Measure / 测度

Set L=4613/1000, A=99999/100000. `orbits.json` lists 206 rows (x,y,w). Divide coordinates by 100000 and each point weight by 1000000; expand distinct images under the eight symmetries of [0,L]^2. The result is 1616 distinct nonnegative weighted points, of total mass M=424969/25000. The verifier reconstructs all images and checks equality with the original R012 measure by a canonical arithmetic-data digest. There is no optimizer in verification.

令 L=4.613、A=0.99999。整数轨道表按上述分母展开 D4 不同像，产生 1616 个点，总质量 M=16.99876。公开版改变了数据编码，没有改变坐标、权重或轨道；复验不依赖优化器或历史 PASS。D4 限制测度，**不要求假想装填整体对称**。

## 2. A selectable strictly interior core / 可选择的严格内部核

For a rational half-tangent u, define c(u)=(1-u^2)/(1+u^2), s(u)=2u/(1+u^2). The parent angle is phi=2 arctan(u). An entry specifies its entire closed parent interval [a,b], a concentric core direction t, and core side B. The exact condition is

$$B\max_{u\in\{a,b\}}\{c(t)c(u)+s(t)s(u)+|s(t)c(u)-c(t)s(u)|\}<A.$$

The verifier checks that relative angles remain within pi/4. The greatest absolute relative angle occurs at an endpoint, and cos(delta)+|sin(delta)| increases with that angle on the supported range. Thus the displayed rational inequality proves **strict containment for the whole interval**, not angular sampling.

半角参数给出精确有理单位轴。相对角范围逐项检查；最大相对角在区间端点，支持宽度因子在此范围单调。上述严格不等式因此覆盖整个连续父角区间。每个父方块只选择一个同中心核，不把多个重叠备选核的质量相加。

## 3. Every legal parent center / 全部合法父中心

At parent half-angle u, the legal center square is [A f(u)/2,L-A f(u)/2]^2, where

$$f(u)=\frac{1+2u-u^2}{1+u^2},\qquad f'(u)=\frac{2(1-2u-u^2)}{(1+u^2)^2}.$$

On [0,1), f has a single interior maximum. The endpoint minimum therefore defines the union of these nested center squares:

$$D_{a,b}=[r,L-r]^2,\qquad r=\frac A2\min(f(a),f(b)).$$

Every entry is checked over **all of this two-dimensional domain**. The verifier also checks B(c(t)+s(t))/2 <= r < L/2. This neither removes real parent poses nor admits an unsupported degenerate domain.

父中心正方形相互嵌套；f 只有一个内部极大值，故端点较小值给出整个区间的完整中心并集。程序检查该二维闭域，保留所有真实父姿态，同时验证核在容器内及中心域有内点。

## 4. Exact translation sweep / 连续平移的精确扫描

Rotate center coordinates into the core frame. Each point is captured exactly on a closed axis-aligned square of side B. All vertical rectangle events **and all rotated domain vertex coordinates** split the domain into open strips. Inside a strip the active rectangles are fixed. Horizontal events split it into constant-charge cells.

The scan computes the v-projection of the intersection of the **whole strip** and the legal domain, not just its midpoint. Domain vertices are strip events, so the piecewise-affine lower and upper boundary extrema occur at the strip endpoints. Every horizontal open cell with a positive-length reachable intersection is tested. Integers accumulate exact mass; Fraction arithmetic decides geometry. A rational point inside a minimizing cell is reconstructed and all atom memberships are recounted directly.

将中心旋转到核坐标后，每个原子对应一个闭捕获矩形。矩形竖边与合法中心多边形的所有顶点横坐标共同切分条带，程序查询整个条带的可达纵向投影，而非条带中点。域顶点已成为事件，故分段仿射上下边界在每条带端点取得投影极值。所有可达二维开胞元被检查；最小胞元另构造有理内点逐原子核对。

Closed boundaries cannot hide a lower value. Every domain boundary point is approachable from interior non-event points. Some subsequence lies in one cell of the finite arrangement. Closed capture retains that cell's captured points at the limit, and all weights are nonnegative. Positive-area domain, closed capture and nonnegative mass are essential assumptions.

闭域边界可由合法域内非事件点逼近；有限排列允许选出同一胞元子列，闭捕获保留其全部原子，非负性使边界质量不下降。因此无需以浮点边界抽样补洞。

## 5. Complete angle union / 全角拼接

Let h=207107/1440000000 and T=2880h=207107/500000. `catalogue.json` defines sixty explicit entries followed by midpoint cells I_k=[max(0,(k-1/2)h),min(T,(k+1/2)h)].

| Entries / 条目 | Core rule / 核规则 |
|---|---|
| First sixty, ending at 31h/2 / 前六十项 | Explicit rational (a,b,t,B) / 明确有理四元组 |
| k=16,...,977 | t=kh, B=6249/6250 |
| k=978,...,1144 | t=kh, B=49992449/50000000 |
| k=1145,...,2880 | t=kh, B=19997/20000 |

All 2925 closed parent intervals meet without gaps, from zero to T; T^2+2T-1>0 extends past tan(pi/8). Forty-eight core directions are off the original grid. Their coverage is recomputed, not inherited. Unlike the original mixed-language replay, this public Python entry **recomputes every catalogue parent envelope directly**, including the high-angle entries.

2925 个闭父角区间无缝覆盖 [0,T]，从而覆盖归约父角 [0,pi/4]。48 个网外核方向有自己的完整覆盖检查。本公开入口直接重算每一目录项的父中心域，包括原先可由高角底座继承的部分；不读取旧日志作为覆盖前提。

## 6. Counting and rescaling / 计数与缩放

All entries have charge at least gamma=250023/250000. Fold an individual parent's angle by square periodicity and container symmetries, choose its core, then undo the symmetry. Invariance preserves the charge. For seventeen interior-disjoint A-parents, their chosen closed cores are pairwise disjoint, since each lies strictly inside its parent. They would satisfy

$$17\gamma\le\sum_i\mu(P_i)\le M,\qquad17\gamma-M=\frac{701}{250000}>0,$$

which is impossible. Scaling unit squares at side L/A by A yields these impossible parents. Register the weak lower bound s(17)>=L/A only.

所有条目共用同一测度与最低收费。逐父方块作对称归约、选核后逆变换，不施加整体对称。十七个父内部不交，严格内部闭核因此不交，产生上述同预算质量矛盾。按 A 缩放即给出 S=L/A。此处只登记普通 >=，不另作最优值严格不等式主张。

The pinned Mira endpoint squared is 17650291964463886688094912400/829429719507765981945905041. Exact comparison gives

$$S^2-S_M^2=\frac{1338724704271950594905978540377600}{8294131309963187985770427210937705041}>0.$$

该比较只针对明确锁定的来源端点，不等于穷尽公开纪录。

## 7. Controls and assurance / 控制与可信边界

`counterexamples.json` retains five legal parents whose specified inferior core recipes fail, at charges .988704, .999638 or .998421. Projection and rational polygon predicates recheck these witnesses. They refute those core choices, not every possible inner core at the parent. The complete selector supplies other choices.

保留的五个反例均是真实父中心，否定的是原配方，不是父姿态本身。新的目录不能倒过来将失败配方改写成成功。

The Python translation kernel is retained from the earlier rational sweep, with its event geometry shared across any accumulator controls. Re-execution in another language/environment and per-witness cross-checks are not a second independently designed full geometric proof. `--records` checks arithmetic and witnesses only; it is never a full-coverage PASS. See [reproduction](README.md) and [attribution](ATTRIBUTION.md).

Python 内核沿用已有有理事件几何；重复执行与单点交叉核对不等于第二份独立全几何证明。records 模式没有覆盖计算，不能当作完整验收。
