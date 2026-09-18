# M12｜T-019 source-faithful 原证书与固定缩放重放

日期：2026-09-17  
锁定提交：`035d84c655b4047bc9986c9a3db5106780d92f77`

## 结果

原证书和固定 `λ=1000001/1000000` 缩放证书均由锁定 source verifier 单工通过全部五项条件：

| 项目 | source | scaled |
|---|---:|---:|
| 外容器边长 | `459/100` | `459000459/100000000` |
| 探针边长 | `9977/10000` | `9977009977/10000000000` |
| 原子数 | 1184 | 1184 |
| 方向数 | 181 | 181 |
| 总质量 | `423327/25000` | `423327/25000` |
| 全局最小覆盖 | `200009/200000` | `200009/200000` |
| 最坏方向标签 | `0` | `0` |
| accepted | true | true |
| wall | 38.8492 s | 40.9646 s |
| CPU | 38.7813 s | 40.7500 s |

两份逐方向 `(label, minimum)` tuple 精确相同，无 mismatch。181 个方向中，113 个 minimum 为 `200009/200000`，68 个为 `50003/50000`。比较文件：`results/DIRECTIONS_COMPARISON.jsonl`，SHA-256 `F639E8464FEB88C86B1F051018D5B72156295D604D98583264842F663B096BE1`。

这为固定缩放实例提供了 source-faithful 计算证据；正式全局下界仍等待 T0 独立 sweep 与 T2 审查汇合后登记。本报告不主张 dilation 方法新颖。

## 五条件结果

两对象均通过：

1. 1184 个原子关于各自容器 D4 闭合；
2. 总质量 `423327/25000<17`；
3. 最终 half-tangent `207107/500000`，exact arc slack `309449/250000000000>0`；
4. source：`B(1+D)=899996306539/900000000000<1`；scaled：`B'(1+D)=899997206535306539/900000000000000000<1`；
5. 181 方向 exact sweep 的 least cell mass 均为 `200009/200000>1`。

scaled 的 Condition 4 余量是

`2793464693461/900000000000000000>0`，

因此本固定 λ 使用原 verifier 的较强粗条件即可，不依赖 T-022 的 sharpened endpoint 条件。

## 来源与环境

M12 新获取 8 个同 commit 文件，共 204,883 bytes（0.195 MiB），包括 `certificate.py`、`model.py`、`sweep.py`、`workers.py`、package init、`pyproject.toml` 和 `uv.lock`；逐项哈希见 `NETWORK_LOG.jsonl`。证书原字节 SHA-256 为 `461cb731917bdaf7a58f54be651ca2c782bc519790d79d0fe4941c24fdd4c652`。

执行环境：

- Python 3.12.13；
- NumPy 2.5.3，来自工作区 `.deps/m2/site-packages`；
- `workers=1`；OMP/OpenBLAS/MKL thread 环境均为 1；
- source 项目声明 Python `>=3.14,<3.15`，所以本次版本偏差已显式记录。

source 根 `sqpack/__init__.py` 会导入无关且未下载的模块；harness 用 namespace package 绕过该聚合入口，锁定 fractional 模块正文不变。

## 唯一兼容修正与保留失败

原冻结 harness 首次 source 运行在 0 个方向处失败：Python 3.12 没有源码调用的 `os.process_cpu_count()`。没有方向结果或结果文件产生，scaled 当时未启动。

经 T0 明确授权，单独 wrapper 仅在 API 缺失时设置

`os.process_cpu_count=os.cpu_count`。

本次显式 `workers=1`；该 API 只进入 worker 数量的 `min`，最终仍为 1，不参与方向、Fraction 几何、权重或网格运算。没有第二个 shim。详见 `COMPATIBILITY_ADDENDUM.md`。

PeakWorkingSet 的 Windows API 查询返回 null，故实际 RSS 为 unknown；不以源码估算冒充实测。源码单 worker dense grid 估算为 44,935,200 bytes（42.85 MiB）。结果文件合计约 179 KB，远低于 200 MB。

## 结果绑定

- `results/source_result.json`：SHA-256 `4AD6D4FFF965E014A1ABA2947EE404EB0987FCA2606A7125A58286CF8971E3E0`。
- `results/scaled_result.json`：SHA-256 `D0725160831F743E967083054DAC76A5D49CE01577D32404C055E0F8662AEE02`。
- `results/scaled_certificate.json`：SHA-256 `6979561EB5137270F7BAABC782CAFC0580F3483A9BFCDF47FEF427484285980C`。
- `results/COMPARISON.json`：SHA-256 `F45AD7EF4131198621EA76E2982B3DB58032DA83921C86B8DFFFCA4454FCC347`。
- frozen harness：`run_replay.py` SHA-256 `26ED7A0B2B26BA8E5B144E73A8008E716F9F259AFAA5AAADB48F46D609539A7B`。
- 唯一 compatibility wrapper：SHA-256 `9067FCE2E22C695D288689A61C5EC2C8B4E17C3A5D442944064ECAD81812201C`。

## 主张边界

- 本次是 source-faithful 固定实例重放，不是独立算法验证；T0 的独立 sweep 是另一条证据线。
- 不声称 `4.59000459` 是外部首次、论文新方法或已完成正式登记的新界。
- 不搜索 λ、不触碰原子/方向网、不运行并行、不用 tolerance。
- 待 T2 比较两套逐方向结果、审查共同缩放证明和环境 shim 后，才决定是否把条件稿升级为正式全局下界。
