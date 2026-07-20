"""Frozen public constants for the OSA v2 contract."""

CONTRACT_ID = "yuanli-osa-card/v2"
ENGINE_ID = "yuanli-osa-scoring-engine"
ENGINE_VERSION = "2.0.0"

O_LEVELS = ("unassessed", "L1", "L2", "L3", "L4", "L5")
S_LEVELS = ("unassessed", "C", "B", "A", "S")
A_LEVELS = ("unassessed", "A0", "A1", "A2", "A3")

EXPERIMENT_STAGES = (
    "technical_feasibility",
    "value_validation",
    "growth_validation",
)

SABC_LABELS = {
    "C": "strategy_idea",
    "B": "technical_feasibility_passed",
    "A": "value_validation_passed",
    "S": "growth_validation_passed",
}

AUTOMATION_LABELS = {
    "A0": "manual_nonstandard",
    "A1": "versioned_sop",
    "A2": "agent_run_with_receipts",
    "A3": "ai_self_driving_with_changed_rule_receipt",
}

RANKS = {
    "O": {level: rank for rank, level in enumerate(O_LEVELS)},
    "S": {level: rank for rank, level in enumerate(S_LEVELS)},
    "A": {level: rank for rank, level in enumerate(A_LEVELS)},
}
