# CBM-OSA-IPO Map Kit · 战略地图-原子卡片工具箱

把任意 IP / 业务 / 领域，用「**一个原子 · 三级递归**」的方法论，构建成一张可打分、可验收、
带诚实纪律的**战略地图-原子卡片**。本仓同时承载唯一正式机器合同
`yuanli-osa-card/v2` 与评分包 `yuanli-osa-card==2.0.0`。

```
IPO   一次三五三：采(全/真·一手/细) → 工(碎片→特征→观点→洞察→全局最优) → 表(闭环/自动化/智能化)
 │ ×3（对 O、S、A 各跑一次）
OSA   把一个「点」想透 = O的IPO + S的IPO + A的IPO          【一格 = 一张原子卡】
 │ ×网格（领域 MECE × Direct/Control/Execute 三责任层）
CBM   把一个「领域」铺全 = 一格格 OSA 拼成的棋盘             【一张战略地图】
```

其中 O 是候选比较后的全局最优目标，S 是实现 O 的策略及科学实验，A 是 SMART 行动合同；
O/S/A 分别运行 IPO 证据回路。同一信息引擎，递归三层。完整标准见 [methodology/recursion-v3.md](methodology/recursion-v3.md)，
从零构建配方见 [methodology/7-steps.md](methodology/7-steps.md)。

## OSA v2 合同与唯一评分引擎

```bash
python3 -m pip install -e .
yuanli-osa-card validate examples/xiaoyuan-public-content-experiment.v2.json
yuanli-osa-card score examples/xiaoyuan-public-content-experiment.v2.json
yuanli-osa-card schema-hash
```

- 正式 Schema：`src/yuanli_osa_card/schema/yuanli-osa-card-v2.schema.json`。
- 正式引擎：`src/yuanli_osa_card/engine.py`；消费者必须锁定 Git commit 与 Schema SHA-256。
- 迁移器：`migrate-v1` 保留 `legacy_v1`，把 `Situation` 仅迁到 `context.situation`，旧分数一律 `unassessed`。
- SABC：C 想法 → B 技术可行 → A 真实价值 → S 至少三可比较增长周期。
- A0–A3 独立于实验阶段；A3 必须有真实 `changed_rule` 回执与 Human Gate。
- 引擎只计算 `supported_ceiling`。只有 production 边界、当前人工批准回执与足够证据同时存在，`effective` 才可能生效。

`ops/card_triangle_scorer.py` 暂作为 `cbm-osa-ipo-scored-v1` 双读兼容入口，供旧地图在两个
weekly 周期内读取历史；它不是 v2 合同或新晋级的真源，不得再产生新消费者。确认旧消费者迁完后退为只读历史投影。

## 快速开始（三命令出图）

```bash
# 0. 先跑自带的虚构示例（手作烘焙工作室，9 格）
python3 ops/card_triangle_scorer.py --map demo-bakery --check   # 评分 + 评分门
python3 build/build_maps.py --map demo-bakery                    # 出图 site/map-demo-bakery.html

# 1. 开你自己的弹夹
python3 build/build_maps.py --new my-business
# 2. 答五问、填 data/maps/my-business/map.py（模板里有 21 叶示例格 + 空白立格 + 纪律注释）
python3 data/maps/my-business/map.py                             # 自检
# 3. 评分门 → 出图
python3 ops/card_triangle_scorer.py --map my-business --check
python3 build/build_maps.py --map my-business
```

出的是一张五段式单页：**SIBLING 同构图 / 黄金三角+指标条 / 域×层棋盘 / 距100分清单 / 下一战**，
每格点开是 OSA 三页签（O的IPO / S的IPO / A的IPO），21 叶逐叶带 分数+置信+证据句。

## 这套东西的脾气（诚实纪律，评分门强制执行）

- **公式默认 ⚪ / authored 覆盖**：你没写判断的叶子由 flat 三轴公式降解（全标 ⚪ 非实证）；
  你写的 authored 叶必须带非空证据句 + 置信 🟢/🟡——公式冒充真据 = 假绿，`--check` 直接拒。
- **无金卡不虚报**：va = min(想, 自)，没有 weekly 人工签发的 `gold_attest`，封顶 4 分。
- **棘轮**：图的 min 分只升不降（`baseline.json`），确属真实退化须人工批准降基线。
- **空白立格**：盲区显式立格标 candidates——盲区是治理信号，不是遮羞布。
- **⚠ va 取叶坑**：命门格的低分判断必须写在 `osa.A.ipo.o.auto`（authored 低分叶），
  只写 O/S 段不会拉低 va——前人踩过，模板注释里有完整说明。

## 仓库结构

```
methodology/   方法论（递归 v3 标准 + 7 步配方）
src/yuanli_osa_card/  v2 正式合同、唯一评分引擎、迁移器与 CLI
ops/           v1 地图兼容装载与 CLI（双读期只读历史）
build/         common.py（页面骨架/门体）· build_maps.py（--new 开弹夹 / --map 出图）
data/maps/     _template/（弹夹模板）· demo-bakery/（虚构示例，可直接跑）
examples/      脱敏 v2 样板卡（无虚构结果、无绿灯）
deploy.example.sh   通用部署示例（换成你自己的静态托管）
```

## 访问门

页面自带 sha256 客户端访问门。**默认 HASH 是占位符 `CHANGE_ME_SHA256_OF_YOUR_PASSPHRASE`**——
上线前生成你自己的口令哈希替换 `build/templates/gate.frag`：

```bash
echo -n '你的口令' | shasum -a 256
```

明文口令永远不要提交进仓库（本仓 CI 的 leak-scan 会扫常见泄漏模式）。

## 血缘与案例

方法论蒸馏自一个私有组织的真实实践：内核组织能力图（10域×3层34格）+ 三张标杆客户图
（经营域 N=1 / 生态标杆 / 内容IP N=2）在同一条产线上运行，弹夹模板经"从零虚构业务出图"
工厂验收。真实案例数据不在本仓（脱敏红线），本仓只含方法论、引擎与虚构示例。

方法论正身与上位标准（私有仓，协作者可见）：`moonstachain/yuanli-strategy-soul`
`docs/YUANLI-STRATEGY-CANON-INDEX.md`——本 kit 是其"公共方法论层"载体；跨域裁决与
双友好验收标准（机器友好/人类友好两把尺）以该正典为准。

## License

MIT
