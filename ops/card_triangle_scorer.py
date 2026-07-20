#!/usr/bin/env python3
"""Thin v1 compatibility CLI; all scoring logic lives in yuanli_osa_card."""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from map_loader import (  # noqa: E402
    ROOT as MAP_ROOT,
    list_maps as _local_list_maps,
    load_map as _local_load_map,
)
from yuanli_osa_card import legacy_map_engine as _engine  # noqa: E402
from yuanli_osa_card.legacy_map_engine import *  # noqa: F401,F403,E402

_engine.configure_legacy(MAP_ROOT, _local_list_maps, _local_load_map)


if __name__ == "__main__":
    _engine.main()
