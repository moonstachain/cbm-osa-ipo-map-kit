#!/usr/bin/env python3
"""map-agnostic 渲染器：build/out/<map_id>.scored.json → site/ 页面（零评分，只读只摆）。

layout=portal（内核）：capability.html（10域总览）+ <domain>.html ×10 + capability-judgment.html（判断书）。
layout=single（标杆，Phase 2）：map-<id>.html 五段式。

红线：判断/渲染分离——本文件不出现任何打分/推导逻辑；分数、四门、距100分全部来自 scored.json。
渲染前校验 scored.source_hash == 当前 map.py 哈希（防陈旧渲染），不符则要求先跑打分器。

用法：python3 build/build_maps.py --map org-kernel   |   --all
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'ops'))
import common as C  # noqa: E402
from map_loader import MAPS_DIR, list_maps  # noqa: E402

OUT_DIR = os.path.join(ROOT, 'build', 'out')

DEEPLINKS = {}  # 域级深链（按需配置：{域id: (url, 链接文案)}）


def load_scored(map_id):
    p = os.path.join(OUT_DIR, f'{map_id}.scored.json')
    if not os.path.exists(p):
        sys.exit(f'缺 {p}：先跑 python3 ops/card_triangle_scorer.py --map {map_id}')
    s = json.load(open(p))
    src = os.path.join(MAPS_DIR, map_id, 'map.py')
    if not os.path.exists(src):
        src = os.path.join(MAPS_DIR, map_id, 'map.json')
    cur = hashlib.sha256(open(src, 'rb').read()).hexdigest()
    if cur != s['source_hash']:
        sys.exit(f'{map_id}: scored.json 已陈旧（map 源已改）——先重跑打分器再渲染')
    return s


# ── 网格单元（承现网标记 + 追加 va 徽标）─────────────────────
def cell_html(r):
    f = r['flat']
    gap_cls = ' gap' if f['gap'] else ''
    gapflag = '<span class="gapflag">🔴盲区</span>' if f['gap'] else ''
    proof_flag = '实证✓' if r['proof'] else '实证—'
    deleg = C.esc(f['delegates'][0]) + (', ' if len(f['delegates']) > 1 else '') if f['delegates'] else '—'
    hc = C.HEATC[heat_of(r)]
    dots = []
    for k in ('collect', 'process', 'execute', 'distribute'):
        v = (r['loop'] or {}).get(k, 'none')
        bg = 'var(--up)' if v == 'auto' else 'var(--hot)' if v == 'manual' else 'var(--ink-3)'
        dots.append(f'<b style="background:{bg}" title="{k}:{v}"></b>')
    return (f'<div class="cell{gap_cls}" data-id="{r["cell_id"]}">{gapflag}'
            f'<div class="id">{r["cell_id"]} · pri {r["pri"]} · {proof_flag} · va{r["va"]}</div>'
            f'<div class="nm">{C.esc(r["name"])}</div>'
            f'<div class="ax"><span class="pill" style="color:{hc}">{f["o"]}/{f["s"]}/{f["a"]}</span>'
            f'<span>{deleg}</span></div>'
            f'<div class="cellloop">{"".join(dots)}</div></div>')


def heat_of(r):
    return C.heat(r['pri'])


# ── 抽屉（承现网骨架 + OSA三页签/距100分/双源四门）───────────
DRAWER_HTML = '''
<div id="dr"><div class="panel"><span class="close" onclick="cd()">✕</span>
<h3 id="d-nm"></h3><div class="cid" id="d-cid"></div>
<div class="axbig"><div class="axbox"><div class="l">信息 o</div><div class="b" id="d-o"></div></div>
<div class="axbox"><div class="l">策略 s</div><div class="b" id="d-s"></div></div>
<div class="axbox"><div class="l">自动化 a</div><div class="b" id="d-a"></div></div>
<div class="axbox"><div class="l">pri</div><div class="b" id="d-pri"></div></div></div>
<div class="vaxrow"><span>想 <b id="d-xiang"></b></span><span>自 <b id="d-zi"></b></span><span class="va">va <b id="d-va"></b></span><span id="d-bneck"></span></div>
<div class="k">实证 / PROOF · 真跑出的结果</div><div id="d-proof"></div>
<div class="k">闭环 / LOOP · 采集→处理→执行→分发</div><div class="lprow" id="d-loop"></div>
<div class="k">资产直达 / ASSETS</div><div id="d-assets"></div>
<div class="k">能力说明 / REUSE</div><div class="v" id="d-reuse"></div>
<div class="k">复用指引 / HOW TO INVOKE</div><div class="v hint" id="d-hint"></div>
<div id="d-edgewrap" style="display:none"><div class="k">关系边 / EDGES</div><div class="v mono" id="d-edges" style="font-size:11px"></div></div>
<div class="k">历史递归叶片 / LEGACY READ-ONLY（不驱动 v2 评分）</div>
<div class="osatabs" id="d-osatabs"></div><div id="d-osa"></div>
<div class="ipolegacy" id="d-ipolegacy"></div>
<div class="k">四道门自检 / GATES（究竟·完备·递进·原子 · 公式×规则取严）</div><div id="d-gates"></div>
<div id="d-scwrap"><div class="k">评分依据 / EVIDENCE</div><div id="d-score"></div></div>
<div class="k">距100分 / GAP TO 100</div><ul class="g100" id="d-gaps"></ul>
<div id="d-candwrap" style="display:none"><div class="k">候选补齐 / CANDIDATES</div><div class="v cand" id="d-cand"></div></div>
<div class="k">STATUS</div><div class="v mono" id="d-status"></div></div></div>
'''

DRAWER_JS = r'''
var KC={skill:'SKILL',pack:'PACK',repo:'REPO',site:'SITE',doc:'DOC'};
var OSEG={O:'O 目标历史叶片',S:'S 策略历史叶片',A:'A 行动历史叶片'};
var OROWS=[['i','quan','I 采·全(不漏)'],['i','zhen','I 采·真一手'],['i','xi','I 采·细'],
           ['p','level','P 工·五层'],['o','closure','O 表·闭环'],['o','auto','O 表·自动化'],['o','intel','O 表·智能化']];
var OB={formula:'公式',authored:'人裁',live:'live'};
function esc(s){var d=document.createElement('div');d.textContent=s==null?'':s;return d.innerHTML}
function scol(n){return n>=4?'var(--up)':n==3?'var(--gold)':n==2?'var(--hot)':'var(--down)'}
function renderSeg(c,seg){var s=c.osa[seg],ip=s.ipo,h='';
 if(s.stmt)h+='<div class="osa-stmt">'+esc(s.stmt)+'</div>';
 h+=OROWS.map(function(r){var lf=ip[r[0]][r[1]];if(!lf)return '';
   return '<div class="osarow"><span class="ax">'+r[2]+'</span><span class="sc" style="color:'+scol(lf.score)+'">'+lf.score+'/5 '+lf.conf+
     '</span><span class="ev"><span class="ob '+lf.origin+'">'+(OB[lf.origin]||lf.origin)+'</span>'+esc(lf.ev)+'</span></div>'}).join('');
 if(ip.reflow)h+='<div class="osa-stmt">回流：'+esc(ip.reflow)+'</div>';
 return h}
function showSeg(c,seg){document.getElementById('d-osa').innerHTML=renderSeg(c,seg);
 document.querySelectorAll('.osatab').forEach(function(t){t.classList.toggle('on',t.dataset.seg===seg)})}
function od(id,push){var c=C[id];if(!c)return;
 document.getElementById('d-nm').textContent=c.name+(c.gap?'  · 战略空白':'');
 document.getElementById('d-cid').textContent=c.cid+' · '+c.lay+' · sourcing:'+c.sourcing;
 document.getElementById('d-o').textContent=c.o;document.getElementById('d-s').textContent=c.s;
 document.getElementById('d-a').textContent=c.a;document.getElementById('d-pri').textContent=c.pri;
 document.getElementById('d-xiang').textContent=c.xiang;document.getElementById('d-zi').textContent=c.zi;
 document.getElementById('d-va').textContent=c.va;
 document.getElementById('d-bneck').textContent='瓶颈 '+c.bottleneck+' · authored '+c.authored_coverage;
 var LS={collect:'采集',process:'处理',execute:'执行',distribute:'分发'};
 var ph=(c.proof||[]).map(function(p){
   var inner='<span class="ak">'+p.kind.toUpperCase()+'</span><span class="at">'+esc(p.name)+'</span>'+
     (p.num?'<div class="pnum">'+esc(p.num)+'</div>':'')+
     '<div class="psrc">'+esc(p.date)+(p.src?' · 出处 '+esc(p.src):'')+'</div>';
   return p.href?'<a class="pitem" href="'+p.href+'" target="_blank" rel="noopener">'+inner+'</a>'
                :'<div class="pitem">'+inner+'</div>'}).join('');
 document.getElementById('d-proof').innerHTML=ph||
   '<div class="pitem noproof">'+(c.gap?'— 战略空白，无交付物':'— 评分有据·无独立交付物实证（不假绿：能力可用但未单独跑出结果）')+'</div>';
 document.getElementById('d-loop').innerHTML=['collect','process','execute','distribute'].map(function(k){
   var v=(c.loop||{})[k]||'none';return '<span class="lseg '+v+'"><i></i>'+LS[k]+'·'+(v==='auto'?'自动':v==='manual'?'人跑':'无')+'</span>'}).join('<span class="larr">→</span>');
 document.getElementById('d-hint').textContent=c.hint||'';
 var ew=document.getElementById('d-edgewrap');
 if(c.edges&&c.edges.length){ew.style.display='';document.getElementById('d-edges').textContent=c.edges.join('   ·   ')}else{ew.style.display='none'}
 var tabs=document.getElementById('d-osatabs');
 tabs.innerHTML=['O','S','A'].map(function(k){return '<span class="osatab" data-seg="'+k+'">'+OSEG[k]+'</span>'}).join('');
 tabs.querySelectorAll('.osatab').forEach(function(t){t.addEventListener('click',function(){showSeg(c,t.dataset.seg)})});
 showSeg(c,'O');
 var li=c.legacy_ipo;
 document.getElementById('d-ipolegacy').textContent='旧版信息三段兼容视图(只读公式) i='+li.i+' p='+li.p+' o='+li.o+' · 不进入 yuanli-osa-card/v2';
 document.getElementById('d-gates').innerHTML=['究竟','完备','递进','原子'].map(function(k){var g=c.gates[k];
   return '<div class="gaterow"><span class="gate '+g.verdict+'">'+k+' · '+g.verdict+(g.authored?' ·人裁':'')+'</span><span class="greason">'+esc(g.reason)+'</span></div>'}).join('');
 var ah=(c.assets||[]).map(function(a){
   var inner='<span class="ak">'+(KC[a.k]||a.k)+'</span><span class="at">'+esc(a.t)+'</span><span class="asub">'+esc(a.sub)+'</span>';
   return a.href?'<a class="alink" href="'+a.href+'" target="_blank" rel="noopener">'+inner+' ↗</a>'
                :'<span class="alink local">'+inner+'</span>'}).join('');
 document.getElementById('d-assets').innerHTML=ah||'<span class="v" style="color:var(--fg-3)">— 无已验真资产（战略空白）</span>';
 document.getElementById('d-reuse').textContent=c.reuse;
 var sw=document.getElementById('d-scwrap');
 if(c.score&&c.score.o_ev){sw.style.display='';var f=c.score.s_factors||{};var fh=Object.keys(f).map(function(k){return '<span class="fchip">'+esc(k)+' '+f[k]+'</span>'}).join('');
  document.getElementById('d-score').innerHTML=
   '<div class="ev"><b>O</b> '+esc(c.score.o_ev)+'</div>'+
   '<div class="ev"><b>S</b> '+esc(c.score.s_ev||'')+'<div class="fwrap">'+fh+'</div></div>'+
   '<div class="ev"><b>A</b> '+esc(c.score.a_ev)+'</div>'+
   '<div class="scmeta">'+esc(c.score.scored_at)+' · '+esc(c.score.scored_by)+' · 链接验真 '+esc(c.verified)+'</div>';
 }else{sw.style.display='none'}
 document.getElementById('d-gaps').innerHTML=(c.gaps||[]).map(function(g){
   var nb=g.indexOf('下一战')===0;return '<li'+(nb?' class="nb"':'')+'>'+esc(g)+'</li>'}).join('')||'<li>— 无缺口记录</li>';
 var cw=document.getElementById('d-candwrap');
 if(c.cand){cw.style.display='';document.getElementById('d-cand').textContent=c.cand}else{cw.style.display='none'}
 document.getElementById('d-status').textContent=c.status+'  (热度 '+c.heat+(c.gap?' · 🔴盲区':'')+(c.gold?' · 🥇金卡':'')+')';
 document.getElementById('dr').classList.add('on');
 if(push!==false){try{history.replaceState(null,'','#'+id)}catch(e){}}}
function cd(){document.getElementById('dr').classList.remove('on');
 try{history.replaceState(null,'',location.pathname)}catch(e){}}
document.querySelectorAll('.cell[data-id],.mcell[data-id]').forEach(function(e){e.addEventListener('click',function(){od(e.dataset.id)})});
document.getElementById('dr').addEventListener('click',function(e){if(e.target.id==='dr')cd()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')cd()});
(function(){var h=decodeURIComponent(location.hash.slice(1));if(h&&C[h]){od(h,false);
 var el=document.querySelector('.cell[data-id="'+h+'"],.mcell[data-id="'+h+'"]');if(el)el.scrollIntoView({block:'center'})}})();
'''


def cell_payload(r, lay_label):
    f = r['flat']
    return {
        'name': r['name'], 'cid': r['cell_id'], 'lay': lay_label[r['layer']],
        'o': f['o'], 's': f['s'], 'a': f['a'], 'v': f['v'], 'pri': r['pri'],
        'heat': heat_of(r), 'status': f['status'], 'sourcing': r.get('sourcing', ''),
        'verified': r.get('verified', ''), 'gap': f['gap'], 'reuse': f['reuse'],
        'assets': r['assets'], 'proof': r['proof'], 'loop': r['loop'],
        'hint': r.get('hint', ''), 'cand': r.get('cand', ''), 'score': r.get('score_meta', {}),
        'xiang': r['xiang'], 'zi': r['zi'], 'va': r['va'], 'bottleneck': r['bottleneck'],
        'authored_coverage': r['authored_coverage'], 'osa': r['osa'], 'gates': r['gates'],
        'gaps': r['gaps'], 'legacy_ipo': r['legacy_ipo'], 'gold': r['gold'],
        'edges': r.get('edges') or [],
    }


def render_domain(*a,**k):
    raise NotImplementedError('portal 布局不在 kit（kit 只发 single 五段式）')


def render_capability(*a,**k):
    raise NotImplementedError('portal 布局不在 kit（kit 只发 single 五段式）')


def render_judgment(*a,**k):
    raise NotImplementedError('portal 布局不在 kit（kit 只发 single 五段式）')


def _load_scoreboard():
    p = os.path.join(OUT_DIR, 'scoreboard.json')
    return json.load(open(p))['maps'] if os.path.exists(p) else []


def render_single(scored):
    """single 五段式（标杆单图页）：SIBLING / GOLDEN TRIANGLE+指标条 / BOARD / GAP TO 100 / NEXT。
    组件体系与 portal 同源（同 CSS/门/抽屉·OSA三页签），零评分只摆 scored.json。"""
    m, ms, cells = scored['MAP'], scored['map_score'], scored['cells']
    dom_meta = {d[0]: d for d in scored['DOMAINS']}
    lay_list = scored['LAYERS']

    # ① SIBLING（scoreboard 生成，替代静态页硬编码）
    sib = []
    for e in _load_scoreboard():
        on = ' class="on"' if e['map_id'] == scored['map_id'] else ''
        sib.append(f'<a href="{e["href"]}"{on}>{C.esc(e["title"])}'
                   f'<span class="tier">min{e["min"]} {e["tier"]}</span></a>')
    sib.append('<a href="capability.html">本OS组织能力 CBM<span class="tier">环0·分形内核</span></a>')

    # ② GOLDEN TRIANGLE + 指标条（诚实口径：资产条数非"验真"）
    tri = ''.join(f'<span class="ax{" mn" if k == "min" else ""}">{k}<b>{ms[k]}</b></span>'
                  for k in ('H', 'V', 'A', 'E', 'min')) + f'<span class="ax mn">{ms["tier"]}</span>'
    st = scored['stats']
    n_assets = sum(len(r['assets']) for r in cells)
    loop_auto = sum(1 for r in cells for v in (r['loop'] or {}).values() if v == 'auto')
    loop_tot = sum(len(r['loop'] or {}) for r in cells) or 1
    gap_n = sum(1 for r in cells if r['flat']['gap'])
    metrics = ''.join(f'<span>{x}</span>' for x in (
        f'域 {len(scored["DOMAINS"])}', f'格 {st["cells"]}', f'盲区格 {gap_n}',
        f'va&lt;3 {st["va_lt3"]}', f'authored {scored["authored_coverage"]} 叶',
        f'⚪公式 {scored["formula_ratio"]:.0%}', f'资产条数 {n_assets}',
        f'loop自动 {loop_auto / loop_tot:.0%}',
        f'🟢{st["conf"]["🟢"]}/🟡{st["conf"]["🟡"]}/⚪{st["conf"]["⚪"]}',
        f'{scored["scored_at"]}'))

    # ③ BOARD（域×层棋盘）
    by = {}
    for r in cells:
        by.setdefault((r['domain'], r['layer']), []).append(r)
    grid = ['<div class="sgrid">', '<div class="sgh">域 \\ 层<span class="e">MECE×三责任层</span></div>']
    for lid, ln, ld in lay_list:
        grid.append(f'<div class="sgh">{C.esc(ln)}<span class="e">{C.esc(ld)}</span></div>')
    for d in scored['DOMAINS']:
        grid.append(f'<div class="sgd">{C.esc(d[1])}<div class="de">{C.esc(d[6] if len(d) > 6 else "")}</div></div>')
        for lid, _, _ in lay_list:
            cs = by.get((d[0], lid), [])
            grid.append('<div>' + ''.join(cell_html(r) for r in cs) + '</div>' if cs
                        else '<div class="cell gap" style="opacity:.45"><div class="id">（未立格）</div></div>')
    grid.append('</div>')

    # ④ GAP TO 100
    g100 = []
    for r in cells:
        core = [g for g in r['gaps'] if not g.startswith('三五三')][:3]
        if core:
            g100.append(f'<div class="gcell">{r["cell_id"]} · {C.esc(r["name"])} · va{r["va"]}</div><ul class="g100">'
                        + ''.join(f'<li{" class=nb" if g.startswith("下一战") else ""}>{C.esc(g)}</li>' for g in core)
                        + '</ul>')

    # ⑤ NEXT（MAP.next authored + 各格 next_battle 汇入）
    next_items = list(m.get('next', []))
    next_items += [f'<b>{r["cell_id"]}</b> · {r["next_battle"]}' for r in cells if r.get('next_battle')]
    next_html = ('<div class="hs">下一战 / NEXT · 按撬动排序</div><ol class="nextol">'
                 + ''.join(f'<li>{x}</li>' for x in next_items) + '</ol>') if next_items else ''

    lay_label = {l[0]: l[1] for l in lay_list}
    payload = {r['cell_id']: cell_payload(r, lay_label) for r in cells}
    deeplink = ''
    if m.get('deeplink'):
        href, label = m['deeplink']
        deeplink = f'<a class="big-link" href="{href}" target="_blank">{C.esc(label)}</a>'
    foot = ('五段式标杆图 · 分数唯一来源 ops/card_triangle_scorer.py（公式⚪/authored/live 三源置信）'
            ' · 棘轮 min 只升不降 · 升分只走 weekly 写回弹夹真源 · 密码门 sha256-only')
    nav = ('<nav class="nav"><a href="index.html" class="brand">Org-Capability Map</a>'
           '<a href="index.html" class="">版图</a><a href="capability.html" class="">能力总图</a>'
           f'<a href="{m["href"]}" class="on">{C.esc(m["title"])}</a>'
           '<a href="maps-audit.html" class="" style="color:var(--gold-2)">记分卡</a>'
           '<span class="right">标杆弹夹 · 原子卡产线 · your-site</span></nav>')
    return (C.head(f'{m["title"]} · 战略地图-原子卡片', m.get('blurb', '')) + '<body>' + nav
            + '<div class="wrap">'
            + '<div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap">'
            + f'<h1>{C.esc(m["title"])}</h1><span class="sub">{C.esc(m.get("role", ""))}</span>'
            + f'<span class="mono" style="color:var(--gold);border:1px solid var(--gold-3);padding:2px 9px;'
            + f'border-radius:2px;font-size:11px">环{m.get("ring", "?")} · {C.esc(m.get("grid", ""))}</span></div>'
            + f'<div class="meta">{scored["map_id"]} · cellcard-v1 · legacy_recursive_interpretation · as_of {C.esc(m.get("as_of", ""))}</div>'
            + f'<div class="blurb">{C.esc(m.get("blurb", ""))}</div>'
            + C.honesty_banner(scored)
            + deeplink
            + '<div class="tag">SIBLING MAPS · 同构标杆</div><div class="mapsw">' + ''.join(sib) + '</div>'
            + '<div class="tag">GOLDEN TRIANGLE · 黄金三角</div>'
            + f'<div class="scoreband">{tri}</div><div class="metrics">{metrics}</div>'
            + f'<div class="tag">BOARD · 棋盘</div><div class="hs">{C.esc(m["title"])}（点击格子查看历史只读叶片）</div>'
            + ''.join(grid)
            + '<div class="g100sec"><div class="hs">距100分 / GAP TO 100 · 缺口即验收清单</div>'
            + ''.join(g100) + '</div>'
            + next_html
            + f'<footer>{foot}</footer></div>'
            + DRAWER_HTML
            + '<script>var C=' + json.dumps(payload, ensure_ascii=False) + ';\n' + DRAWER_JS
            + '</script></body></html>')


def render_playbook(*a,**k):
    raise NotImplementedError('portal 布局不在 kit（kit 只发 single 五段式）')


def build_portal(scored):
    raise NotImplementedError("portal 布局不在 kit（kit 只发 single 五段式）")


def new_map(map_id):
    """弹夹工厂：拷 _template → data/maps/<id>/，替换 map_id 占位。"""
    import re
    assert re.fullmatch(r'[a-z][a-z0-9-]{1,30}', map_id), 'map_id 须为小写字母开头的 kebab-case'
    src = os.path.join(MAPS_DIR, '_template', 'map.py')
    dst_dir = os.path.join(MAPS_DIR, map_id)
    dst = os.path.join(dst_dir, 'map.py')
    assert not os.path.exists(dst), f'{dst} 已存在，拒绝覆盖'
    os.makedirs(dst_dir, exist_ok=True)
    open(dst, 'w').write(open(src).read().replace('__MAP_ID__', map_id))
    print(f'新弹夹已开: {dst}')
    print('下一步（五问 intake → 三命令出图）：')
    print('  ①脊 数据在哪怎么拿 ②实体 MECE域×3层 ③判断 每格OSA ④视图 ⑤诚实 缺数显示什么')
    print(f'  python3 {dst}                                        # 自检')
    print(f'  python3 ops/card_triangle_scorer.py --map {map_id} --check   # 评分门')
    print(f'  python3 build/build_maps.py --map {map_id}                    # 出图')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', dest='map_id')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--new', dest='new_id')
    args = ap.parse_args()
    if args.new_id:
        new_map(args.new_id)
        return
    ids = list_maps() if args.all else [args.map_id] if args.map_id else []
    if not ids:
        ap.error('需要 --map <id> 或 --all')
    for mid in ids:
        scored = load_scored(mid)
        layout = scored['MAP'].get('layout', 'single')
        if layout == 'portal':
            outs = build_portal(scored)
        elif layout == 'single':
            href = scored['MAP'].get('href', f'map-{mid}.html')
            assert href.startswith('map-') and href.endswith('.html'), f'{mid}: single 布局 href 须为 map-*.html'
            p = os.path.join(C.SITE, href)
            open(p, 'w').write(render_single(scored))
            outs = [p]
        else:
            print(f'[{mid}] layout={layout} 非本产线布局（如 atom 归 soul 线），跳过')
            continue
        for p in outs:
            print(f'  {p} ({os.path.getsize(p) // 1024}KB)')
        print(f'[{mid}] {len(outs)} 页再生（零评分·source_hash 已校验）')


if __name__ == '__main__':
    main()
