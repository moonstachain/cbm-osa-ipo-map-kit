#!/bin/sh
# 通用部署示例：把 site/ 发到你自己的静态托管（换成 rsync/scp/对象存储均可）。
# 部署前三道门：评分门 → 无门页扫描 → 泄漏扫描。任何一道 FAIL 都不发布。
set -eu
python3 ops/card_triangle_scorer.py --all --check
python3 build/build_maps.py --all
for f in site/*.html; do
  grep -q 'MAPKIT_GATE_V1' "$f" || { echo "GATELESS PAGE, abort: $f"; exit 1; }
done
grep -q 'CHANGE_ME_SHA256' build/templates/gate.frag && {
  echo "⚠ 门体 HASH 仍是占位符——生成你的口令哈希后再上线（README·访问门）"; exit 1; }
# rsync -av site/ user@host:/var/www/mymap/    # ← 换成你的托管
echo "local build ok — 接上你的托管命令后取消注释"
