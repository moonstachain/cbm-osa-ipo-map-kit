"""Package-owned conformance fixtures shared by every OSA v2 consumer."""

from __future__ import annotations

import importlib.resources
import json
from typing import Any


GOLDEN_FIXTURE_NAME = "golden-unassessed-v2.json"


def load_golden_fixture() -> dict[str, Any]:
    """Load a fresh copy of the single cross-repository golden fixture."""
    payload = importlib.resources.files(__package__).joinpath(GOLDEN_FIXTURE_NAME).read_text(
        encoding="utf-8"
    )
    return json.loads(payload)


__all__ = ["GOLDEN_FIXTURE_NAME", "load_golden_fixture"]
