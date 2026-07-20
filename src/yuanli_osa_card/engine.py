"""Fail-closed evaluator for ``yuanli-osa-card/v2``.

The engine never promotes a card.  It computes an evidence-supported ceiling,
compares it with the human-declared calibration, and exposes an effective grade
only when a production card carries a current human approval receipt.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker

from .constants import (
    A_LEVELS,
    CONTRACT_ID,
    ENGINE_ID,
    ENGINE_VERSION,
    O_LEVELS,
    RANKS,
    S_LEVELS,
)


SCHEMA_PATH = Path(__file__).parent / "schema" / "yuanli-osa-card-v2.schema.json"
IPO_PROCESS_LEVELS = ("unassessed", "L1", "L2", "L3", "L4", "L5")
IPO_PROCESS_RANKS = {level: rank for rank, level in enumerate(IPO_PROCESS_LEVELS)}


class CardValidationError(ValueError):
    """Raised when the machine contract or a hard semantic invariant fails."""

    def __init__(self, errors: list[dict[str, str]]):
        self.errors = errors
        super().__init__("; ".join(f"{row['code']}@{row['path']}" for row in errors))


@dataclass(frozen=True)
class EvidenceIndex:
    rows: dict[str, dict[str, Any]]

    def trusted(self, refs: Iterable[str], *, kind: str | None = None) -> bool:
        refs = list(refs)
        if not refs:
            return False
        for ref in refs:
            row = self.rows.get(ref)
            if not row:
                return False
            if kind is not None and row.get("kind") != kind:
                return False
            if row.get("authenticity") != "verified_real":
                return False
            if not row.get("current") or row.get("conflicted"):
                return False
        return True


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def contract_sha256() -> str:
    return hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest()


def _schema_errors(card: dict[str, Any]) -> list[dict[str, str]]:
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    rows = []
    for error in sorted(validator.iter_errors(card), key=lambda item: list(item.absolute_path)):
        path = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}"
            for part in error.absolute_path
        )
        rows.append({"code": "schema_invalid", "path": path, "message": error.message})
    return rows


def _error(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _privacy_errors(card: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    forbidden_keys = {
        "api_key", "access_token", "password", "cookie", "secret",
        "raw_payload", "customer_name", "phone", "email", "local_path",
    }
    secret_pattern = re.compile(
        r"(?:/Users/|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
        r"(?i:api[_-]?key|access[_-]?token|password|cookie)\s*[:=]\s*[^\s]{8,})"
    )

    def walk(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}"
                if key.lower() in forbidden_keys:
                    errors.append(_error("privacy_field_forbidden", child_path, "sensitive field is not part of the public contract"))
                walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")
        elif isinstance(value, str) and secret_pattern.search(value):
            errors.append(_error("privacy_value_forbidden", path, "secret or local-path pattern detected"))

    walk(card)
    if card.get("governance", {}).get("classification") == "public":
        for index, row in enumerate(card.get("evidence", {}).get("items", [])):
            if row.get("privacy") != "public":
                errors.append(_error(
                    "private_evidence_in_public_card",
                    f"$.evidence.items[{index}].privacy",
                    "public cards may expose only public evidence metadata",
                ))
    return errors


def _gate_supported(
    gate: dict[str, Any], evidence: EvidenceIndex, *, kind: str | None = None
) -> bool:
    return gate.get("status") == "pass" and evidence.trusted(
        gate.get("evidence_refs", []), kind=kind
    )


def _information_refs(card: dict[str, Any]) -> set[str]:
    engine = card["information_engine"]
    refs = set(engine["input"]["source_refs"])
    for key in ("complete", "authentic_first_hand", "granular"):
        refs.update(engine["input"][key]["evidence_refs"])
    for artifact in engine["process"]["artifacts"]:
        refs.update(artifact["evidence_refs"])
    refs.update(engine["process"]["method_refs"])
    for key in ("closed_loop", "automated", "intelligent"):
        refs.update(engine["output"][key]["evidence_refs"])
    refs.update(engine["feedback"]["result_refs"])
    refs.update(engine["feedback"]["next_input_refs"])
    return refs


def _information_engine(
    card: dict[str, Any], evidence: EvidenceIndex, gaps: list[str]
) -> dict[str, Any]:
    engine = card["information_engine"]
    input_contract = engine["input"]
    input_gates = {
        key: _gate_supported(input_contract[key], evidence, kind="source")
        for key in ("complete", "authentic_first_hand", "granular")
    }
    sources_trusted = evidence.trusted(input_contract["source_refs"], kind="source")
    input_verified = bool(input_contract["coverage_dimensions"]) and sources_trusted and all(input_gates.values())
    if not input_verified:
        gaps.append("IPO/I: full, authentic first-hand, granular source coverage is not verified")

    artifacts_by_level: dict[str, list[dict[str, Any]]] = {
        level: [row for row in engine["process"]["artifacts"] if row["level"] == level]
        for level in IPO_PROCESS_LEVELS[1:]
    }
    process_supported = "unassessed"
    for level in IPO_PROCESS_LEVELS[1:]:
        rows = artifacts_by_level[level]
        if len(rows) != 1 or not evidence.trusted(rows[0]["evidence_refs"]):
            break
        process_supported = level
    methods_trusted = evidence.trusted(engine["process"]["method_refs"])
    if process_supported == "L5" and not methods_trusted:
        process_supported = "L4"
        gaps.append("IPO/P: L5 requires a verified processing-method reference")
    if process_supported != "L5":
        gaps.append("IPO/P: the shared information process has not reached evidenced L5 without skipping")

    output_contract = engine["output"]
    output_gates = {
        "closed_loop": _gate_supported(output_contract["closed_loop"], evidence, kind="feedback_receipt"),
        "automated": _gate_supported(output_contract["automated"], evidence, kind="action_receipt"),
        "intelligent": _gate_supported(output_contract["intelligent"], evidence, kind="changed_rule"),
    }
    if not all(output_gates.values()):
        gaps.append("IPO/O: closed-loop, automated, and intelligent output evidence is incomplete")

    feedback = engine["feedback"]
    feedback_verified = bool(
        feedback.get("incorporated_at")
        and evidence.trusted(feedback["result_refs"], kind="feedback_receipt")
        and evidence.trusted(feedback["next_input_refs"])
    )
    if not feedback_verified:
        gaps.append("IPO/feedback: reality results have not been incorporated as next-round input")

    verified = bool(
        input_verified
        and process_supported == "L5"
        and all(output_gates.values())
        and feedback_verified
    )
    return {
        "input": {
            "verified": input_verified,
            "sources_trusted": sources_trusted,
            "gates": input_gates,
        },
        "process": {
            "declared": engine["process"]["level"],
            "supported_level": process_supported,
            "methods_trusted": methods_trusted,
        },
        "output": {"verified": all(output_gates.values()), "gates": output_gates},
        "feedback": {"verified": feedback_verified},
        "verified": verified,
    }


def _objective_ceiling(
    card: dict[str, Any], evidence: EvidenceIndex, gaps: list[str], process_ceiling: str
) -> str:
    objective = card["objective"]
    ceiling = "unassessed"
    if objective.get("statement"):
        ceiling = "L1"
    if ceiling != "unassessed" and objective.get("metrics") and objective.get("baseline") is not None:
        ceiling = "L2"
    if ceiling == "L2" and objective.get("goal_model"):
        ceiling = "L3"

    candidates = objective.get("candidate_goals", [])
    candidate_ids = [row.get("candidate_id") for row in candidates]
    selected = objective.get("selected_candidate_id")
    comparison_ready = (
        len(candidates) >= 3
        and len(set(candidate_ids)) == len(candidate_ids)
        and selected in candidate_ids
        and bool(objective.get("constraints"))
        and bool(objective.get("global_optimum_basis"))
    )
    if ceiling == "L3" and comparison_ready:
        ceiling = "L4"
    if ceiling == "L4" and all([
        objective.get("target_value") is not None,
        objective.get("deadline"),
        evidence.trusted(objective.get("evidence_refs", [])),
    ]):
        ceiling = "L5"

    if len(candidates) < 3:
        gaps.append("O: fewer than three candidate goals")
    if selected and selected not in candidate_ids:
        gaps.append("O: selected_candidate_id is not in candidate_goals")
    if not evidence.trusted(objective.get("evidence_refs", [])):
        gaps.append("O: objective evidence is missing, stale, conflicted, or not verified_real")
    if RANKS["O"][ceiling] > IPO_PROCESS_RANKS[process_ceiling]:
        ceiling = process_ceiling
        gaps.append(f"O: objective maturity is capped by the shared IPO Process at {process_ceiling}")
    return ceiling


def _experiment_has_outcome(experiment: dict[str, Any], allowed: set[str]) -> bool:
    kinds = {metric.get("kind") for metric in experiment.get("metrics", [])}
    return bool(kinds & allowed)


def _strategy_ceiling(
    strategy: dict[str, Any], evidence: EvidenceIndex, gaps: list[str]
) -> str:
    ceiling = "C"
    experiments = strategy.get("experiments", [])
    passed_technical = [
        row for row in experiments
        if row["stage"] == "technical_feasibility" and row["status"] == "passed"
        and row.get("result") is not None and row.get("reproducible") is True
        and evidence.trusted(row.get("receipt_refs", []), kind="experiment_receipt")
    ]
    if passed_technical:
        ceiling = "B"

    passed_value = [
        row for row in experiments
        if row["stage"] == "value_validation" and row["status"] == "passed"
        and row.get("result") is not None
        and _experiment_has_outcome(row, {"outcome"})
        and evidence.trusted(row.get("receipt_refs", []), kind="experiment_receipt")
    ]
    if ceiling == "B" and passed_value:
        ceiling = "A"

    passed_growth = [
        row for row in experiments
        if row["stage"] == "growth_validation" and row["status"] == "passed"
        and row.get("result") is not None
        and row.get("reproducible") is True and row.get("attributable") is True
        and row.get("comparable_cycle_id")
        and _experiment_has_outcome(row, {"outcome", "growth"})
        and evidence.trusted(row.get("receipt_refs", []), kind="experiment_receipt")
    ]
    cycles = {row["comparable_cycle_id"] for row in passed_growth}
    if ceiling == "A" and len(cycles) >= 3:
        ceiling = "S"

    if any(row["stage"] == "value_validation" and row["status"] == "passed" for row in experiments) and not passed_value:
        gaps.append(f"S/{strategy['strategy_id']}: value validation lacks a verified real outcome metric; vanity metrics do not qualify")
    if any(row["stage"] == "growth_validation" and row["status"] == "passed" for row in experiments) and len(cycles) < 3:
        gaps.append(f"S/{strategy['strategy_id']}: fewer than three verified comparable growth cycles")
    if not passed_technical:
        gaps.append(f"S/{strategy['strategy_id']}: no reproducible technical feasibility receipt")
    return ceiling


def _strategy_calibration(
    card: dict[str, Any], evidence: EvidenceIndex, gaps: list[str]
) -> tuple[str, dict[str, str]]:
    strategies = card.get("strategies", [])
    if not strategies:
        gaps.append("S: no Strategy exists; legacy Situation is context, not Strategy")
        return "unassessed", {}
    ceilings = {
        strategy["strategy_id"]: _strategy_ceiling(strategy, evidence, gaps)
        for strategy in strategies
    }
    return max(ceilings.values(), key=RANKS["S"].get), ceilings


def _smart(action: dict[str, Any]) -> bool:
    return all([
        action.get("statement"), action.get("owner"), action.get("start_at"),
        action.get("due_at"), action.get("measurable_result"),
        action.get("sop_version"), action.get("outputs"),
    ])


def _action_ceiling(action: dict[str, Any], evidence: EvidenceIndex, gaps: list[str]) -> str:
    ceiling = "A0"
    if _smart(action):
        ceiling = "A1"
    if ceiling == "A1" and evidence.trusted(action.get("run_receipt_refs", []), kind="action_receipt"):
        ceiling = "A2"
    changed_ref = action.get("changed_rule_receipt_ref")
    gate = action.get("human_gate", {})
    if ceiling == "A2" and all([
        action.get("autonomous_planning") is True,
        evidence.trusted(action.get("feedback_receipt_refs", []), kind="feedback_receipt"),
        changed_ref and evidence.trusted([changed_ref], kind="changed_rule"),
        gate.get("required") is True,
        gate.get("owner"),
        gate.get("conditions"),
        action.get("rollback"),
    ]):
        ceiling = "A3"
    if ceiling != "A3" and action.get("autonomous_planning"):
        gaps.append(f"A/{action['action_id']}: AI self-driving requires run, feedback, changed_rule, Human Gate, and rollback receipts")
    return ceiling


def _action_calibration(
    card: dict[str, Any], evidence: EvidenceIndex, gaps: list[str]
) -> tuple[str, dict[str, str]]:
    actions = card.get("actions", [])
    if not actions:
        gaps.append("A: no SMART action contract")
        return "unassessed", {}
    ceilings = {
        action["action_id"]: _action_ceiling(action, evidence, gaps)
        for action in actions
    }
    return min(ceilings.values(), key=RANKS["A"].get), ceilings


def _semantic_errors(card: dict[str, Any], result: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for collection in ("strategies", "actions"):
        key = "strategy_id" if collection == "strategies" else "action_id"
        for index, row in enumerate(card[collection]):
            value = row[key]
            if value in seen_ids:
                errors.append(_error("duplicate_id", f"$.{collection}[{index}].{key}", "card identifiers must be unique"))
            seen_ids.add(value)

    active_total = 0
    for s_index, strategy in enumerate(card["strategies"]):
        running = [row for row in strategy["experiments"] if row["status"] == "running"]
        active_total += len(running)
        if len(running) > 1:
            errors.append(_error(
                "strategy_wip_exceeded", f"$.strategies[{s_index}].experiments",
                "one strategy may run at most one stage experiment",
            ))
        stages_passed = {row["stage"] for row in strategy["experiments"] if row["status"] == "passed"}
        if "value_validation" in stages_passed and "technical_feasibility" not in stages_passed:
            errors.append(_error("experiment_stage_skipped", f"$.strategies[{s_index}].experiments", "value validation cannot pass before technical feasibility"))
        if "growth_validation" in stages_passed and "value_validation" not in stages_passed:
            errors.append(_error("experiment_stage_skipped", f"$.strategies[{s_index}].experiments", "growth validation cannot pass before value validation"))
    if active_total > card["governance"]["wip_limit"]:
        errors.append(_error("project_wip_exceeded", "$.governance.wip_limit", "running experiments exceed project WIP"))

    process = card["information_engine"]["process"]
    artifact_levels = [row["level"] for row in process["artifacts"]]
    if len(artifact_levels) != len(set(artifact_levels)):
        errors.append(_error(
            "ipo_process_duplicate_level", "$.information_engine.process.artifacts",
            "the shared IPO Process may contain at most one artifact per information level",
        ))
    if artifact_levels:
        highest = max(IPO_PROCESS_RANKS[level] for level in artifact_levels)
        required = set(IPO_PROCESS_LEVELS[1:highest + 1])
        if set(artifact_levels) != required:
            errors.append(_error(
                "ipo_process_level_skipped", "$.information_engine.process.artifacts",
                "IPO Process artifacts must form one contiguous L1-L5 sequence",
            ))
    process_supported = result["information_engine"]["process"]["supported_level"]
    if IPO_PROCESS_RANKS[process["level"]] > IPO_PROCESS_RANKS[process_supported]:
        errors.append(_error(
            "ipo_process_exceeds_evidence", "$.information_engine.process.level",
            f"declared {process['level']} exceeds evidence-supported {process_supported}",
        ))

    for axis in ("O", "S", "A"):
        declared = card["calibration"][axis]
        ceiling = result["calibration"][axis]["supported_ceiling"]
        if RANKS[axis][declared] > RANKS[axis][ceiling]:
            errors.append(_error(
                "calibration_exceeds_evidence",
                f"$.calibration.{axis}",
                f"declared {declared} exceeds evidence-supported {ceiling}",
            ))

    approval = card["governance"]["human_approval"]
    if any(card["calibration"][axis] != "unassessed" for axis in ("O", "S", "A")):
        if not approval.get("approved"):
            errors.append(_error("human_approval_missing", "$.governance.human_approval", "AI may propose grades but cannot approve them"))
    if approval.get("approved"):
        ref = approval.get("approval_ref")
        evidence = EvidenceIndex({row["evidence_id"]: row for row in card["evidence"]["items"]})
        if not ref or not evidence.trusted([ref], kind="approval"):
            errors.append(_error("approval_receipt_invalid", "$.governance.human_approval.approval_ref", "approval requires a current verified_real approval receipt"))
    if card["governance"].get("contract_sha256") not in (None, contract_sha256()):
        errors.append(_error("contract_hash_mismatch", "$.governance.contract_sha256", "card is pinned to a different contract"))
    return errors


def evaluate_card(card: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic, fail-closed evaluation without mutating ``card``."""
    errors = _schema_errors(card)
    errors.extend(_privacy_errors(card))
    if errors:
        raise CardValidationError(errors)

    evidence_rows = {row["evidence_id"]: row for row in card["evidence"]["items"]}
    evidence = EvidenceIndex(evidence_rows)
    gaps: list[str] = []
    information_engine = _information_engine(card, evidence, gaps)
    o_ceiling = _objective_ceiling(
        card, evidence, gaps, information_engine["process"]["supported_level"]
    )
    s_ceiling, strategy_ceilings = _strategy_calibration(card, evidence, gaps)
    a_ceiling, action_ceilings = _action_calibration(card, evidence, gaps)
    ceilings = {"O": o_ceiling, "S": s_ceiling, "A": a_ceiling}

    approval = card["governance"]["human_approval"]
    approval_valid = bool(
        approval.get("approved")
        and approval.get("approval_ref")
        and evidence.trusted([approval["approval_ref"]], kind="approval")
        and card["governance"]["boundary"] == "production"
    )
    calibration = {}
    for axis in ("O", "S", "A"):
        declared = card["calibration"][axis]
        supported = RANKS[axis][declared] <= RANKS[axis][ceilings[axis]]
        effective = declared if (
            declared != "unassessed"
            and supported
            and approval_valid
            and information_engine["input"]["verified"]
        ) else "unassessed"
        calibration[axis] = {
            "declared": declared,
            "supported_ceiling": ceilings[axis],
            "promotion_eligible": (
                supported
                and ceilings[axis] != "unassessed"
                and information_engine["input"]["verified"]
            ),
            "effective": effective,
        }

    result = {
        "contract": CONTRACT_ID,
        "engine": {
            "id": ENGINE_ID,
            "version": ENGINE_VERSION,
            "contract_sha256": contract_sha256(),
        },
        "card_id": card["card_id"],
        "information_engine": information_engine,
        "calibration": calibration,
        "strategy_ceilings": strategy_ceilings,
        "action_ceilings": action_ceilings,
        "gold": False,
        "maturity_floor": None,
        "valid": False,
        "errors": [],
        "gaps": list(dict.fromkeys(gaps)),
        "failed_experiments_preserved": sum(
            row["status"] in {"failed", "inconclusive"}
            for strategy in card["strategies"] for row in strategy["experiments"]
        ),
    }
    result["errors"] = _semantic_errors(card, result)
    result["valid"] = not result["errors"]

    effective = {axis: calibration[axis]["effective"] for axis in ("O", "S", "A")}
    if all(value != "unassessed" for value in effective.values()):
        result["maturity_floor"] = min(RANKS[axis][effective[axis]] for axis in ("O", "S", "A"))

    referenced = _information_refs(card)
    referenced.update(card["objective"]["evidence_refs"])
    for strategy in card["strategies"]:
        for experiment in strategy["experiments"]:
            referenced.update(experiment["receipt_refs"])
    for action in card["actions"]:
        referenced.update(action["run_receipt_refs"])
        referenced.update(action["feedback_receipt_refs"])
        if action["changed_rule_receipt_ref"]:
            referenced.add(action["changed_rule_receipt_ref"])
    if approval.get("approval_ref"):
        referenced.add(approval["approval_ref"])
    evidence_clean = bool(referenced) and evidence.trusted(referenced)
    result["gold"] = bool(
        result["valid"]
        and effective == {"O": "L5", "S": "S", "A": "A3"}
        and information_engine["verified"]
        and evidence_clean
    )
    return result


def validate_card(card: dict[str, Any], *, semantic: bool = True) -> dict[str, Any]:
    """Validate a card and return its evaluation; raise on hard violations."""
    result = evaluate_card(card)
    if semantic and result["errors"]:
        raise CardValidationError(result["errors"])
    return result
