#!/usr/bin/env python3
"""渲染产线共用件（抽取自 07-06 现网富化页，字节级冻结于 build/templates/*.frag）。

- 门体（MAPKIT_GATE_V1·sha256-only）与全站 CSS 逐字复用，不改视觉基线；
- 新增样式（诚实横幅/OSA三页签/距100分/origin徽标）全部追加命名空间类，只增不改；
- 本模块零评分：只提供模板与工具函数，分数一律来自 scored.json。
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(HERE, 'templates')
SITE = os.path.join(ROOT, 'site')
os.makedirs(SITE, exist_ok=True)


def _frag(name):
    return open(os.path.join(TPL, name)).read()


GATE = _frag('gate.frag')
CSS = _frag('domain_css.frag')

# 新增样式：只增不改（命名空间 hb-/osa-/g100-/ob-）
EXTRA_CSS = '''
/* ── 重构新增：诚实横幅 ── */
.hb{margin:14px 0 4px;padding:10px 14px;border:1px solid var(--down);border-left:3px solid var(--down);
  background:rgba(201,122,114,.06);font-size:12px;color:var(--fg-1);letter-spacing:.4px;line-height:1.8}
.hb b{color:var(--down)}
.hb .m{font-family:'JetBrains Mono',monospace;color:var(--fg-2)}
/* ── OSA 三页签 ── */
.osatabs{display:flex;gap:6px;margin:8px 0 6px}
.osatab{flex:1;text-align:center;padding:7px 4px;border:1px solid var(--line-2);cursor:pointer;
  font-size:12px;letter-spacing:1.5px;color:var(--fg-2);background:var(--ink-1);border-radius:2px;user-select:none}
.osatab.on{border-color:var(--gold-3);color:var(--gold);background:rgba(201,169,106,.07)}
.osa-stmt{font-size:12px;color:var(--fg-1);margin:6px 0;padding:6px 10px;border-left:2px solid var(--gold-3);background:var(--ink-1)}
.osarow{display:grid;grid-template-columns:96px 64px auto;gap:8px;align-items:baseline;
  padding:5px 2px;border-bottom:1px dashed var(--line-1);font-size:12px}
.osarow .ax{color:var(--fg-2);letter-spacing:.5px}
.osarow .sc{font-family:'JetBrains Mono',monospace;font-weight:600}
.osarow .ev{color:var(--fg-2);line-height:1.6}
.ob{display:inline-block;font-size:10px;padding:0 5px;border-radius:2px;margin-right:5px;vertical-align:1px;letter-spacing:1px}
.ob.formula{border:1px solid var(--line-2);color:var(--fg-3)}
.ob.authored{border:1px solid var(--gold-3);color:var(--gold)}
.ob.live{border:1px solid var(--up);color:var(--up)}
.ipolegacy{margin-top:6px;font-size:11px;color:var(--fg-3);font-family:'JetBrains Mono',monospace}
.vaxrow{display:flex;gap:10px;margin:8px 0 2px;font-size:12px;font-family:'JetBrains Mono',monospace}
.vaxrow span{padding:3px 10px;border:1px solid var(--line-2);border-radius:2px;color:var(--fg-1)}
.vaxrow .va{border-color:var(--gold-3);color:var(--gold)}
/* ── single 五段式（标杆单图页）── */
.mapsw{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0 4px}
.mapsw a{display:inline-block;padding:6px 12px;border:1px solid var(--line-2);border-radius:2px;
  font-size:11.5px;color:var(--fg-2);background:var(--ink-1)}
.mapsw a.on{border-color:var(--gold-3);color:var(--gold);background:rgba(201,169,106,.07)}
.mapsw a .tier{font-family:'JetBrains Mono',monospace;font-size:9.5px;color:var(--fg-3);margin-left:6px}
.scoreband{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0;font-family:'JetBrains Mono',monospace}
.scoreband .ax{padding:8px 14px;border:1px solid var(--line-2);border-radius:2px;background:var(--ink-1);
  font-size:12px;color:var(--fg-1)}
.scoreband .ax b{font-size:17px;color:var(--gold);font-weight:600;margin-left:6px}
.scoreband .ax.mn{border-color:var(--gold-3)}
.metrics{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 2px;font-family:'JetBrains Mono',monospace;
  font-size:10.5px;color:var(--fg-2)}
.metrics span{border:1px solid var(--line-1);padding:3px 9px;border-radius:2px}
.sgrid{display:grid;grid-template-columns:148px repeat(3,1fr);gap:9px;margin-top:10px}
.sgh{padding:8px 4px 6px;font-family:'Noto Serif SC',serif;font-size:12.5px;color:var(--gold);
  border-bottom:1px solid var(--gold-3)}
.sgh .e{display:block;font-family:'Inter',sans-serif;font-size:9px;color:var(--fg-3);margin-top:2px}
.sgd{padding:10px 8px;font-family:'Noto Serif SC',serif;font-size:13px;color:var(--fg-0)}
.sgd .de{font-size:9.5px;color:var(--fg-3);font-family:'JetBrains Mono',monospace;margin-top:3px;line-height:1.5}
.nextol{margin:6px 0 0;padding-left:20px}
.nextol li{font-size:12.5px;color:var(--fg-1);line-height:2;margin:4px 0}
.nextol li b{color:var(--gold)}
@media(max-width:860px){.sgrid{grid-template-columns:1fr}.sgh{display:none}}
/* ── 距100分 ── */
.g100{margin:4px 0}
.g100 li{font-size:12px;color:var(--fg-1);line-height:1.9;list-style:none;position:relative;padding-left:16px}
.g100 li::before{content:"▸";position:absolute;left:0;color:var(--down)}
.g100 li.nb::before{color:var(--gold)}
.g100 li.nb{color:var(--gold)}
.g100sec{margin:26px 0 8px;padding:14px 16px;border:1px solid var(--line-2);background:var(--ink-1)}
.g100sec .hs{margin-top:0}
.g100sec .gcell{font-family:'JetBrains Mono',monospace;color:var(--fg-2);font-size:11px;margin-top:8px}
'''


def esc(s):
    return html.escape(str(s if s is not None else ''), quote=True)


MAT = {'rich': ('🟢 丰富', 'var(--up)'), 'partial': ('🟡 部分', 'var(--hot)'),
       'gap': ('🔴 战略空白', 'var(--down)'), 'built': ('🟢 已建成', 'var(--gold)')}
HEATC = {'h5': 'var(--gold)', 'h4': 'var(--hot)', 'h3': 'var(--cold)', 'h2': 'var(--fg-2)', 'h0': 'var(--fg-3)'}


def heat(pri):
    return 'h5' if pri >= 20 else 'h4' if pri >= 15 else 'h3' if pri >= 10 else 'h2' if pri >= 5 else 'h0'


def head(title, desc=''):
    return ('<!DOCTYPE html><html lang="zh"><head>' + GATE
            + '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            + '<meta name="robots" content="noindex">'
            + (f'<meta name="description" content="{esc(desc)}">' if desc else '')
            + f'<title>{esc(title)}</title>'
            + '<style>' + CSS + EXTRA_CSS + '</style></head>')


def nav(domains, active=''):
    """active: 'index' | 'capability' | <domain id> | 'judgment' | 页面名。"""
    def a(href, label, key, style=''):
        on = ' class="on"' if key == active else ' class=""'
        st = f' style="{style}"' if style else ''
        return f'<a href="{href}"{on}{st}>{label}</a>'
    parts = ['<nav class="nav"><a href="index.html" class="brand">Org-Capability Map</a>']
    parts.append(a('index.html', '版图', 'index'))
    parts.append(a('capability.html', '能力总图', 'capability'))
    for d in domains:
        parts.append(a(f'{d[0]}.html', d[1], d[0]))
    parts.append(a('capability-judgment.html', '判断书', 'judgment', 'color:var(--gold-2)'))
    parts.append(a('playbook.html', '实操攻略', 'playbook', 'color:var(--gold-2)'))
    parts.append(a('deliverables.html', '交付物', 'deliverables', 'color:var(--gold-2)'))
    parts.append(a('maps-audit.html', '记分卡', 'audit', 'color:var(--gold-2)'))
    parts.append(a('atlas.html', '全信息', 'atlas', 'color:var(--gold)'))
    parts.append('<span class="right">本OS组织能力 CBM · your-site</span></nav>')
    return ''.join(parts)


def honesty_banner(scored, scope_cells=None):
    """诚实横幅：无金卡 + authored 覆盖 + ⚪占比。scope_cells 给出时按域收窄口径。"""
    cells = scope_cells if scope_cells is not None else scored['cells']
    n_auth = sum(int(r['authored_coverage'].split('/')[0]) for r in cells)
    n_leaf = sum(int(r['authored_coverage'].split('/')[1]) for r in cells)
    gold = sum(1 for r in cells if r['gold'])
    pct = (n_auth / n_leaf * 100) if n_leaf else 0
    scope = f'本域 {len(cells)} 格' if scope_cells is not None else f"全图 {len(cells)} 格"
    return (f'<div class="hb"><b>⚠ 本图无金卡</b> — {scope}无一格四门全pass且va=5（金卡须 weekly gold_attest 人证）'
            f' · <span class="m">递归三五三 authored {n_auth}/{n_leaf} 叶（{pct:.1f}%），其余公式默认⚪</span>'
            f' · 评分门+棘轮在位（{esc(scored["scored_at"])} · 引擎 ops/card_triangle_scorer.py）'
            + (f' · 金卡格 {gold}' if gold else '') + '</div>')
