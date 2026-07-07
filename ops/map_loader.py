#!/usr/bin/env python3
"""cellcard-v1 弹夹装载器：把 data/maps/<map_id>/ 的 map.py 或 map.json 归一为同一 dict 契约。

打分器与渲染器只认本装载器输出的契约，不认文件形态：
  {'MAP': {...}, 'LAYERS': [[id,名,说明],...], 'DOMAINS': [[id,名,英,成熟度,组件数,桥,blurb],...],
   'CELLS': [cell,...], 'source_hash': sha256, 'source_path': ...}
cell 契约见 data/maps/org-kernel/map.py 头注（flat 必填；osa/gates_authored/gold_attest/live/next_battle 可选）。
"""
import hashlib
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS_DIR = os.path.join(ROOT, 'data', 'maps')

FLAT_REQUIRED = ('o', 's', 'a', 'v', 'status', 'gap', 'delegates', 'reuse')
O_VALUES = ('L1', 'L2', 'L3', 'L4', 'L5')
S_VALUES = ('C', 'B', 'A', 'S')
A_VALUES = ('A0', 'A1', 'A2', 'A3')
STATUS_VALUES = ('operating', 'stable', 'draft', 'concept')
DEFAULT_LAYERS = [['direct', 'Direct 定向', '关键判断（靠人脑的决策点）'],
                  ['control', 'Control 管控', '管理保障（确保质量的检查点）'],
                  ['execute', 'Execute 执行', '自动化流水（可规模化的动作）']]


def list_maps():
    if not os.path.isdir(MAPS_DIR):
        return []
    return sorted(d for d in os.listdir(MAPS_DIR)
                  if not d.startswith('_') and os.path.isdir(os.path.join(MAPS_DIR, d))
                  and (os.path.exists(os.path.join(MAPS_DIR, d, 'map.py'))
                       or os.path.exists(os.path.join(MAPS_DIR, d, 'map.json'))))


def _validate(m, path):
    assert isinstance(m.get('MAP'), dict) and m['MAP'].get('map_id'), f'{path}: MAP/map_id 缺失'
    cells = m.get('CELLS')
    assert isinstance(cells, list) and cells, f'{path}: CELLS 空'
    dom_ids = {d[0] for d in m['DOMAINS']}
    lay_ids = {l[0] for l in m['LAYERS']}
    ids = set()
    for c in cells:
        cid = c.get('cell_id')
        assert cid and cid not in ids, f'{path}: cell_id 缺失或重复 {cid}'
        ids.add(cid)
        assert c.get('domain') in dom_ids, f'{cid}: 域 {c.get("domain")} 不在 DOMAINS'
        assert c.get('layer') in lay_ids, f'{cid}: 层 {c.get("layer")} 非法'
        f = c.get('flat')
        assert isinstance(f, dict), f'{cid}: flat 缺失'
        for k in FLAT_REQUIRED:
            assert k in f, f'{cid}: flat.{k} 缺失'
        assert f['o'] in O_VALUES and f['s'] in S_VALUES and f['a'] in A_VALUES, f'{cid}: flat 轴非法'
        assert f['status'] in STATUS_VALUES, f'{cid}: status 非法'
        assert isinstance(f['delegates'], list), f'{cid}: delegates 须为 list'
        assert 1 <= int(f['v']) <= 5, f'{cid}: v 越界'
        osa = c.get('osa')
        if osa:
            for seg in ('O', 'S', 'A'):
                assert seg in osa, f'{cid}: osa 缺 {seg} 段'
        for lv in c.get('live') or []:
            assert lv.get('src') and lv.get('probe') and str(lv.get('target', '')).startswith('osa.'), \
                f'{cid}: live 绑定非法 {lv}'
    return m


def load_map(map_id):
    d = os.path.join(MAPS_DIR, map_id)
    py, js = os.path.join(d, 'map.py'), os.path.join(d, 'map.json')
    if os.path.exists(py):
        spec = importlib.util.spec_from_file_location(f'map_{map_id.replace("-", "_")}', py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        raw, path = {
            'MAP': dict(mod.MAP),
            'LAYERS': [list(x) for x in getattr(mod, 'LAYERS', DEFAULT_LAYERS)],
            'DOMAINS': [list(x) for x in mod.DOMAINS],
            'CELLS': [dict(c) for c in mod.CELLS],
        }, py
    elif os.path.exists(js):
        j = json.load(open(js))
        raw, path = {
            'MAP': j['MAP'],
            'LAYERS': j.get('LAYERS', DEFAULT_LAYERS),
            'DOMAINS': j['DOMAINS'],
            'CELLS': j['CELLS'],
        }, js
    else:
        raise FileNotFoundError(f'弹夹不存在: {d}/map.(py|json)')
    raw['source_path'] = path
    raw['source_hash'] = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    return _validate(raw, path)


if __name__ == '__main__':
    for mid in list_maps():
        m = load_map(mid)
        print(f"{mid}: {len(m['CELLS'])}格/{len(m['DOMAINS'])}域 · {m['source_hash'][:12]} · {m['source_path']}")
