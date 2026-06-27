from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "verify-proofcard-backfill-v0.py"
REPORT_PATH = ROOT / "proof" / "reports" / "hoxline-proofcard-backfill-v0.json"
INDEX_PATH = ROOT / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml"

spec = importlib.util.spec_from_file_location("verify_proofcard_backfill_v0", SCRIPT_PATH)
verifier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verifier)


class ProofCardBackfillV0Tests(unittest.TestCase):
    def test_valid_backfill_passes(self) -> None:
        result = verifier.verify_backfill(ROOT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["created_proofcards_count"], 8)
        self.assertIn("HO-DET-011", result["verified_proofcards"])

    def test_report_created_count_matches_cards(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(report["counts_before_after"]["proofcards_created"], len(report["created_proofcards"]))

    def test_counts_do_not_create_promoted_status(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        counts = report["counts_before_after"]
        for field in verifier.ZERO_COUNT_FIELDS:
            self.assertEqual(counts[field], 0, field)

    def test_boundary_flags_are_false(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        for field in verifier.FALSE_BOUNDARY_FIELDS:
            self.assertIs(report["boundary"][field], False, field)

    def test_index_entries_point_to_created_cards(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        index = yaml.safe_load(INDEX_PATH.read_text(encoding="utf-8"))
        by_id = {entry["detection_id"]: entry for entry in index["entries"]}
        for card in report["created_proofcards"]:
            entry = by_id[card["case_id"]]
            self.assertEqual(entry["proof_record_path"], card["proof_record_path"])
            self.assertEqual(entry["proof_card_path"], card["proof_card_path"])
            self.assertEqual(entry["proof_ceiling"], card["proof_ceiling"])
            self.assertEqual(entry["public_safe_status"], "NOT_PUBLIC_SAFE")

    def test_card_missing_required_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self.copy_backfill_tree(tmp_root)
            card_path = tmp_root / "proof" / "cards" / "HO-DET-009.md"
            text = card_path.read_text(encoding="utf-8")
            card_path.write_text(text.replace("## 8. Non-Proof Surfaces\n\n", ""), encoding="utf-8")
            with self.assertRaises(verifier.VerificationError) as caught:
                verifier.verify_backfill(tmp_root)
            self.assertIn("missing section", str(caught.exception))

    def test_report_public_safe_creation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self.copy_backfill_tree(tmp_root)
            report_path = tmp_root / "proof" / "reports" / REPORT_PATH.name
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["counts_before_after"]["public_safe_cases_created"] = 1
            report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
            with self.assertRaises(verifier.VerificationError) as caught:
                verifier.verify_backfill(tmp_root)
            self.assertIn("public_safe_cases_created must be 0", str(caught.exception))

    def test_card_without_proof_record_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self.copy_backfill_tree(tmp_root)
            record_path = tmp_root / "proof" / "records" / "HO-DET-009.md"
            record_path.unlink()
            with self.assertRaises(verifier.VerificationError) as caught:
                verifier.verify_backfill(tmp_root)
            self.assertIn("proof record does not exist", str(caught.exception))

    def copy_backfill_tree(self, tmp_root: Path) -> None:
        (tmp_root / "proof" / "indexes").mkdir(parents=True)
        (tmp_root / "proof" / "records").mkdir(parents=True)
        (tmp_root / "proof" / "cards").mkdir(parents=True)
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
        for card in report["created_proofcards"]:
            source_record = ROOT / card["proof_record_path"]
            target_record = tmp_root / card["proof_record_path"]
            target_record.write_text(source_record.read_text(encoding="utf-8"), encoding="utf-8")
            source_card = ROOT / card["proof_card_path"]
            target_card = tmp_root / card["proof_card_path"]
            target_card.write_text(source_card.read_text(encoding="utf-8"), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
