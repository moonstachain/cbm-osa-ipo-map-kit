"""Lossless v1/APM migration into the OSA v2 dual-read shape."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Iterable

from .constants import CONTRACT_ID, ENGINE_VERSION
from .engine import contract_sha256


TECHNICAL_HINTS = (
    "技术", "代码", "接口", "api", "agent", "自动化", "模型", "mvp", "端到端", "可行性",
)
ARCHETYPE_HINTS = (
    "我是谁", "人格", "原型人格", "荣格", "禀赋", "天赋", "贵问题", "自我认知",
)


def classify_prototype_hypothesis(text: str) -> str:
    lowered = text.lower()
    technical = any(token in lowered for token in TECHNICAL_HINTS)
    archetype = any(token in lowered for token in ARCHETYPE_HINTS)
    if technical and not archetype:
        return "technical_feasibility_hypothesis"
    if archetype and not technical:
        return "archetype_hypothesis"
    return "needs_ruling"


def _walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)


def _text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() or None
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _legacy_actions(legacy: dict[str, Any]) -> list[dict[str, Any]]:
    raw = legacy.get("Action", legacy.get("action"))
    if raw in (None, "", []):
        return []
    rows = raw if isinstance(raw, list) else [raw]
    return [
        {
            "action_id": f"legacy-action-{index}",
            "statement": _text(row) or "legacy action requires ruling",
            "owner": None,
            "start_at": None,
            "due_at": None,
            "measurable_result": None,
            "sop_version": None,
            "agent_permissions": [],
            "human_gate": {"required": True, "owner": None, "conditions": []},
            "outputs": [],
            "run_receipt_refs": [],
            "feedback_receipt_refs": [],
            "changed_rule_receipt_ref": None,
            "autonomous_planning": False,
            "rollback": None,
        }
        for index, row in enumerate(rows, 1)
    ]


def _empty_information_engine() -> dict[str, Any]:
    unassessed_gate = {"status": "unassessed", "evidence_refs": []}
    return {
        "input": {
            "source_refs": [],
            "coverage_dimensions": [],
            "complete": copy.deepcopy(unassessed_gate),
            "authentic_first_hand": copy.deepcopy(unassessed_gate),
            "granular": copy.deepcopy(unassessed_gate),
        },
        "process": {"level": "unassessed", "artifacts": [], "method_refs": []},
        "output": {
            "decision_pointers": ["/objective", "/strategies", "/actions"],
            "closed_loop": copy.deepcopy(unassessed_gate),
            "automated": copy.deepcopy(unassessed_gate),
            "intelligent": copy.deepcopy(unassessed_gate),
        },
        "feedback": {"result_refs": [], "next_input_refs": [], "incorporated_at": None},
    }


def _legacy_recursive_ipo(legacy: dict[str, Any]) -> dict[str, Any] | None:
    """Extract old O/S/A IPO payloads without interpreting or scoring them."""
    containers = []
    for key in ("osa", "OSA"):
        if isinstance(legacy.get(key), dict):
            containers.append(legacy[key])
    containers.append(legacy)
    extracted: dict[str, Any] = {}
    for axis in ("O", "S", "A"):
        for container in containers:
            row = container.get(axis, container.get(axis.lower()))
            if isinstance(row, dict) and "ipo" in row:
                extracted[axis] = copy.deepcopy(row["ipo"])
                break
    return extracted or None


def _candidate_evidence_refs(value: Any, path: str = "$") -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            lowered = key.lower()
            if lowered.endswith("_ref") and isinstance(child, str) and child:
                rows.append({"path": child_path, "value": child})
            elif lowered.endswith("_refs") and isinstance(child, list):
                rows.extend(
                    {"path": f"{child_path}[{index}]", "value": ref}
                    for index, ref in enumerate(child) if isinstance(ref, str) and ref
                )
            rows.extend(_candidate_evidence_refs(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(_candidate_evidence_refs(child, f"{path}[{index}]"))
    return rows


def migrate_v1(
    legacy: dict[str, Any], *, card_id: str | None = None,
    classification: str = "internal",
) -> dict[str, Any]:
    """Preserve the v1 payload and create a fail-closed v2 dual-read card.

    ``Situation`` is copied only to ``context.situation``.  It is deliberately
    never converted into a Strategy.  Old maturity values remain inside
    ``legacy_v1`` and all v2 calibration axes start as ``unassessed``.
    """
    payload_hash = hashlib.sha256(
        json.dumps(legacy, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    migrations = []
    seen = set()
    for text in _walk_strings(legacy):
        if "原型假设" not in text or text in seen:
            continue
        seen.add(text)
        classification_result = classify_prototype_hypothesis(text)
        migrations.append({
            "original_term": text,
            "classification": classification_result,
            "status": "needs_ruling" if classification_result == "needs_ruling" else "migrated",
        })

    situation = legacy.get("Situation", legacy.get("situation"))
    objective = legacy.get("Objective", legacy.get("objective"))
    needs_ruling = any(row["status"] == "needs_ruling" for row in migrations)
    legacy_copy = copy.deepcopy(legacy)
    legacy_copy["legacy_recursive_ipo"] = _legacy_recursive_ipo(legacy)
    legacy_copy["migration_report"] = {
        "candidate_evidence_refs": _candidate_evidence_refs(legacy),
        "binding_status": "human_review_required",
        "scoring_status": "ignored_by_v2",
    }
    return {
        "contract": CONTRACT_ID,
        "card_id": card_id or legacy.get("apm_card_id") or f"legacy-{payload_hash[:16]}",
        "version": "2.0",
        "status": "draft",
        "context": {
            "situation": _text(situation),
            "cbm_domain": None,
            "cbm_layer": None,
            "parent_card_id": None,
            "hypothesis_migrations": migrations,
        },
        "information_engine": _empty_information_engine(),
        "objective": {
            "statement": _text(objective),
            "candidate_goals": [],
            "selected_candidate_id": None,
            "goal_model": None,
            "baseline": None,
            "metrics": [],
            "target_value": None,
            "deadline": None,
            "constraints": [],
            "evidence_refs": [],
            "global_optimum_basis": None,
        },
        "strategies": [],
        "actions": _legacy_actions(legacy),
        "calibration": {"O": "unassessed", "S": "unassessed", "A": "unassessed"},
        "evidence": {"items": []},
        "governance": {
            "classification": classification,
            "boundary": "historical_read_only" if legacy.get("status") == "retired" else "internal_dry_run",
            "wip_limit": 1,
            "human_approval": {
                "approved": False,
                "approval_ref": None,
                "approved_by": None,
                "approved_at": None,
            },
            "privacy_reviewed": False,
            "engine_pin": {
                "repository": "moonstachain/cbm-osa-ipo-map-kit",
                "commit": None,
                "package": "yuanli-osa-card",
                "version": ENGINE_VERSION,
            },
            "contract_sha256": contract_sha256(),
            "migration_state": "needs_ruling" if needs_ruling else "dual_read",
            "weekly_cycle_id": None,
        },
        "legacy_v1": legacy_copy,
    }
