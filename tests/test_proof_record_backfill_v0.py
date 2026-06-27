from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "verify-proof-record-backfill-v0.py"
REPORT_PATH = ROOT / "proof" / "reports" / "hoxline-proof-record-backfill-v0.json"
INDEX_PATH = ROOT / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml"

spec = importlib.util.spec_from_file_location("verify_proof_record_backfill_v0", SCRIPT_PATH)
verifier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verifier)


class ProofRecordBackfillV0Tests(unittest.TestCase):
    def test_valid_backfill_passes(self) -> None:
        result = verifier.verify_backfill(ROOT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["created_records_count"], 7)
        self.assertIn("HO-DET-009", result["verified_records"])

    def test_report_created_count_matches_records(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(report["counts_before_after"]["proof_records_created"], len(report["created_records"]))

    def test_counts_do_not_create_promoted_status(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        counts = report["counts_before_after"]
        for field in verifier.ZERO_COUNT_FIELDS:
            self.assertEqual(counts[field], 0, field)

    def test_boundary_flags_are_false(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        for field in verifier.FALSE_BOUNDARY_FIELDS:
            self.assertIs(report["boundary"][field], False, field)

    def test_index_entries_point_to_created_records(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        index = yaml.safe_load(INDEX_PATH.read_text(encoding="utf-8"))
        by_id = {entry["detection_id"]: entry for entry in index["entries"]}
        for record in report["created_records"]:
            entry = by_id[record["case_id"]]
            self.assertEqual(entry["proof_record_path"], record["proof_record_path"])
            self.assertEqual(entry["proof_ceiling"], "CONTROLLED_TEST_VALIDATED")
            self.assertEqual(entry["public_safe_status"], "NOT_PUBLIC_SAFE")
            self.assertEqual(entry["runtime_status"], "NOT_PROVEN")
            self.assertEqual(entry["signal_status"], "NOT_PROVEN")

    def test_record_missing_required_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self.copy_backfill_tree(tmp_root)
            record_path = tmp_root / "proof" / "records" / "HO-DET-009.md"
            text = record_path.read_text(encoding="utf-8")
            record_path.write_text(text.replace("## 8. Public Proof Truth\n\n", ""), encoding="utf-8")
            with self.assertRaises(verifier.VerificationError) as caught:
                verifier.verify_backfill(tmp_root)
            self.assertIn("missing section", str(caught.exception))

    def test_report_public_safe_creation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self.copy_backfill_tree(tmp_root)
            report_path = tmp_root / "proof" / "reports" / "hoxline-proof-record-backfill-v0.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["counts_before_after"]["public_safe_cases_created"] = 1
            report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
            with self.assertRaises(verifier.VerificationError) as caught:
                verifier.verify_backfill(tmp_root)
            self.assertIn("public_safe_cases_created must be 0", str(caught.exception))

    def copy_backfill_tree(self, tmp_root: Path) -> None:
        (tmp_root / "proof" / "indexes").mkdir(parents=True)
        (tmp_root / "proof" / "records").mkdir(parents=True)
        (tmp_root / "proof" / "reports").mkdir(parents=True)
        (tmp_root / "proof" / "indexes" / INDEX_PATH.name).write_text(
            INDEX_PATH.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        (tmp_root / "proof" / "reports" / REPORT_PATH.name).write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )
        for record in report["created_records"]:
            source = ROOT / record["proof_record_path"]
            target = tmp_root / record["proof_record_path"]
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
