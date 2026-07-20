#!/bin/sh
# 通用 v2 验证示例。旧地图 scorer 已退休；新卡只允许调用锁定的
# yuanli-osa-card/v2 合同与统一 information_engine。
set -eu
python3 -m pip install -e .
yuanli-osa-card validate examples/xiaoyuan-public-content-experiment.v2.json
yuanli-osa-card score examples/xiaoyuan-public-content-experiment.v2.json >/dev/null
test "$(yuanli-osa-card schema-hash)" = \
  "d229df1e18ec8bd1fa2325ec3a1d11f3d124416d839368a5dfe0115e05b91268"
echo "v2 contract verified — publication remains a separate gated step"
