#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo-bakery · 手作烘焙工作室（虚构示例弹夹）——kit 自带的可跑通样例。

这是一个完全虚构的小生意，用来演示 cellcard-v1 的完整写法：
authored 叶（带证据句+置信）、空白立格、命门低分写 A段 o.auto（va 取叶坑）。
跑通：python3 ops/card_triangle_scorer.py --map demo-bakery --check
     python3 build/build_maps.py --map demo-bakery
"""

MAP = {
  'map_id': 'demo-bakery', 'title': '手作烘焙工作室 · 战略地图（虚构示例）',
  'kind': 'CBM', 'ring': 3, 'role': 'Direct·示例', 'layout': 'single',
  'href': 'map-demo-bakery.html', 'grid': '3域×3层·9格', 'as_of': '2026-01-01',
  'blurb': '一家虚构的社区手作烘焙工作室：产品有口碑、获客靠缘分、复购没体系——最大空白是会员经营。',
  'next': ['<b>下一战</b> · 会员复购判据从零到 v0（先想透 O，再谈自动化）'],
}

LAYERS = [
  ['direct', 'Direct 定向', '关键判断（靠人脑的决策点）'],
  ['control', 'Control 管控', '管理保障（确保质量的检查点）'],
  ['execute', 'Execute 执行', '自动化流水（可规模化的动作）'],
]

DOMAINS = [
  ['prod', '产品与工艺', 'Product & Craft', 'partial', 2, 'engineering', '把手作面包做成可复制的品质'],
  ['grow', '获客增长', 'Growth', 'partial', 1, 'growth', '把路过的人变成第一次下单的客人'],
  ['member', '会员经营', 'Membership', 'gap', 0, 'client', '把一次性客人变成复购会员（整域空白）'],
]

CELLS = [
  {
    'cell_id': 'demo-bakery.prod.direct.1', 'domain': 'prod', 'layer': 'direct',
    'name': '招牌品判断（做什么不做什么）',
    'flat': {'o': 'L4', 's': 'B', 'a': 'A1', 'v': 5, 'status': 'operating', 'gap': False,
             'delegates': ['每周品测会SOP'], 'reuse': '三款招牌+两款季节限定，其余一律不做'},
    'sourcing': '一手·经营记录', 'verified': '2026-01-01',
    'assets': [{'t': '品测会记录表', 'href': '', 'k': 'doc', 'sub': '每周一次·打分维度4项'}],
    'proof': [{'name': '招牌品复购率', 'kind': 'data', 'href': '',
               'num': '碱水包复购 38%（近90天·店内POS口径）', 'date': '2026-01-01', 'src': 'POS 导出'},
              {'name': '砍品记录', 'kind': 'doc', 'href': '', 'num': '12款候选砍到3款招牌',
               'date': '2025-12', 'src': '品测会记录表'}],
    'loop': {'collect': 'manual', 'process': 'manual', 'execute': 'manual', 'distribute': 'none'},
    'hint': '新品先过品测会，不过不上架', 'cand': '',
    'osa': {
      'O': {'stmt': '目标=用3款招牌品建立"这家店=碱水包"的心智，而不是什么都卖',
            'ipo': {'i': {'zhen': {'score': 4, 'ev': 'POS 一手数据：碱水包复购 38%（近90天）', 'conf': '🟢'}},
                    'p': {'level': {'score': 4, 'ev': '从12款候选对比砍到3款——有候选集对比的洞察', 'conf': '🟡'}}}},
      'S': {'stmt': '策略=少而精：产能全部押给已验证复购的品'},
      'A': {'stmt': '行动=每周品测会 SOP，新品不过会不上架',
            'ipo': {'o': {'auto': {'score': 2, 'ev': '品测会全靠人跑，记录靠手抄——A1 如实', 'conf': '🟡'}}}},
    },
    'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': 'demo-bakery.prod.control.1', 'domain': 'prod', 'layer': 'control',
    'name': '出品一致性门',
    'flat': {'o': 'L3', 's': 'C', 'a': 'A0', 'v': 4, 'status': 'draft', 'gap': False,
             'delegates': [], 'reuse': '发酵时长/含水量两项抽检，未成文'},
    'sourcing': '构想中', 'verified': '2026-01-01', 'assets': [], 'proof': [],
    'loop': {'collect': 'manual', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '把老板手感变成可检查的两项数字门', 'osa': None,
    'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': 'demo-bakery.prod.execute.1', 'domain': 'prod', 'layer': 'execute',
    'name': '备料排产流水',
    'flat': {'o': 'L3', 's': 'B', 'a': 'A1', 'v': 4, 'status': 'operating', 'gap': False,
             'delegates': ['排产表模板'], 'reuse': '按周销量排产，损耗率手工记'},
    'sourcing': '一手·经营记录', 'verified': '2026-01-01',
    'assets': [{'t': '排产表', 'href': '', 'k': 'doc', 'sub': '周表·含损耗列'}],
    'proof': [{'name': '损耗率', 'kind': 'data', 'href': '', 'num': '周均损耗 7%（12月四周）',
               'date': '2026-01-01', 'src': '排产表'}],
    'loop': {'collect': 'manual', 'process': 'manual', 'execute': 'manual', 'distribute': 'none'},
    'hint': '', 'cand': '', 'osa': None, 'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': 'demo-bakery.grow.direct.1', 'domain': 'grow', 'layer': 'direct',
    'name': '获客渠道判断',
    'flat': {'o': 'L3', 's': 'C', 'a': 'A0', 'v': 4, 'status': 'draft', 'gap': False,
             'delegates': [], 'reuse': '目前全靠社区口碑+路过，未做对比判断'},
    'sourcing': '观察', 'verified': '2026-01-01', 'assets': [],
    'proof': [{'name': '客源构成（口头盘点）', 'kind': 'doc', 'href': '',
               'num': '约七成熟客带新（店主口述，未系统记录）', 'date': '2026-01-01', 'src': '店主访谈'}],
    'loop': {'collect': 'manual', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '先记录客源渠道两周，再谈选主战场（没数据不拍板）', 'osa': None,
    'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': 'demo-bakery.grow.control.1', 'domain': 'grow', 'layer': 'control',
    'name': '内容质量门（社区群/朋友圈）',
    'flat': {'o': 'L2', 's': 'C', 'a': 'A0', 'v': 3, 'status': 'concept', 'gap': False,
             'delegates': [], 'reuse': '发什么全凭当天心情'},
    'sourcing': '构想中', 'verified': '2026-01-01', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '定一个发图三要素 checklist（成品/过程/人）', 'osa': None,
    'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': 'demo-bakery.grow.execute.1', 'domain': 'grow', 'layer': 'execute',
    'name': '出炉即发流水',
    'flat': {'o': 'L2', 's': 'C', 'a': 'A1', 'v': 3, 'status': 'operating', 'gap': False,
             'delegates': ['出炉拍照提醒'], 'reuse': '每炉出炉拍一张发社区群'},
    'sourcing': '一手', 'verified': '2026-01-01',
    'assets': [{'t': '出炉提醒闹钟', 'href': '', 'k': 'doc', 'sub': '手机闹钟·每炉'}],
    'proof': [{'name': '群内下单转化（估）', 'kind': 'data', 'href': '',
               'num': '出炉照发群后 1 小时内平均 5 单（店主手记两周）', 'date': '2026-01-01', 'src': '店主手记'}],
    'loop': {'collect': 'manual', 'process': 'manual', 'execute': 'manual', 'distribute': 'manual'},
    'hint': '', 'cand': '', 'osa': None, 'gates_authored': None, 'gold_attest': None,
  },
  # ── 会员经营：整域空白立格（示范"盲区不静默"）──
  {
    'cell_id': 'demo-bakery.member.direct.1', 'domain': 'member', 'layer': 'direct',
    'name': '会员复购判据（空白立格）',
    'flat': {'o': 'L1', 's': 'C', 'a': 'A0', 'v': 5, 'status': 'concept', 'gap': True,
             'delegates': [], 'reuse': '谁是会员、多久没来算流失——全在店主脑子里'},
    'sourcing': '空白立格', 'verified': '2026-01-01', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '先答五问①：POS 里有没有会员字段？有就先导出看复购分布',
    'osa': None, 'gates_authored': None, 'gold_attest': None,
    'next_battle': '会员复购判据 v0——全图价值最高的空白（v=5）',
  },
  {
    'cell_id': 'demo-bakery.member.control.1', 'domain': 'member', 'layer': 'control',
    'name': '流失预警门（空白立格）',
    'flat': {'o': 'L1', 's': 'C', 'a': 'A0', 'v': 4, 'status': 'concept', 'gap': True,
             'delegates': [], 'reuse': ''},
    'sourcing': '空白立格', 'verified': '2026-01-01', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '判据(direct)立了才有门可设——不跳层', 'osa': None,
    'gates_authored': None, 'gold_attest': None,
  },
  {
    'cell_id': 'demo-bakery.member.execute.1', 'domain': 'member', 'layer': 'execute',
    'name': '会员触达流水（空白立格）',
    'flat': {'o': 'L1', 's': 'C', 'a': 'A0', 'v': 4, 'status': 'concept', 'gap': True,
             'delegates': [], 'reuse': ''},
    'sourcing': '空白立格', 'verified': '2026-01-01', 'assets': [], 'proof': [],
    'loop': {'collect': 'none', 'process': 'none', 'execute': 'none', 'distribute': 'none'},
    'hint': '', 'cand': '', 'osa': None, 'gates_authored': None, 'gold_attest': None,
  },
]


def selfcheck():
    ids = [c['cell_id'] for c in CELLS]
    assert len(ids) == len(set(ids)) == 9
    dom_ids = {d[0] for d in DOMAINS}
    cov = {}
    for c in CELLS:
        assert c['domain'] in dom_ids
        cov.setdefault(c['domain'], set()).add(c['layer'])
    for d in dom_ids:
        assert cov[d] == {'direct', 'control', 'execute'}
    return True


if __name__ == '__main__':
    selfcheck()
    print(f'demo-bakery 自检通过: 9格/3域, 空白格 {sum(1 for c in CELLS if c["flat"]["gap"])}')
