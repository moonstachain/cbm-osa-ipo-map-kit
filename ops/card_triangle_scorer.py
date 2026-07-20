#!/usr/bin/env python3
"""Retired v1 scoring entrypoint.

The implementation remains in repository history for evidence replay.  Active
calibration must use ``yuanli-osa-card/v2`` and its single shared
``information_engine``.  This tombstone deliberately has no compatibility
switch: restoring the old scorer would recreate an active O/S/A-owned IPO
consumer after the dual-read sunset.
"""

from __future__ import annotations

import json


RETIREMENT = {
    "schema": "yuanli-legacy-scorer-retired/v1",
    "status": "retired",
    "reason": "post_dual_read_sunset",
    "merge_precondition": "two_countable_weekly_cycles_completed",
    "replacement": "yuanli-osa-card validate/score",
    "contract": "yuanli-osa-card/v2",
    "engine_commit": "873f9e2f33e06dcbb896f46fe06bc7ba0f5288d0",
    "schema_sha256": "d229df1e18ec8bd1fa2325ec3a1d11f3d124416d839368a5dfe0115e05b91268",
}


def main() -> int:
    print(json.dumps(RETIREMENT, ensure_ascii=False, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
