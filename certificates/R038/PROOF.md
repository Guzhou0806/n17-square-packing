# R038 proof / R038 证明

## Statement / 命题

Let $s(17)$ be the infimum side length of a square that can contain seventeen unit squares with arbitrary rotations and pairwise disjoint interiors, with boundary contact allowed. / 记 $s(17)$ 为容纳十七个可任意旋转且内部两两不交的单位正方形时容器正方形边长的下确界，并允许边界接触。

The R038 computer-assisted certificate proves / R038 计算机辅助证书证明：

$$\boxed{s(17)>\frac{461300000000}{99974999999}=\frac{65900000000}{14282142857}=4.614153538430749222689979987\ldots}$$

The strict inequality concerns a lower-bound constant, not a two-sided enclosure of the unknown optimum. / 该严格不等式给出的是下界常数，并不是对未知最优值的双侧夹逼。

## 1. Pinned base certificate / 锁定基础证书

The numerical measure and 4,391-row parent-angle catalogue are pinned to `Mira-acc/17squares` commit `ac464dd06ded72e2f6eb2c2f3d510b01391c056d`, file `certificates/lower_bound_4p614153/certificate.json`, SHA-256 `5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3`. / 数值测度与 4,391 行父角目录锁定到 `Mira-acc/17squares` 提交 `ac464dd06ded72e2f6eb2c2f3d510b01391c056d`、文件 `certificates/lower_bound_4p614153/certificate.json`，其 SHA-256 为 `5ffb7746fb8aa8d436256710a035235436eecc5e6cfeca3d150dc01b18b801c3`。

The outer side remains $L=4613/1000$, while R038 replaces the original parent side $A=3999/4000$ by / 外框边长保持 $L=4613/1000$，R038 将原父边长 $A=3999/4000$ 替换为：

$$A'=\frac{99974999999}{100000000000}=A-10^{-11}.$$

## 2. Strict containment survives / 严格内含仍成立

For each catalogue row, the selected concentric core had old exact margin $\eta_i=A-B_iF_i>0$, where $F_i$ is the exact endpoint maximum of the relative-angle width factor. / 对每个目录行，选定同心内核原有精确余量 $\eta_i=A-B_iF_i>0$，其中 $F_i$ 是相对角宽度因子在端点上的精确最大值。

The old global minimum margin is / 旧全局最小余量为：

```text
1607618012893827523067050824831683950874799 /
160736546585949244179205669616483275355501572000000000
```

It is approximately `1.000157118614092e-11`, which is strictly larger than `1e-11`. / 其近似值为 `1.000157118614092e-11`，严格大于 `1e-11`。

Replacing $A$ by $A'$ reduces every margin by exactly $10^{-11}$, leaving the exact positive lower bound / 将 $A$ 替换为 $A'$ 会使每个余量恰减少 $10^{-11}$，留下如下精确正下界：

```text
3156837929188515937426608335639966497291 /
2009206832324365552240070870206040941943769650000000000
```

This residual is approximately `1.571186140919352e-15>0`, so every selected core remains strictly inside its parent throughout its entire angle interval. / 该剩余量约为 `1.571186140919352e-15>0`，因此每个选定内核在其完整角区间内仍严格位于父正方形内部。

## 3. The enlarged legal-centre domains are recomputed / 扩大的合法父中心域被重新计算

Decreasing the parent side enlarges the legal parent-centre region, so the containment calculation alone cannot justify the new endpoint. / 缩小父边长会扩大合法父中心域，因此仅靠内含余量计算不足以证明新端点。

The bundled source-distinct scanner rebuilds the complete legal-centre envelope for every one of the 4,391 catalogue rows at $A'$ and scans every reachable event cell. / 随附的不同源码扫描器在 $A'$ 下为全部 4,391 个目录行重新构造完整合法父中心包络，并扫描每个可达事件胞元。

All rational geometry is evaluated with JavaScript `BigInt`; the segment tree stores only integer weights whose accumulated values remain below $2^{53}$, so those integer additions and subtractions are exact as well. / 全部有理几何使用 JavaScript `BigInt` 计算；线段树只存储累加值始终小于 $2^{53}$ 的整数权重，因此这些整数加减同样是精确的。

For the pinned base measure, the full scan gives 3,280 atoms, total mass `16999991644`, global minimum `1000000030`, histogram `2860×1000000030 + 1428×1000000032 + 103×1000000035`, `27918671` centre slabs, and zero escape rows. / 对锁定的基础测度，完整扫描得到 3,280 个原子、总质量 `16999991644`、全局最低 `1000000030`、直方图 `2860×1000000030 + 1428×1000000032 + 103×1000000035`、`27918671` 个中心条带，且逃逸行数为零。

With weight denominator $10^9$, the common charge is therefore $\gamma=1000000030/10^9$ and the total mass is $M=16999991644/10^9$. / 权重分母为 $10^9$，因此共同最低收费为 $\gamma=1000000030/10^9$，总质量为 $M=16999991644/10^9$。

The exact counting gap is / 精确计数余量为：

$$17\cdot1000000030-16999991644=8866>0.$$

## 4. Counting contradiction / 计数矛盾

For any hypothetical packing of seventeen pairwise interior-disjoint $A'$-squares in the $L$-square, fold each parent angle by square symmetries into the certified range, choose the catalogue core, and undo the symmetry. / 对任意假设存在的十七个内部两两不交的 $A'$ 正方形在 $L$ 正方形中的装填，可利用正方形对称将每个父方块角度折叠到已验证范围，选择目录内核后再逆变换。

Each chosen closed core lies strictly inside its parent, so the chosen cores are pairwise disjoint and all charge the same fixed nonnegative measure. / 每个选定闭内核都严格位于其父方块内部，因此这些内核两两不交，并共同使用同一固定非负测度收费。

They would imply $17\gamma\le M$, contradicting the positive gap `8866/10^9`. / 这将推出 $17\gamma\le M$，与正余量 `8866/10^9` 矛盾。

Therefore seventeen $A'$-squares cannot fit in an $L$-square. / 因而十七个边长为 $A'$ 的正方形不能装入边长为 $L$ 的正方形。

Scaling by $1/A'$ excludes seventeen unit squares at side $L/A'$. / 按比例 $1/A'$ 缩放后，排除了容器边长 $L/A'$ 对十七个单位正方形的可行性。

The feasible-configuration space is compact under bounded centres and angles and the non-overlap/containment constraints are closed, so the infimum is attained; excluding the endpoint therefore gives the strict inequality $s(17)>L/A'$. / 在中心与角度有界时，可行构型空间为紧集，且不重叠与包含约束为闭约束，因此下确界可取得；排除端点便得到严格不等式 $s(17)>L/A'$。

## 5. Augmented-orbit control / 增广轨道对照

Adding the D4 orbit `[64477,68039,1]` produces 3,288 atoms, minimum `1000000032`, mass `16999991652`, surplus `8892`, and zero escape rows at the same parent side. / 加入 D4 轨道 `[64477,68039,1]` 后，在同一父边长上得到 3,288 个原子、最低 `1000000032`、总质量 `16999991652`、余量 `8892`，且逃逸行数为零。

Because the base measure already proves the endpoint, this augmented result is a control and not a necessary premise of the R038 theorem. / 由于基础测度已经证明该端点，这个增广结果只是对照，而不是 R038 定理的必要前提。

## 6. Assurance boundary / 可信边界

The exact scan recorded here was executed against the SHA-pinned upstream certificate, and the public scripts permit a cold replay when identical source bytes are supplied. / 此处登记的精确扫描针对 SHA 锁定的上游证书执行；只要提供相同源字节，公开脚本即可进行冷启动复演。

The upstream certificate bytes and Mira's C++ implementation are not redistributed here, and the modified Mira tree/direct backends are not claimed as completed R038 cross-checks. / 本目录不重新分发上游证书字节或 Mira 的 C++ 实现，也不宣称已完成修改后 Mira tree/direct 后端的 R038 交叉复验。

Exact program replay does not by itself constitute external peer review, proof-assistant formalization, global optimality, or priority verification. / 精确程序复演本身不等于外部同行审查、证明助理形式化、全局最优证明或首发核验。
