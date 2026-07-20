import copy
import json
import unittest
from pathlib import Path

from yuanli_osa_card import CardValidationError, evaluate_card, migrate_v1
from yuanli_osa_card.engine import contract_sha256, validate_card
from yuanli_osa_card.fixtures import load_golden_fixture


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "xiaoyuan-public-content-experiment.v2.json"


def sample():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def evidence(evidence_id, kind):
    return {
        "evidence_id": evidence_id,
        "kind": kind,
        "source": f"test://{evidence_id}",
        "source_published_at": "2026-07-20T00:00:00Z",
        "observed_at": "2026-07-20T00:01:00Z",
        "sha256": (evidence_id.encode().hex() + "0" * 64)[:64],
        "authenticity": "verified_real",
        "current": True,
        "conflicted": False,
        "privacy": "public",
    }


def experiment(exp_id, stage, metric_kind, cycle=None):
    return {
        "experiment_id": exp_id,
        "stage": stage,
        "hypothesis": f"conformance hypothesis for {exp_id}",
        "metrics": [{
            "metric_id": f"m-{exp_id}",
            "name": f"metric {exp_id}",
            "kind": metric_kind,
            "unit": "count",
            "baseline": 0,
            "target": 1,
        }],
        "threshold": 1,
        "sample": 1,
        "timebox": "one cycle",
        "stop_conditions": ["threshold missed"],
        "status": "passed",
        "result": "passed in conformance test",
        "decision": "promote",
        "receipt_refs": [f"ev-{exp_id}"],
        "reproducible": True,
        "attributable": True,
        "comparable_cycle_id": cycle,
    }


def add_receipt(card, exp):
    card["evidence"]["items"].append(evidence(exp["receipt_refs"][0], "experiment_receipt"))


class OSAContractTest(unittest.TestCase):
    def test_packaged_golden_fixture_has_exact_cross_repository_projection(self):
        result = validate_card(load_golden_fixture())
        self.assertEqual(
            {
                "ceilings": {
                    axis: result["calibration"][axis]["supported_ceiling"]
                    for axis in "OSA"
                },
                "effective": {
                    axis: result["calibration"][axis]["effective"]
                    for axis in "OSA"
                },
                "gaps": result["gaps"],
                "gold": result["gold"],
            },
            {
                "ceilings": {"O": "L1", "S": "C", "A": "A0"},
                "effective": {"O": "unassessed", "S": "unassessed", "A": "unassessed"},
                "gaps": [
                    "O: objective evidence is missing, stale, conflicted, or not verified_real",
                    "S/strategy-conformance: no reproducible technical feasibility receipt",
                ],
                "gold": False,
            },
        )

    def test_public_sample_is_valid_but_has_no_effective_grade(self):
        result = validate_card(sample())
        self.assertTrue(result["valid"])
        self.assertEqual(
            {axis: result["calibration"][axis]["effective"] for axis in "OSA"},
            {"O": "unassessed", "S": "unassessed", "A": "unassessed"},
        )
        self.assertFalse(result["gold"])

    def test_schema_rejects_missing_field_and_wrong_stage(self):
        card = sample()
        del card["objective"]
        with self.assertRaises(CardValidationError):
            evaluate_card(card)
        card = sample()
        card["strategies"][0]["experiments"][0]["stage"] = "prototype_validation"
        with self.assertRaises(CardValidationError):
            evaluate_card(card)

    def test_technical_prototype_can_reach_b_but_not_a_or_s(self):
        card = sample()
        tech = experiment("tech", "technical_feasibility", "technical")
        card["strategies"][0]["experiments"] = [tech]
        add_receipt(card, tech)
        result = evaluate_card(card)
        self.assertEqual(result["calibration"]["S"]["supported_ceiling"], "B")
        card["calibration"]["S"] = "A"
        result = evaluate_card(card)
        self.assertIn("calibration_exceeds_evidence", {row["code"] for row in result["errors"]})

    def test_vanity_metric_cannot_pass_value_gate(self):
        card = sample()
        tech = experiment("tech", "technical_feasibility", "technical")
        vanity = experiment("value-vanity", "value_validation", "vanity")
        card["strategies"][0]["experiments"] = [tech, vanity]
        add_receipt(card, tech)
        add_receipt(card, vanity)
        result = evaluate_card(card)
        self.assertEqual(result["calibration"]["S"]["supported_ceiling"], "B")
        self.assertTrue(any("vanity metrics" in gap for gap in result["gaps"]))

    def test_fewer_than_three_growth_cycles_cannot_reach_s(self):
        card = sample()
        rows = [
            experiment("tech", "technical_feasibility", "technical"),
            experiment("value", "value_validation", "outcome"),
            experiment("growth-1", "growth_validation", "growth", "week-1"),
            experiment("growth-2", "growth_validation", "growth", "week-2"),
        ]
        card["strategies"][0]["experiments"] = rows
        for row in rows:
            add_receipt(card, row)
        result = evaluate_card(card)
        self.assertEqual(result["calibration"]["S"]["supported_ceiling"], "A")

    def test_a3_requires_real_changed_rule_receipt(self):
        card = sample()
        action = card["actions"][0]
        action.update({
            "owner": "test-owner",
            "start_at": "2026-07-20T00:00:00Z",
            "due_at": "2026-07-21T00:00:00Z",
            "measurable_result": "one conformance output",
            "sop_version": "v1",
            "outputs": ["test output"],
            "run_receipt_refs": ["ev-run"],
            "feedback_receipt_refs": ["ev-feedback"],
            "autonomous_planning": True,
            "rollback": "restore test fixture",
        })
        action["human_gate"] = {"required": True, "owner": "human", "conditions": ["review"]}
        card["evidence"]["items"].extend([
            evidence("ev-run", "action_receipt"),
            evidence("ev-feedback", "feedback_receipt"),
        ])
        result = evaluate_card(card)
        self.assertEqual(result["calibration"]["A"]["supported_ceiling"], "A2")
        action["changed_rule_receipt_ref"] = "ev-rule"
        card["evidence"]["items"].append(evidence("ev-rule", "changed_rule"))
        result = evaluate_card(card)
        self.assertEqual(result["calibration"]["A"]["supported_ceiling"], "A3")

    def test_situation_is_context_and_prototype_terms_are_routed(self):
        migrated = migrate_v1({
            "Objective": "test objective",
            "Situation": "market context only",
            "Action": "draft an action",
            "prototype_hypothesis": "原型假设：验证接口和代码能否端到端运行",
        })
        self.assertEqual(migrated["context"]["situation"], "market context only")
        self.assertEqual(migrated["strategies"], [])
        self.assertEqual(migrated["calibration"], {"O": "unassessed", "S": "unassessed", "A": "unassessed"})
        self.assertEqual(migrated["context"]["hypothesis_migrations"][0]["classification"], "technical_feasibility_hypothesis")
        self.assertEqual(migrated["legacy_v1"]["Situation"], "market context only")

        ambiguous = migrate_v1({"prototype_hypothesis": "原型假设尚未说明语义"})
        self.assertEqual(ambiguous["governance"]["migration_state"], "needs_ruling")
        self.assertEqual(ambiguous["context"]["hypothesis_migrations"][0]["classification"], "needs_ruling")

        archetype = migrate_v1({"prototype_hypothesis": "原型假设回答我是谁和原型人格"})
        self.assertEqual(archetype["context"]["hypothesis_migrations"][0]["classification"], "archetype_hypothesis")

    def test_public_card_rejects_private_evidence(self):
        card = sample()
        private = evidence("ev-private", "source")
        private["privacy"] = "confidential"
        card["evidence"]["items"].append(private)
        with self.assertRaises(CardValidationError):
            evaluate_card(card)

    def test_contract_hash_is_stable_and_enforced(self):
        self.assertEqual(len(contract_sha256()), 64)
        card = sample()
        card["governance"]["contract_sha256"] = "f" * 64
        result = evaluate_card(card)
        self.assertIn("contract_hash_mismatch", {row["code"] for row in result["errors"]})

    def test_gold_requires_all_three_top_grades_and_clean_evidence(self):
        card = sample()
        card["governance"]["boundary"] = "production"
        card["governance"]["contract_sha256"] = contract_sha256()
        card["objective"].update({
            "selected_candidate_id": "goal-conversion",
            "goal_model": "test comparison model",
            "baseline": 0,
            "metrics": [{
                "metric_id": "objective-outcome", "name": "verified outcome",
                "kind": "outcome", "unit": "count", "baseline": 0, "target": 1,
            }],
            "target_value": 1,
            "deadline": "2026-08-20T00:00:00Z",
            "evidence_refs": ["ev-objective"],
            "global_optimum_basis": "three candidates compared under constraints",
        })
        rows = [
            experiment("tech", "technical_feasibility", "technical"),
            experiment("value", "value_validation", "outcome"),
            experiment("growth-1", "growth_validation", "growth", "week-1"),
            experiment("growth-2", "growth_validation", "growth", "week-2"),
            experiment("growth-3", "growth_validation", "growth", "week-3"),
        ]
        card["strategies"][0]["experiments"] = rows
        action = card["actions"][0]
        action.update({
            "owner": "test-owner", "start_at": "2026-07-20T00:00:00Z",
            "due_at": "2026-07-21T00:00:00Z", "measurable_result": "one output",
            "sop_version": "v1", "outputs": ["output"],
            "run_receipt_refs": ["ev-run"], "feedback_receipt_refs": ["ev-feedback"],
            "changed_rule_receipt_ref": "ev-rule", "autonomous_planning": True,
            "rollback": "restore fixture",
        })
        action["human_gate"] = {"required": True, "owner": "human", "conditions": ["review"]}
        card["evidence"]["items"] = [
            evidence("ev-objective", "source"),
            evidence("ev-run", "action_receipt"),
            evidence("ev-feedback", "feedback_receipt"),
            evidence("ev-rule", "changed_rule"),
            evidence("ev-approval", "approval"),
        ]
        for row in rows:
            add_receipt(card, row)
        card["calibration"] = {"O": "L5", "S": "S", "A": "A3"}
        card["governance"]["human_approval"] = {
            "approved": True,
            "approval_ref": "ev-approval",
            "approved_by": "test-human",
            "approved_at": "2026-07-20T00:02:00Z",
        }
        result = validate_card(card)
        self.assertTrue(result["gold"])


if __name__ == "__main__":
    unittest.main()
