# CBM-OSA-IPO Map Kit · 战略地图-原子卡片工具箱

把任意 IP / 业务 / 领域，用「**一个原子 · 三级递归**」的方法论，构建成一张可打分、可验收、
带诚实纪律的**战略地图-原子卡片**——并用本仓的打分器与渲染器直接出图。

```
IPO   一次三五三：采(全/真·一手/细) → 工(碎片→特征→观点→洞察→全局最优) → 表(闭环/自动化/智能化)
 │ ×3（对 O、S、A 各跑一次）
OSA   把一个「点」想透 = O的IPO + S的IPO + A的IPO          【一格 = 一张原子卡 = 21 叶三五三】
 │ ×网格（领域 MECE × Direct/Control/Execute 三责任层）
CBM   把一个「领域」铺全 = 一格格 OSA 拼成的棋盘             【一张战略地图】
```

同一信息引擎，递归三层。完整标准见 [methodology/recursion-v3.md](methodology/recursion-v3.md)，
从零构建配方见 [methodology/7-steps.md](methodology/7-steps.md)。

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
ops/           map_loader.py（弹夹契约装载）· card_triangle_scorer.py（唯一评分引擎+评分门）
build/         common.py（页面骨架/门体）· build_maps.py（--new 开弹夹 / --map 出图）
data/maps/     _template/（弹夹模板）· demo-bakery/（虚构示例，可直接跑）
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

## License

MIT
