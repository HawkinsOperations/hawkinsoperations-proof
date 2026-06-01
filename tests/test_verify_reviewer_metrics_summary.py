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
    def test_summary_exposes_big_number_without_promoting_case_count(self) -> None:
        result = verifier.verify_summary(SUMMARY_PATH, ROOT)

        metrics = result["metrics"]
        self.assertEqual(metrics["lifetime_governed_cases"], 4)
        self.assertEqual(metrics["detection_activity_count"], 49)
        self.assertEqual(metrics["validation_case_count"], 106)
        self.assertEqual(metrics["proof_record_count"], 8)
        self.assertGreater(metrics["detection_activity_count"], metrics["lifetime_governed_cases"])
        self.assertEqual(result["public_safe_status"], "NOT_PUBLIC_SAFE")

    def test_summary_metrics_match_platform_state(self) -> None:
        platform_metrics = verifier.platform_metrics_from_summary(SUMMARY_PATH, ROOT)
        summary_metrics = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))["metrics"]

        for key, expected in platform_metrics.items():
            self.assertEqual(summary_metrics[key], expected)

    def test_summary_blocks_website_or_project_board_proof_authority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "summary.json"
            data = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
            data["authority_boundaries"]["website_is_proof_authority"] = True
            path.write_text(json.dumps(data), encoding="utf-8")

            with self.assertRaisesRegex(verifier.VerificationError, "website must remain render-only"):
                verifier.verify_summary(path, ROOT)


if __name__ == "__main__":
    unittest.main()
