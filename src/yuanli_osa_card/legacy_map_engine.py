#!/usr/bin/env python3
"""Legacy v1 map-scoring compatibility hosted by the canonical package.

This module preserves historical map rendering during the two-weekly-cycle
dual-read window.  New OSA calibration must use :mod:`yuanli_osa_card.engine`.
Consumers inject their local map loader; they must not copy this implementation.

一个原子（IPO 三五三）× 三级递归（OSA=3×IPO → CBM=网格×OSA）的唯一判断引擎。
所有图（内核/标杆/弹夹）经 ops/map_loader.py 装载后由本器打分；渲染器零评分只读输出。

■ 公式族血缘（沿用 07-05 丢失版命名；数值公式 2026-07-07 自
  data/org_cbm_enriched_recovered.json 34 格全量反推，逐格拟合验证）：
    cell_e  = 4 if proof else 2                       # 究竟·证据代理（34/34 拟合）
    cell_i  = 1 if 无assets else 2+资产种类数(封顶5)    # 完备·采集广度（34/34）
    cell_v  = o 信息层级 L1-5                          # 递进·纵向到底（33/34；唯一偏差
              org.content.execute.4 系当轮 llm-judge 人工压 2，属 authored 覆盖畴，公式不追）
    cell_a  = 4 if delegates else 1                   # 原子·可接手（34/34）
    ipo_i   = cell_i                                  # 旧单IPO三段（34/34）
    ipo_p   = 3 + [loop.process=auto] + [loop.execute=auto]      # （34/34）
    ipo_o   = 1 + loop 四段 auto 计数                  # （34/34）
    gate verdict 阈值 = ≥4 pass / ==3 partial / ≤2 fail
  judgment 规则族（data/org_cbm_judgment_2026-07-07.py，status/delegates/gap 推导）：
    derive_xiang / derive_zi / derive_gates —— 已并入本器（见下）。
  四门终值 = 公式族 与 judgment 族 取更严 verdict，reason 记双源；gates_authored 人裁再覆盖。

■ OSA=3×IPO 公式降解（21 叶/格，全 ⚪；authored 逐叶 deep-merge 覆盖）：
    O段(目标的IPO):  i.quan=cell_i  i.zhen=cell_e  i.xi=min(quan,zhen)
                     p.level=derive_xiang(想)
                     o.closure=闭环基分(运行4/草稿2/概念1)  o.auto=min(closure,derive_zi)  o.intel=1
    S段(策略的IPO):  i.* 同上(同一信息底盘)
                     p.level=s段位(C/B/A/S→2/3/4/5)
                     o.closure=min(p.level,闭环基分)  o.auto=min(closure,derive_zi)  o.intel=1
    A段(行动的IPO):  i.* 同上
                     p.level=ipo_p(拆解到位度)
                     o.closure=闭环基分  o.auto=derive_zi(自)  o.intel=2 if a==A3 else 1
    想=O段p.level  自=A段o.auto  va=min(想,自)，无 gold_attest 封顶 4（无金卡不虚报）。

■ 诚实纪律（--check 硬门，非零退出断部署）：
    authored 叶须非空 ev 且 conf∈{🟢,🟡}（公式冒充真据=假绿）；formula 叶恒⚪；
    🟢 叶所在格须有 proof/assets 锚点；无 gold_attest 则 va≤4；
    棘轮：逐格 va ≥ baseline（分数只升不降，weekly --update-baseline 才许更新）；
    live 证据 >7 天自动降 🟡 并进距100分清单（评分行为，非门失败）。

用法：
  python3 ops/card_triangle_scorer.py --map org-kernel        # 打分 → build/out/org-kernel.scored.json
  python3 ops/card_triangle_scorer.py --all                   # 全部弹夹 + scoreboard.json
  python3 ops/card_triangle_scorer.py --all --check           # 评分门（部署前必过）
  python3 ops/card_triangle_scorer.py --map <id> --update-baseline   # weekly 棘轮更新
"""
import argparse
import copy
import datetime
import json
import os

ROOT = None
OUT_DIR = None
list_maps = None
load_map = None
O_LEVEL = {'L1': 1, 'L2': 2, 'L3': 3, 'L4': 4, 'L5': 5}
S2N = {'C': 2, 'B': 3, 'A': 4, 'S': 5}
A2N = {'A0': 1, 'A1': 2, 'A2': 3, 'A3': 4}
RUNNING = {'operating', 'stable'}
SEV = {'pass': 0, 'partial': 1, 'fail': 2}
GATE_KEYS = ['究竟', '完备', '递进', '原子']
PINYIN = {'究竟': 'jiujing', '完备': 'wanbei', '递进': 'dijin', '原子': 'yuanzi'}
LIVE_MAX_AGE_DAYS = 7


def configure_legacy(root, list_maps_fn, load_map_fn):
    """Bind one consumer's data root and loader to the shared legacy engine."""
    global ROOT, OUT_DIR, list_maps, load_map
    ROOT = os.fspath(root)
    OUT_DIR = os.path.join(ROOT, 'build', 'out')
    list_maps = list_maps_fn
    load_map = load_map_fn


def _require_loader():
    if ROOT is None or OUT_DIR is None or list_maps is None or load_map is None:
        raise RuntimeError('legacy_loader_not_configured')


# ── 公式族（丢失版命名·反推复原）──────────────────────────────
def cell_e(c):
    return 4 if c.get('proof') else 2


def cell_i(c):
    if not c.get('assets'):
        return 1
    kinds = len({a.get('k', '?') for a in c['assets']})
    return min(5, 2 + kinds)


def cell_v(c):
    return O_LEVEL[c['flat']['o']]


def cell_a(c):
    return 4 if c['flat']['delegates'] else 1


def _loop(c):
    lp = c.get('loop') or {}
    return [lp.get(k, 'none') for k in ('collect', 'process', 'execute', 'distribute')]


def ipo_p(c):
    lp = c.get('loop') or {}
    return 3 + (lp.get('process') == 'auto') + (lp.get('execute') == 'auto')


def ipo_o(c):
    return 1 + sum(1 for v in _loop(c) if v == 'auto')


# ── legacy portal adapter compatibility (read-only; not used by score_map) ──
# build_portal/maps_registry and their locked tests still consume the scored-v2
# IPO facade.  The data-spine merge kept those readers but dropped the facade.
# Restore it here without changing the current OSA=3×IPO scoring path below.
def cell_o_axes(c):
    """Conservative O lower bounds: closure, automation, recursive evolution."""
    lp = c.get('loop') or {}
    output_path = (lp.get('execute') in ('manual', 'auto')
                   and lp.get('distribute') in ('manual', 'auto'))
    result_proof = bool(c.get('proof') or c.get('evidence') or c.get('result_receipt'))
    closure = 3 if (output_path and result_proof) else 2 if output_path else 1
    autos = sum(1 for value in lp.values() if value == 'auto')
    automation = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}.get(autos, 5)
    reflow = c.get('reflow') or c.get('feedback') or c.get('evolution')
    recursive_evolution = 3 if (reflow and result_proof) else 2 if reflow else 1
    return {'closure': closure, 'auto': automation, 'intel': recursive_evolution}


def cell_o(c):
    return min(cell_o_axes(c).values())


def _legacy_cell_i(c):
    if c.get('flat') is not None:
        return cell_i(c)
    if not c.get('assets'):
        return 1
    kinds = len({asset.get('kind') for asset in c['assets']})
    has_evidence = bool(c.get('proof') or c.get('evidence') or c.get('score'))
    base = {0: 1, 1: 2, 2: 3, 3: 4}.get(kinds, 4)
    return min(base + (1 if has_evidence else 0), 5)


def _legacy_cell_p(c):
    lp = c.get('loop') or {}
    process_auto = 1 if lp.get('process') == 'auto' else 0
    execute_auto = 1 if lp.get('execute') == 'auto' else 0
    has_depth = bool(c.get('score') or c.get('insight'))
    return min(2 + process_auto + execute_auto + (1 if has_depth else 0), 5)


def _formula_leaf(score):
    return {'score': int(score), 'ev': '', 'conf': '⚪'}


def _authored_leaf(authored, fallback):
    authored = authored or {}
    if authored.get('score') is not None:
        return {'score': int(authored['score']), 'ev': authored.get('ev', ''),
                'conf': authored.get('conf', '🟡')}
    return fallback


def ipo_read(c):
    """Legacy I/P/O facade; an old scalar O is automation only, never closure."""
    authored = c.get('ipo') or {}
    out = {}
    for key, score in (('i', _legacy_cell_i(c)), ('p', _legacy_cell_p(c))):
        out[key] = _authored_leaf(authored.get(key), _formula_leaf(score))

    formula_axes = {key: _formula_leaf(value) for key, value in cell_o_axes(c).items()}
    authored_o = authored.get('o') or {}
    legacy = authored_o.get('score') is not None
    if legacy:
        detail = dict(formula_axes)
        detail['auto'] = _authored_leaf(authored_o, formula_axes['auto'])
    else:
        detail = {
            key: _authored_leaf(authored_o.get(key), formula_axes[key])
            for key in ('closure', 'auto', 'intel')
        }
    confidence_rank = {'⚪': 0, '🟡': 1, '🟢': 2}
    aggregate_confidence = min(
        (leaf.get('conf', '⚪') for leaf in detail.values()),
        key=lambda value: confidence_rank.get(value, 0),
    )
    out['o_detail'] = detail
    out['o'] = {
        'score': min(leaf['score'] for leaf in detail.values()),
        'ev': '；'.join(
            f"{key}={leaf['score']} {leaf.get('ev', '')}".strip()
            for key, leaf in detail.items()
        ),
        'conf': aggregate_confidence,
        'legacy_auto_only': legacy,
    }
    return out


def _legacy_cell_v(c):
    if c.get('flat') is not None:
        return cell_v(c)
    level = str(c.get('o', 'L1'))
    score = int(level[1:]) if level.startswith('L') and level[1:].isdigit() else 1
    has_evidence = bool(c.get('score'))
    has_proof = bool(c.get('proof'))
    return score if (has_evidence and (has_proof or c.get('gap'))) else max(score - 1, 1)


def _legacy_cell_a(c):
    if c.get('flat') is not None:
        return cell_a(c)
    if not c.get('assets'):
        return 1
    return 4 if (c.get('loop') and c.get('reuse_hint')) else 3


def gate_resolve(c):
    """Legacy four-gate facade with authored entries overriding formulas."""
    vertical, atomic, breadth = _legacy_cell_v(c), _legacy_cell_a(c), _legacy_cell_i(c)
    evidence = 4 if ((c.get('proof') or c.get('evidence')) and c.get('assets')) else 2
    defaults = {
        'jiujing': {'verdict': verdict(evidence), 'reason': f'E 证据代理={evidence}（实证/证据锚点 × 资产出处）'},
        'wanbei': {'verdict': verdict(breadth), 'reason': f'I 采集广度代理={breadth}（assets 种类+实证）'},
        'dijin': {'verdict': verdict(vertical), 'reason': f'V 纵向到底={vertical}（cell_v 真源）'},
        'yuanzi': {'verdict': verdict(atomic), 'reason': f'A 原子递进={atomic}（cell_a 真源）'},
    }
    for key, gate in (c.get('gates') or {}).items():
        if key in defaults and gate.get('verdict'):
            defaults[key] = {'verdict': gate['verdict'], 'reason': gate.get('reason', '')}
    return defaults


def finalize_ipo(sidecar, cells_by_id):
    """Lint legacy sidecars; O authored leaves must be a complete triple."""
    real_fields = ('proof', 'loop', 'insight', 'evidence', 'score', 'assets',
                   'reuse_hint', 'result_receipt', 'reflow', 'feedback', 'evolution')
    for entry in sidecar.get('cells', []):
        cell_id = entry['cell_id']
        cell = cells_by_id.get(cell_id, {})
        authored = entry.get('ipo') or {}
        for key in ('i', 'p'):
            axis = authored.get(key)
            if not axis:
                continue
            assert axis.get('ev'), f'ipo lint: {cell_id}.{key} 有条目但 ev 空（无证据句不收）'
            if axis.get('conf') == '🟢':
                assert any(cell.get(field) for field in real_fields), \
                    f'ipo lint: {cell_id}.{key} 标🟢 但该格无真实字段可引（禁上抬置信）'

        authored_o = authored.get('o') or {}
        if authored_o.get('score') is not None:
            assert authored_o.get('ev'), f'ipo lint: {cell_id}.o legacy 条目 ev 空'
        elif authored_o:
            assert set(authored_o) == {'closure', 'auto', 'intel'}, \
                f'ipo lint: {cell_id}.o 必须 closure/auto/intel 三叶成组'
            for key in ('closure', 'auto', 'intel'):
                axis = authored_o[key]
                assert axis.get('ev'), f'ipo lint: {cell_id}.o.{key} ev 空'
                assert axis.get('conf') in ('🟢', '🟡'), \
                    f'ipo lint: {cell_id}.o.{key} authored 置信须🟢/🟡'
                if axis.get('conf') == '🟢':
                    assert any(cell.get(field) for field in real_fields), \
                        f'ipo lint: {cell_id}.o.{key} 标🟢但无真实字段'

        for gate_key, gate in (entry.get('gates') or {}).items():
            assert gate.get('reason'), f'ipo lint: {cell_id}.gate.{gate_key} verdict 有但 reason 空'
    return True


def verdict(n):
    return 'pass' if n >= 4 else 'partial' if n == 3 else 'fail'


# ── judgment 规则族（org_cbm_judgment_2026-07-07 并入）───────────
def derive_xiang(c):
    f = c['flat']
    x = O_LEVEL[f['o']]
    if f['status'] == 'concept':
        return min(x, 2)
    if f['status'] == 'draft':
        return min(x, 3)
    if f['v'] >= 5:
        return min(5, x + 1)
    return x


def derive_zi(c):
    f = c['flat']
    return min(5, A2N[f['a']] + (1 if f['status'] in RUNNING else 0))


def derive_gates_rule(c):
    f = c['flat']
    st, has_d, gap = f['status'], bool(f['delegates']), f['gap']
    return {
        '究竟': 'pass' if st in RUNNING else 'partial' if st == 'draft' else 'fail',
        '完备': 'partial' if gap else 'pass',
        '递进': 'fail' if not has_d else 'partial' if st == 'concept' else 'pass',
        '原子': 'pass' if (has_d and st in RUNNING) else 'partial' if has_d else 'fail',
    }


# ── OSA 21 叶公式降解 ────────────────────────────────────────
def leaf(score, formula_name, inputs):
    return {'score': int(score), 'ev': f'{formula_name}({inputs}) · 非实证默认，待 authored 覆盖',
            'conf': '⚪', 'origin': 'formula'}


def formula_osa(c):
    f = c['flat']
    ci, ce = cell_i(c), cell_e(c)
    xiang, zi = derive_xiang(c), derive_zi(c)
    closure = 4 if f['status'] in RUNNING else 2 if f['status'] == 'draft' else 1
    sp = S2N[f['s']]

    def i_block():
        return {'quan': leaf(ci, 'cell_i', f"assets种类"),
                'zhen': leaf(ce, 'cell_e', f"proof={len(c.get('proof') or [])}"),
                'xi': leaf(min(ci, ce), 'min(quan,zhen)', '保守取邻近min')}

    return {
        'O': {'stmt': None, 'ipo': {
            'i': i_block(),
            'p': {'level': leaf(xiang, 'derive_xiang', f"o={f['o']},v={f['v']},{f['status']}")},
            'o': {'closure': leaf(closure, '闭环基分', f['status']),
                  'auto': leaf(min(closure, zi), 'min(closure,derive_zi)', '保守取邻近min'),
                  'intel': leaf(1, '智能化默认', '无AI自复盘证据')}}},
        'S': {'stmt': None, 'ipo': {
            'i': i_block(),
            'p': {'level': leaf(sp, 's段位', f"s={f['s']}")},
            'o': {'closure': leaf(min(sp, closure), 'min(s段位,闭环基分)', '保守取邻近min'),
                  'auto': leaf(min(min(sp, closure), zi), 'min(closure,derive_zi)', '保守取邻近min'),
                  'intel': leaf(1, '智能化默认', '无AI自复盘证据')}}},
        'A': {'stmt': None, 'ipo': {
            'i': i_block(),
            'p': {'level': leaf(ipo_p(c), 'ipo_p', 'loop.process/execute自动段')},
            'o': {'closure': leaf(closure, '闭环基分', f['status']),
                  'auto': leaf(zi, 'derive_zi', f"a={f['a']},{f['status']}"),
                  'intel': leaf(2 if f['a'] == 'A3' else 1, 'a轴智能化', f"a={f['a']}")}}},
    }


def merge_authored(base_osa, authored):
    """authored 逐叶 deep-merge 覆盖公式默认；authored 叶标 origin=authored。"""
    out = copy.deepcopy(base_osa)
    if not authored:
        return out
    for seg in ('O', 'S', 'A'):
        a_seg = authored.get(seg)
        if not a_seg:
            continue
        if a_seg.get('stmt'):
            out[seg]['stmt'] = a_seg['stmt']
        if a_seg.get('ipo', {}).get('reflow'):
            out[seg]['ipo']['reflow'] = a_seg['ipo']['reflow']
        for grp in ('i', 'p', 'o'):
            for key, lv in (a_seg.get('ipo', {}).get(grp) or {}).items():
                if isinstance(lv, dict) and 'score' in lv:
                    out[seg]['ipo'][grp][key] = {**lv, 'origin': 'authored'}
    return out


# ── live 证据消费（只改置信与证据句，不改分）──────────────────
def _get_leaf(osa, target):
    # target 形如 osa.A.ipo.o.closure
    parts = target.split('.')
    assert parts[0] == 'osa' and len(parts) == 5
    return osa[parts[1]]['ipo'][parts[3]], parts[4]


def apply_live(osa, cell, live_evidence, gaps, today):
    for b in cell.get('live') or []:
        src = (live_evidence or {}).get('sources', {}).get(b['src'])
        grp, key = _get_leaf(osa, b['target'])
        lf = grp.get(key)
        if lf is None:
            continue
        if not src:
            gaps.append(f"live 绑定 {b['src']}.{b['probe']} 无采集快照（跑 collect_live_evidence.py）")
            continue
        probe = src.get('probes', {}).get(b['probe'])
        as_of = src.get('as_of', '')
        age = _age_days(as_of, today)
        if probe is None:
            gaps.append(f"live 探针 {b['src']}.{b['probe']} 缺失")
            continue
        detail = probe.get('detail', '')
        if age is not None and age <= LIVE_MAX_AGE_DAYS and probe.get('ok'):
            grp[key] = {**lf, 'conf': '🟢', 'origin': 'live',
                        'ev': f"{detail} · {b['src']} as_of {as_of}"}
        else:
            why = f'快照 {age:.0f} 天前' if age is not None and age > LIVE_MAX_AGE_DAYS else \
                  ('探针 fail: ' + detail if not probe.get('ok') else '快照时间不可解析')
            grp[key] = {**lf, 'conf': '🟡', 'origin': 'live',
                        'ev': f"降级：{why} · {b['src']} as_of {as_of}"}
            gaps.append(f"live 证据降级（{b['src']}.{b['probe']}: {why}）")


def _age_days(as_of, today):
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            dt = datetime.datetime.strptime(as_of[:19], fmt)
            return (today - dt).total_seconds() / 86400.0
        except (ValueError, TypeError):
            continue
    return None


# ── 逐格打分 ────────────────────────────────────────────────
def score_cell(c, live_evidence, today):
    f = c['flat']
    gaps = []
    osa = merge_authored(formula_osa(c), c.get('osa'))
    apply_live(osa, c, live_evidence, gaps, today)

    xiang = osa['O']['ipo']['p']['level']['score']
    zi = osa['A']['ipo']['o']['auto']['score']
    va_raw = min(xiang, zi)
    gold = c.get('gold_attest')
    va = va_raw if gold else min(va_raw, 4)

    # 四门：公式族 × judgment 族取更严，gates_authored 再覆盖
    fg = {'究竟': cell_e(c), '完备': cell_i(c), '递进': cell_v(c), '原子': cell_a(c)}
    rg = derive_gates_rule(c)
    gates = {}
    for g in GATE_KEYS:
        v_f, v_r = verdict(fg[g]), rg[g]
        worse = v_f if SEV[v_f] >= SEV[v_r] else v_r
        gates[g] = {'verdict': worse,
                    'reason': f'公式 {PINYIN[g]}={fg[g]}→{v_f} × 规则({f["status"]}/委派/gap)→{v_r}，取严'}
    for g, ov in (c.get('gates_authored') or {}).items():
        if g in gates:
            gates[g] = {'verdict': ov['verdict'], 'reason': f"人裁: {ov['reason']}", 'authored': True}

    # 距100分
    n_leaves, n_authored = 0, 0
    for seg in ('O', 'S', 'A'):
        for grp in ('i', 'p', 'o'):
            for key, lv in osa[seg]['ipo'][grp].items():
                if isinstance(lv, dict) and 'score' in lv:
                    n_leaves += 1
                    if lv.get('origin') in ('authored', 'live'):
                        n_authored += 1
    if f['gap']:
        gaps.append(f"空白格：{f['reuse']}")
    if zi < 3:
        gaps.append(f"自动化仅 {f['a']}（自={zi}/5），未到 A2 流水")
    if xiang < 3:
        gaps.append(f"想透仅 {xiang}/5，未爬到观点/洞察层")
    for g in GATE_KEYS:
        if gates[g]['verdict'] != 'pass':
            gaps.append(f"四门·{g}={gates[g]['verdict']}")
    if n_authored == 0:
        gaps.append(f"三五三 21 叶全公式⚪，0 叶 authored——递归判断尚未人裁")
    if not gold and va_raw >= 5:
        gaps.append('va 公式达 5 但无金卡人证（gold_attest），按纪律封顶 4')
    if c.get('next_battle'):
        gaps.append(f"下一战：{c['next_battle']}")

    conf = ('🟢' if f['status'] in RUNNING and f['delegates'] else
            '⚪' if f['status'] == 'concept' and not f['delegates'] else '🟡')
    return {
        'cell_id': c['cell_id'], 'domain': c['domain'], 'layer': c['layer'], 'name': c['name'],
        'flat': f, 'sourcing': c.get('sourcing', ''), 'verified': c.get('verified', ''),
        'assets': c.get('assets', []), 'proof': c.get('proof', []), 'loop': c.get('loop', {}),
        'hint': c.get('hint', ''), 'cand': c.get('cand', ''), 'score_meta': c.get('score', {}),
        'osa': osa, 'gates': gates,
        'xiang': xiang, 'zi': zi, 'va': va, 'va_raw': va_raw,
        'bottleneck': 'A 自动' if zi < xiang else 'O/S 想透' if xiang < zi else '想自齐平',
        'm': min(O_LEVEL[f['o']], S2N[f['s']], A2N[f['a']]),
        'pri': f['v'] * (6 - min(O_LEVEL[f['o']], S2N[f['s']], A2N[f['a']])),
        'confidence': conf, 'gold': bool(gold), 'gaps': gaps,
        'authored_coverage': f'{n_authored}/{n_leaves}',
        'legacy_ipo': {'i': cell_i(c), 'p': ipo_p(c), 'o': ipo_o(c)},
        'next_battle': c.get('next_battle'),
        'edges': c.get('edges') or [],
    }


# ── 图级评分（H/V/A/E 公式代理·⚪，可被 MAP.score_authored 覆盖）──
def score_map_level(m, cells):
    n = len(cells)
    va_avg = sum(r['va'] for r in cells) / n
    deleg_ratio = sum(1 for r in cells if r['flat']['delegates']) / n
    ev_ratio = sum(1 for r in cells if r['proof'] or r['assets']) / n
    has_gap_cells = any(r['flat']['gap'] for r in cells)
    H = 4 if (len(m['DOMAINS']) >= 9 and has_gap_cells) else 3
    V = max(1, min(5, round(va_avg)))
    A = 5 if deleg_ratio >= 0.95 else 4 if deleg_ratio >= 0.8 else 3 if deleg_ratio >= 0.5 else 2
    E = 5 if ev_ratio >= 0.85 else 4 if ev_ratio >= 0.6 else 3 if ev_ratio >= 0.4 else 2
    sc = {'H': H, 'V': V, 'A': A, 'E': E, 'origin': 'formula'}
    sc.update(m['MAP'].get('score_authored') or {})
    sc['min'] = min(sc['H'], sc['V'], sc['A'], sc['E'])
    gold_cells = sum(1 for r in cells if r['gold'] and r['va'] >= 5
                     and all(g['verdict'] == 'pass' for g in r['gates'].values()))
    sc['tier'] = '🥇金卡' if (sc['min'] >= 4 and gold_cells) else '🥈合格' if sc['min'] >= 3 else '🚧草稿'
    return sc, gold_cells


def score_map(map_id, live_evidence=None, today=None):
    _require_loader()
    today = today or datetime.datetime.now()
    m = load_map(map_id)
    if live_evidence is None:
        lp = os.path.join(ROOT, 'data', 'maps', map_id, 'live_evidence.json')
        live_evidence = json.load(open(lp)) if os.path.exists(lp) else None
    cells = [score_cell(c, live_evidence, today) for c in m['CELLS']]
    map_score, gold_cells = score_map_level(m, cells)
    no_gold = gold_cells == 0
    n_leaves = sum(int(r['authored_coverage'].split('/')[1]) for r in cells)
    n_auth = sum(int(r['authored_coverage'].split('/')[0]) for r in cells)
    top_gaps = sorted((r for r in cells if r['va'] < 3), key=lambda r: -r['pri'])
    return {
        'schema': 'cbm-osa-ipo-scored-v1',
        'map_id': map_id, 'MAP': m['MAP'], 'LAYERS': m['LAYERS'], 'DOMAINS': m['DOMAINS'],
        'source_hash': m['source_hash'], 'scored_at': today.strftime('%Y-%m-%d %H:%M'),
        'no_gold_card': no_gold, 'gold_cells': gold_cells,
        'authored_coverage': f'{n_auth}/{n_leaves}',
        'formula_ratio': round(1 - (n_auth / n_leaves), 3) if n_leaves else 1.0,
        'map_score': map_score,
        'stats': {
            'cells': len(cells),
            'va_lt3': sum(1 for r in cells if r['va'] < 3),
            'conf': {k: sum(1 for r in cells if r['confidence'] == k) for k in ('🟢', '🟡', '⚪')},
            'bottleneck': {k: sum(1 for r in cells if r['bottleneck'] == k)
                           for k in ('A 自动', 'O/S 想透', '想自齐平')},
        },
        'top_gaps': [{'cell_id': r['cell_id'], 'name': r['name'], 'pri': r['pri'],
                      'va': r['va'], 'first_gap': r['gaps'][0] if r['gaps'] else ''}
                     for r in top_gaps[:8]],
        'cells': cells,
    }


# ── 评分门（--check）与棘轮 ─────────────────────────────────
def check_map(scored, map_id, update_baseline=False):
    errs = []
    for r in scored['cells']:
        for seg in ('O', 'S', 'A'):
            for grp in ('i', 'p', 'o'):
                for key, lv in r['osa'][seg]['ipo'][grp].items():
                    if not isinstance(lv, dict) or 'score' not in lv:
                        continue
                    path = f"{r['cell_id']}.osa.{seg}.{grp}.{key}"
                    if lv['origin'] == 'formula' and lv['conf'] != '⚪':
                        errs.append(f'{path}: 公式叶置信非⚪（假绿）')
                    if lv['origin'] == 'authored':
                        if not lv.get('ev'):
                            errs.append(f'{path}: authored 叶缺证据句')
                        if lv.get('conf') not in ('🟢', '🟡'):
                            errs.append(f'{path}: authored 叶置信须🟢/🟡')
                        if lv.get('conf') == '🟢' and not (r['proof'] or r['assets']):
                            errs.append(f'{path}: 🟢叶所在格无 proof/assets 锚点')
                    if not (1 <= lv['score'] <= 5):
                        errs.append(f'{path}: 分数越界 {lv["score"]}')
        if not r['gold'] and r['va'] > 4:
            errs.append(f"{r['cell_id']}: 无 gold_attest 而 va={r['va']}（禁虚报满分）")
    # 棘轮
    bl_path = os.path.join(ROOT, 'data', 'maps', map_id, 'baseline.json')
    cur = {r['cell_id']: r['va'] for r in scored['cells']}
    if os.path.exists(bl_path):
        bl = json.load(open(bl_path))
        for cid, prev in bl.get('va', {}).items():
            if cid in cur and cur[cid] < prev:
                errs.append(f'{cid}: va {cur[cid]} < 棘轮基线 {prev}（分数只升不降；确属真实退化须 weekly 人批降基线）')
        if scored['map_score']['min'] < bl.get('map_min', 0):
            errs.append(f"图min {scored['map_score']['min']} < 棘轮基线 {bl['map_min']}")
        if update_baseline and not errs:
            _write_baseline(bl_path, cur, scored)
    else:
        _write_baseline(bl_path, cur, scored)
        print(f'[{map_id}] 棘轮基线首建 → {bl_path}')
    return errs


def _write_baseline(path, cur, scored):
    json.dump({'schema': 'va-baseline-v1', 'as_of': scored['scored_at'],
               'map_min': scored['map_score']['min'], 'va': cur},
              open(path, 'w'), ensure_ascii=False, indent=1)


def main():
    _require_loader()
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', dest='map_id')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--update-baseline', action='store_true')
    args = ap.parse_args()
    ids = list_maps() if args.all else [args.map_id] if args.map_id else []
    if not ids:
        ap.error('需要 --map <id> 或 --all')
    os.makedirs(OUT_DIR, exist_ok=True)
    board, failed = [], False
    for mid in ids:
        scored = score_map(mid)
        out = os.path.join(OUT_DIR, f'{mid}.scored.json')
        json.dump(scored, open(out, 'w'), ensure_ascii=False, indent=1)
        errs = check_map(scored, mid, update_baseline=args.update_baseline) if (args.check or args.update_baseline) else []
        ms = scored['map_score']
        board.append({'map_id': mid, 'title': scored['MAP'].get('title'), 'kind': scored['MAP'].get('kind'),
                      'ring': scored['MAP'].get('ring'), 'href': scored['MAP'].get('href'),
                      'grid': scored['MAP'].get('grid'), 'H': ms['H'], 'V': ms['V'], 'A': ms['A'], 'E': ms['E'],
                      'min': ms['min'], 'tier': ms['tier'], 'no_gold_card': scored['no_gold_card'],
                      'authored_coverage': scored['authored_coverage'],
                      'va_lt3': scored['stats']['va_lt3'], 'cells': scored['stats']['cells'],
                      'scored_at': scored['scored_at'], 'source_hash': scored['source_hash']})
        st = scored['stats']
        print(f"[{mid}] {st['cells']}格 va<3={st['va_lt3']} 无金卡={scored['no_gold_card']} "
              f"authored={scored['authored_coverage']} min={ms['min']} {ms['tier']} → {out}")
        if errs:
            failed = True
            print(f'[{mid}] 评分门 FAIL ×{len(errs)}:')
            for e in errs[:20]:
                print('  ✗', e)
    json.dump({'schema': 'cbm-scoreboard-v1',
               'as_of': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'maps': board},
              open(os.path.join(OUT_DIR, 'scoreboard.json'), 'w'), ensure_ascii=False, indent=1)
    if args.check and failed:
        sys.exit(1)
    if args.check:
        print('评分门 PASS：禁假绿/金卡封顶/棘轮全过')

