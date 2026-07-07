#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__MAP_ID__ · CBM 弹夹模板（cellcard-v1）——复制本目录即开一张新战略地图。

═══ 快速开始（弹夹三命令）═══════════════════════════════════════════
  1. python3 build/build_maps.py --new <你的map_id>     # 已为你复制好本模板
  2. 填五问 → 改本文件（见下）→ python3 data/maps/<id>/map.py 自检
  3. python3 ops/card_triangle_scorer.py --map <id> --check   # 评分门
     python3 build/build_maps.py --map <id>                    # 出图 site/map-<id>.html

═══ 五问 intake（动笔前先答，答案决定弹夹形状）═══════════════════════
  ①脊：数据在哪、怎么拿？→ 有运行时数据脊则配 live 绑定；没有就全 authored（诚实标🟡）。
  ②实体：这盘生意的 MECE 域切分（5-7 域为宜）× Direct/Control/Execute 三层。
  ③判断：每格 O 目标/S 策略/A 行动 各是什么判断？证据句在哪？
  ④视图：谁看这张图？（single 五段式默认够用）
  ⑤诚实：缺数据的格显示什么？→ 空白立格 gap=True + cand，禁假绿。

═══ 评分机制（你只管写判断，分数由打分器统一算）══════════════════════
  · flat 三轴（o 信息层级/s 段位/a 自动化）公式降解出 21 叶三五三，全⚪；
  · 你写的 osa authored 叶逐叶覆盖公式（必须带非空 ev + conf 🟢/🟡）；
  · 想=O段p.level，自=A段o.auto，va=min(想,自)——无 gold_attest 封顶 4（无金卡不虚报）。

═══ 三条前人用血换的纪律 ═══════════════════════════════════════════
  ⚠ va 取叶坑：命门格的低分判断必须写在 osa.A.ipo.o.auto（authored 低分叶）——
    只写 O/S 段不会拉低 va（先行弹夹 的 reflux 格曾因此虚高 4→修正 2）。
  ⚠ proof ≥2 条/格（authoring 纪律）；conf=🟢 必须可回溯（该格要有 proof/assets 锚点，评分门会查）。
  ⚠ 数字必带口径+as_of；绑 live 的格 authored ev 禁写"日更在线"式焊死句（写节奏+「实况见 live 探针」）。
"""

MAP = {
  'map_id': '__MAP_ID__',
  'title': '__MAP_ID__ · 战略地图',      # 图名（门内展示）
  'kind': 'CBM', 'ring': 3,              # 环位：0内核/1自营标杆/2接管实例/3学员·复制场
  'role': 'Direct·能力/战略图',
  'layout': 'single',                     # single=五段式标杆单图（portal 仅内核用）
  'href': 'map-__MAP_ID__.html',
  'grid': '2域×3层·6格（示例——照你的域切分改）',
  'as_of': '2026-XX-XX',
  'blurb': '一句话说清这盘生意 + 一句诚实话（最大空白是什么）。',
  # 'deeplink': ['https://…', '→ 已建子系统深链（可删）'],
  'next': ['<b>下一战</b> · 全图最该打的一仗（撬动最大的短板格）'],
}

LAYERS = [
  ['direct', 'Direct 定向', '关键判断（靠人脑的决策点）'],
  ['control', 'Control 管控', '管理保障（确保质量的检查点）'],
  ['execute', 'Execute 执行', '自动化流水（可规模化的动作）'],
]

# (id, 名, 英文, 成熟度 rich|partial|gap|built, 组件数, 治理桥, 一句话)
DOMAINS = [
  ['demo', '示例域', 'Demo Domain', 'partial', 3, 'growth', '把X转化为Y的能力（改成你的域）'],
  ['blank', '空白域', 'Blank Domain', 'gap', 0, 'client', '还没想清楚的域也要显式立出来（盲区是治理信号）'],
]

CELLS = [
  # ── 满 authored 示例格：三段 OSA 各自带 authored 叶 ─────────────────
  {
    'cell_id': '__MAP_ID__.demo.direct.1', 'domain': 'demo', 'layer': 'direct',
    'name': '示例·关键判断格',
    'flat': {
      'o': 'L3',            # 信息层级 L1碎片/L2特征/L3观点/L4洞察/L5全局最优
      's': 'B',             # 段位 C/B/A/S
      'a': 'A1',            # 自动化 A0全人工/A1流程化/A2半自动/A3智能化
      'v': 5,               # 价值权重 1-5
      'status': 'draft',    # operating|stable|draft|concept（status 只在 weekly 升级）
      'gap': False,
      'delegates': ['某个真实skill或脚本'],   # 真委派才写；没有写 [] （递进门 fail 是诚实结果）
      'reuse': '这格能复用的一句话打法',
    },
    'sourcing': '一手·XX来源', 'verified': '2026-XX-XX',
    'assets': [{'t': '资产名', 'href': '', 'k': 'doc', 'sub': '在哪/什么口径'}],
    'proof': [
      {'name': '证据一（真跑出的结果）', 'kind': 'data', 'href': '',
       'num': '数字必带口径+as_of', 'date': '2026-XX-XX', 'src': '出处可回溯'},
      {'name': '证据二', 'kind': 'doc', 'href': '', 'num': '', 'date': '2026-XX-XX', 'src': '…'},
    ],
    'loop': {'collect': 'manual', 'process': 'manual', 'execute': 'none', 'distribute': 'none'},
    'hint': '复用指引：别人怎么调用这格能力',
    'cand': '',
    'osa': {
      'O': {'stmt': 'O 目标判断句（≥3 候选对比后的全局最优）',
            'ipo': {'i': {'zhen': {'score': 4, 'ev': '一手证据句·带口径', 'conf': '🟢'}},
                    'p': {'level': {'score': 3, 'ev': '想透到观点层的证据', 'conf': '🟡'}}}},
      'S': {'stmt': 'S 策略判断句（多元思维模型收敛后的稳定打法）'},
      'A': {'stmt': 'A 行动判断句（SMART·agent 可接手）',
            'ipo': {'o': {'auto': {'score': 2, 'ev': '⚠命门低分写这里才拉低 va（va 取叶坑）', 'conf': '🟡'}}}},
    },
    'gates_authored': None,   # 四门人裁覆盖（一般留 None 走公式×规则双族取严）
    'gold_attest': None,      # 金卡人证：weekly 签发才允许 va=5
    # 'live': [{'src': 'your-source', 'probe': 'freshness', 'target': 'osa.A.ipo.o.closure'}],
    #   ↑ 有数据脊才配；live 只升置信不升分，快照>7天自动降🟡
    'next_battle': '这格的下一战（可选）',
  },
  # ── 其余格：最小可过门形态 ───────────────────────────────────────
  {
    'cell_id': '__MAP_ID__.demo.control.1', 'domain': 'demo', 'layer': 'control',
    'name': '示例·质量门格',
    'flat': {'o': 'L2', 's': 'C', 'a': 'A0', 'v': 4, 'status': 'concept', 'gap': False,
             'delegates': [], 'reuse': '还没建的门先诚实写 concept'},
    'sourcing': '构想', 'verified': '2026-XX-XX', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '', 'osa': None, 'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': '__MAP_ID__.demo.execute.1', 'domain': 'demo', 'layer': 'execute',
    'name': '示例·流水格',
    'flat': {'o': 'L2', 's': 'C', 'a': 'A1', 'v': 4, 'status': 'draft', 'gap': False,
             'delegates': [], 'reuse': ''},
    'sourcing': '构想', 'verified': '2026-XX-XX', 'assets': [], 'proof': [],
    'loop': {'collect': 'manual', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '', 'osa': None, 'gates_authored': None, 'gold_attest': None,
  },
  # ── 空白立格示例：盲区不静默 ─────────────────────────────────────
  {
    'cell_id': '__MAP_ID__.blank.direct.1', 'domain': 'blank', 'layer': 'direct',
    'name': '空白域·定向（空白立格）',
    'flat': {'o': 'L1', 's': 'C', 'a': 'A0', 'v': 4, 'status': 'concept', 'gap': True,
             'delegates': [], 'reuse': '显式立格：这里缺什么判断'},
    'sourcing': '空白立格', 'verified': '2026-XX-XX', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '候选补法：先答五问的哪一问？', 'osa': None,
    'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': '__MAP_ID__.blank.control.1', 'domain': 'blank', 'layer': 'control',
    'name': '空白域·管控（空白立格）',
    'flat': {'o': 'L1', 's': 'C', 'a': 'A0', 'v': 3, 'status': 'concept', 'gap': True,
             'delegates': [], 'reuse': ''},
    'sourcing': '空白立格', 'verified': '2026-XX-XX', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '随域判断成型一并立门', 'osa': None,
    'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': '__MAP_ID__.blank.execute.1', 'domain': 'blank', 'layer': 'execute',
    'name': '空白域·执行（空白立格）',
    'flat': {'o': 'L1', 's': 'C', 'a': 'A0', 'v': 3, 'status': 'concept', 'gap': True,
             'delegates': [], 'reuse': ''},
    'sourcing': '空白立格', 'verified': '2026-XX-XX', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '判断没立之前不建流水（不跳层）', 'osa': None,
    'gates_authored': None, 'gold_attest': None,
  },
]


def selfcheck():
    ids = [c['cell_id'] for c in CELLS]
    assert len(ids) == len(set(ids)), 'cell_id 重复'
    dom_ids = {d[0] for d in DOMAINS}
    lay_ids = {l[0] for l in LAYERS}
    cov = {}
    for c in CELLS:
        assert c['domain'] in dom_ids and c['layer'] in lay_ids, c['cell_id']
        cov.setdefault(c['domain'], set()).add(c['layer'])
        f = c['flat']
        assert f['o'] in ('L1', 'L2', 'L3', 'L4', 'L5') and f['s'] in 'CBAS' and f['a'] in ('A0', 'A1', 'A2', 'A3')
        assert f['status'] in ('operating', 'stable', 'draft', 'concept')
        if c.get('osa'):
            for seg in ('O', 'S', 'A'):
                assert seg in c['osa'], f"{c['cell_id']} osa 缺 {seg} 段"
    for d in dom_ids:
        assert cov[d] == lay_ids, f'{d} 域层覆盖不全（每域三层都要立格，空白也立）'
    return True


if __name__ == '__main__':
    selfcheck()
    print(f'__MAP_ID__ map.py 自检通过: {len(CELLS)}格/{len(DOMAINS)}域, '
          f'空白格 {sum(1 for c in CELLS if c["flat"]["gap"])}')
