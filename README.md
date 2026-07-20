# CBM-OSA-IPO Map Kit · 战略地图-原子卡片工具箱

把任意 IP / 业务 / 领域构建成一张可打分、可验收、带诚实纪律的**战略地图-原子卡片**。
本仓同时承载唯一正式机器合同
`yuanli-osa-card/v2` 与评分包 `yuanli-osa-card==2.0.0`。

```
能力栈：IPO 信息力 → OSA 策略力 → CBM 统筹力
生产链：IPO 信息引擎 → OSA 决策合同 → CBM 能力棋盘

IPO/I  全 / 真·一手 / 细
   ↓
IPO/P  碎片 → 特征 → 观点 → 洞察 → 全局最优
   ↓
IPO/O  闭环 → 自动化 → 智能化
   ↺    隐藏回流：现实反馈成为下一轮 Input
```

一张 OSA 卡只拥有一个统一 `information_engine`。O 是候选比较后的全局最优目标，S 是实现 O
的策略及科学实验，A 是 SMART 行动合同；三者引用同一信息底座，不复制平行 I/P/O 对象。
完整标准见 [methodology/unified-information-engine-v4.md](methodology/unified-information-engine-v4.md)，
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
- 统一 IPO 对象：`information_engine`；IPO 与 OSA 分开计算、联合验收。
- 迁移器：`migrate-v1` 保留 `legacy_v1.legacy_recursive_ipo`，把 `Situation` 仅迁到
  `context.situation`，旧分数一律 `unassessed`。
- SABC：C 想法 → B 技术可行 → A 真实价值 → S 至少三可比较增长周期。
- A0–A3 独立于实验阶段；A3 必须有真实 `changed_rule` 回执与 Human Gate。
- 引擎只计算 `supported_ceiling`。只有 production 边界、当前人工批准回执与足够证据同时存在，`effective` 才可能生效。

`cbm-osa-ipo-scored-v1` 已完成两个可计数 weekly 周期后退出主动评分。历史实现和旧叶片仍由
Git 历史及 `legacy_v1` 数据保留，但 `ops/card_triangle_scorer.py` 现在是 fail-closed 退休标记，
不会再生成分数。任何新建、更新或晋级只能调用上面的 `yuanli-osa-card/v2` 引擎。

## Legacy v1 历史投影

历史五段式页面和旧叶片只读保留，不再提供重评分或新建弹夹入口。运行旧 CLI 会返回结构化
`status=retired` 并以非零状态退出。需要核验历史时应读取已经签名的快照或指定 Git 提交，
不得重新计算并覆盖旧证据；新卡必须通过 `yuanli-osa-card validate/score` 使用统一信息底座。

## Legacy v1 历史纪律（只读说明，不再执行评分）

以下规则解释既有 v1 快照为何形成当前结果，只用于审计历史，不是可继续调用的评分门：

- **公式默认 ⚪ / authored 覆盖**：你没写判断的叶子由 flat 三轴公式降解（全标 ⚪ 非实证）；
  你写的 authored 叶必须带非空证据句 + 置信 🟢/🟡——公式冒充真据 = 假绿，`--check` 直接拒。
- **无金卡不虚报**：va = min(想, 自)，没有 weekly 人工签发的 `gold_attest`，封顶 4 分。
- **棘轮**：图的 min 分只升不降（`baseline.json`），确属真实退化须人工批准降基线。
- **空白立格**：盲区显式立格标 candidates——盲区是治理信号，不是遮羞布。
- **旧叶片只读**：历史 `osa.<O|S|A>.ipo` 只能留在 legacy 投影，不得进入新卡或影响 v2 分数。

## 仓库结构

```
methodology/   统一信息底座正典 + 7 步配方；递归 v3 仅保存历史血缘
src/yuanli_osa_card/  v2 正式合同、唯一评分引擎、迁移器与 CLI
ops/           v1 退休标记与历史装载源码（不得用于主动评分）
build/         legacy v1 页面源码，只用于理解历史投影
data/maps/     legacy v1 虚构示例与模板，只读保留
examples/      脱敏 v2 样板卡（无虚构结果、无绿灯）
deploy.example.sh   通用部署示例（换成你自己的静态托管）
```

## 历史访问门

历史页面源码带 sha256 客户端访问门。**默认 HASH 是占位符 `CHANGE_ME_SHA256_OF_YOUR_PASSPHRASE`**；
本仓不再提供旧页面的主动构建或发布流程。若审计历史实现，可在隔离环境生成测试哈希：

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
