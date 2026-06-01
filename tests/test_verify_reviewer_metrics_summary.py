from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "verify-reviewer-metrics-summary.py"
SUMMARY_PATH = ROOT / "proof" / "records" / "reviewer-metrics-pipeline-v1-summary.json"

spec = importlib.util.spec_from_file_location("verify_reviewer_metrics_summary", SCRIPT_PATH)
verifier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verifier)


class ReviewerMetricsSummaryTests(unittest.TestCase):
    def write_summary_source_fixtures(self, root: Path, summary: dict) -> Path:
        summary_path = root / "proof" / "records" / "reviewer-metrics-pipeline-v1-summary.json"
        summary_path.parent.mkdir(parents=True)
        summary_path.write_text(json.dumps(summary), encoding="utf-8")

        platform_path = root / summary["source_artifacts"]["platform_metrics_state"]
        platform_path.parent.mkdir(parents=True)
        platform_path.write_text(
            json.dumps(
                {
                    "metrics": dict(summary["metrics"]),
                    "proof_ceiling": "SCHEMA_CONTRACT_VERIFIER_EXISTS_ONLY",
                    "public_safe_status": "NOT_PUBLIC_SAFE",
                }
            ),
            encoding="utf-8",
        )

        receipt_path = root / summary["source_artifacts"]["github_control_receipts"]
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(
            "#8 standing control\n#10 blocked claims\nProject #2\nREPORT_ONLY not proof\n",
            encoding="utf-8",
        )
        return summary_path

    def test_summary_exposes_big_number_without_promoting_case_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
            summary["source_artifacts"]["platform_metrics_state"] = "sources/platform-state.json"
            summary["source_artifacts"]["github_control_receipts"] = "sources/github/receipts.md"
            summary_path = self.write_summary_source_fixtures(root, summary)

            result = verifier.verify_summary(summary_path, root)

            metrics = result["metrics"]
            self.assertEqual(metrics["lifetime_governed_cases"], 4)
            self.assertEqual(metrics["detection_activity_count"], 49)
            self.assertEqual(metrics["validation_case_count"], 106)
            self.assertEqual(metrics["proof_record_count"], 8)
            self.assertGreater(metrics["detection_activity_count"], metrics["lifetime_governed_cases"])
            self.assertEqual(result["public_safe_status"], "NOT_PUBLIC_SAFE")

    def test_summary_metrics_match_platform_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
            summary["source_artifacts"]["platform_metrics_state"] = "sources/platform-state.json"
            summary["source_artifacts"]["github_control_receipts"] = "sources/github/receipts.md"
            summary_path = self.write_summary_source_fixtures(root, summary)

            platform_metrics = verifier.platform_metrics_from_summary(summary_path, root)

            self.assertEqual(set(platform_metrics), set(summary["metrics"]))
            for key, expected in platform_metrics.items():
                self.assertEqual(summary["metrics"][key], expected)

    def test_summary_fails_when_platform_state_omits_summarized_metric(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
            summary["source_artifacts"]["platform_metrics_state"] = "sources/platform-state.json"
            summary["source_artifacts"]["github_control_receipts"] = "sources/github/receipts.md"
            summary_path = self.write_summary_source_fixtures(root, summary)
            platform_path = root / summary["source_artifacts"]["platform_metrics_state"]
            platform_state = json.loads(platform_path.read_text(encoding="utf-8"))
            del platform_state["metrics"]["validation_case_count"]
            platform_path.write_text(json.dumps(platform_state), encoding="utf-8")

            with self.assertRaisesRegex(verifier.VerificationError, "platform metrics missing summarized keys"):
                verifier.verify_summary(summary_path, root)

    def test_project_reconciliation_is_backed_by_github_receipt_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
            summary["source_artifacts"]["platform_metrics_state"] = "sources/platform-state.json"
            summary["source_artifacts"]["github_control_receipts"] = "sources/github/receipts.md"
            summary_path = self.write_summary_source_fixtures(root, summary)

            reconciliation = verifier.project_reconciliation_from_summary(summary_path, root)

            self.assertTrue(reconciliation["standing_issue_8_present"])
            self.assertTrue(reconciliation["standing_issue_10_present"])
            self.assertTrue(reconciliation["project_2_route_present"])
            self.assertTrue(reconciliation["report_only_boundary_present"])
            self.assertFalse(reconciliation["project_metadata_is_proof_authority"])
            self.assertFalse(reconciliation["github_project_mutation_performed"])

    def test_summary_blocks_website_or_project_board_proof_authority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
            data["source_artifacts"]["platform_metrics_state"] = "sources/platform-state.json"
            data["source_artifacts"]["github_control_receipts"] = "sources/github/receipts.md"
            data["authority_boundaries"]["website_is_proof_authority"] = True
            path = self.write_summary_source_fixtures(root, data)

            with self.assertRaisesRegex(verifier.VerificationError, "website must remain render-only"):
                verifier.verify_summary(path, root)


if __name__ == "__main__":
    unittest.main()
