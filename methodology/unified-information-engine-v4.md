# CBM‑OSA‑IPO · 统一信息底座标准 v4

> 本标准取代“OSA 由三个 IPO 组成”的递归解释。旧解释只保留在历史材料和 v1 兼容投影中，
> 不得驱动 `yuanli-osa-card/v2`。

## 1. 正典关系

```text
IPO · 一套统一信息能力底座

I · 信息采集：全 / 真·一手 / 细
→ P · 信息处理：碎片 → 特征 → 观点 → 洞察 → 全局最优
→ O · 信息输出：闭环 → 自动化 → 智能化
↺ 隐藏回流：输出进入执行，现实反馈成为下一轮 I

能力栈：IPO 信息力 → OSA 策略力 → CBM 统筹力
生产链：IPO 信息引擎 → OSA 决策合同 → CBM 能力棋盘
```

IPO 评价信息工艺，OSA 评价 Objective、Strategy、Action 的决策成熟度，CBM 负责把 OSA 卡
放入能力域 × Direct/Control/Execute 棋盘。三者是正交读数与生产链，不是嵌套的三个平行 IPO。

## 2. 唯一合同

一张 `yuanli-osa-card/v2` 只有一个顶层 `information_engine`：

- `input` 保存来源引用、覆盖维度，以及全、真·一手、细三项证据门。
- `process` 保存连续 L1–L5 加工产物和方法引用；禁止跳层。
- `output` 指向同一张卡的 Objective、Strategies、Actions，并保存闭环、自动化、智能化证据门。
- `feedback` 保存现实结果、下一轮输入和正式纳入时间。它是隐藏回流，不是 IPO 的第四个字母。

O/S/A 只引用统一底座的证据和产物，不拥有各自的 I/P/O 子树。IPO 的 O 是 Output，OSA 的 O
是 Objective；页面和 API 必须使用完整标签，避免混淆。

## 3. OSA 与 Gold

- O：不少于三个候选目标、约束比较、目标模型、基线、指标、目标值与期限。
- S：C 想法 → B 技术可行 → A 真实价值 → S 至少三个可比较、可复制、可归因增长周期。
- A：A0 人工非标 → A1 版本化 SOP → A2 Agent+回执 → A3 AI 自主规划与真实 `changed_rule`。
- Gold：`O=L5 ∧ S=S ∧ A=A3 ∧ information_engine=verified ∧ 当前可信证据 ∧ 人工批准`。

Input 不可信时，OSA 只输出诊断上限，所有 `effective` 保持 `unassessed`。IPO P 的证据层级限制
O 的最高等级；Output 或回流不完整不会伪造修改 SABC/A0–A3，但会阻止 IPO verified 与 Gold。

## 4. 兼容纪律

旧 `osa.<O|S|A>.ipo` 原样进入 `legacy_v1.legacy_recursive_ipo`，只供历史双读。迁移器仅列出
待人工绑定的候选证据引用，不去重、不平均、不继承旧分数，也不自动创建可信新 IPO。
