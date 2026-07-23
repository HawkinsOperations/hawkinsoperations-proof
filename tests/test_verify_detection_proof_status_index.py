from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "verify_detection_proof_status_index.py"
INDEX_PATH = ROOT / "proof" / "indexes" / "DETECTION_PROOF_STATUS_INDEX.yml"

spec = importlib.util.spec_from_file_location("verify_detection_proof_status_index", SCRIPT_PATH)
verifier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verifier)


class DetectionProofStatusIndexTests(unittest.TestCase):
    def load_index(self) -> dict:
        return yaml.safe_load(INDEX_PATH.read_text(encoding="utf-8"))

    def write_temp_index(self, data: dict) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "DETECTION_PROOF_STATUS_INDEX.yml"
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return path

    def write_temp_index_text(self, text: str) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "DETECTION_PROOF_STATUS_INDEX.yml"
        path.write_text(text, encoding="utf-8")
        return path

    def assert_verification_fails(self, data: dict, expected: str) -> None:
        path = self.write_temp_index(data)
        with self.assertRaises(verifier.VerificationError) as caught:
            verifier.verify_index(path)
        self.assertIn(expected, str(caught.exception))

    def test_valid_index_passes(self) -> None:
        entries = verifier.verify_index(INDEX_PATH)
        self.assertGreaterEqual(len(entries), 10)

    def test_duplicate_detection_id_fails(self) -> None:
        data = self.load_index()
        duplicate = copy.deepcopy(data["entries"][0])
        data["entries"].append(duplicate)
        self.assert_verification_fails(data, "duplicate detection_id")

    def test_duplicate_yaml_key_fails_closed(self) -> None:
        text = INDEX_PATH.read_text(encoding="utf-8")
        text = text.replace(
            "owner_repo: hawkinsoperations-proof",
            "owner_repo: hawkinsoperations-proof\nowner_repo: attacker-proof",
            1,
        )
        path = self.write_temp_index_text(text)
        with self.assertRaisesRegex(verifier.VerificationError, "duplicate key"):
            verifier.verify_index(path)

    def test_nested_duplicate_yaml_key_fails_closed(self) -> None:
        text = INDEX_PATH.read_text(encoding="utf-8")
        text = text.replace(
            "    public_safe_count: 0",
            "    public_safe_count: 0\n    public_safe_count: 1",
            1,
        )
        path = self.write_temp_index_text(text)
        with self.assertRaisesRegex(verifier.VerificationError, "duplicate key"):
            verifier.verify_index(path)

    def test_missing_required_field_fails(self) -> None:
        data = self.load_index()
        del data["entries"][0]["proof_ceiling"]
        self.assert_verification_fails(data, "missing fields")

    def test_unknown_top_level_and_entry_fields_fail(self) -> None:
        data = self.load_index()
        data["extension"] = {"safe": True}
        self.assert_verification_fails(data, "unknown fields")
        data = self.load_index()
        data["entries"][0]["extension"] = {"safe": True}
        self.assert_verification_fails(data, "unknown fields")

    def test_nested_authority_laundering_fails_before_shape_acceptance(self) -> None:
        data = self.load_index()
        data["entries"][0]["extension"] = {
            "review": [{"ai_disposition_authority": True}],
        }
        self.assert_verification_fails(data, "unauthorized authority value")

    def test_nested_public_safe_and_case_closure_laundering_fail(self) -> None:
        for key, value in (
            ("public_safe", True),
            ("case_closed", True),
            ("proof_status", "PUBLIC_SAFE"),
            ("runtime_status", "RUNTIME_ACTIVE"),
        ):
            data = self.load_index()
            data["entries"][0]["extension"] = {"nested": {key: value}}
            self.assert_verification_fails(data, "unauthorized authority value")

    def test_public_safe_promotion_fails(self) -> None:
        data = self.load_index()
        data["entries"][0]["public_safe_status"] = "PUBLIC_SAFE"
        self.assert_verification_fails(data, "unauthorized authority value")

    def test_runtime_promotion_without_record_fails(self) -> None:
        data = self.load_index()
        for entry in data["entries"]:
            if entry["detection_id"] == "HO-DET-012":
                entry["runtime_status"] = "PRIVATE_RUNTIME_EVIDENCE_CAPTURED"
                break
        self.assert_verification_fails(data, "runtime status mismatch")

    def test_signal_promotion_fails(self) -> None:
        data = self.load_index()
        data["entries"][0]["signal_status"] = "SIGNAL_OBSERVED"
        self.assert_verification_fails(data, "unauthorized authority value")

    def test_missing_proof_record_fails_when_claimed(self) -> None:
        data = self.load_index()
        data["entries"][0]["proof_record_path"] = "proof/records/DOES-NOT-EXIST.md"
        self.assert_verification_fails(data, "points to missing file")

    def test_validation_registry_drift_fails(self) -> None:
        data = self.load_index()
        for entry in data["entries"]:
            if entry["detection_id"] == "AWS-DET-001":
                entry["validation_status"] = "VALIDATION_PLANNED"
                break
        self.assert_verification_fails(data, "validation drift")

    def test_source_matrix_drift_fails(self) -> None:
        data = self.load_index()
        data["entries"][0]["source_status"] = "EXTERNAL_BOUNDARY_CONTRACT"
        self.assert_verification_fails(data, "source_status drift")

    def test_current_counts_are_derived(self) -> None:
        data = self.load_index()
        data["current_authority"]["derived_counts"]["proof_record_count"] = 99
        self.assert_verification_fails(data, "current proof counts drift")

    def test_duplicate_proof_record_path_fails(self) -> None:
        data = self.load_index()
        data["entries"][1]["proof_record_path"] = data["entries"][0]["proof_record_path"]
        data["entries"][1]["proof_ceiling"] = data["entries"][0]["proof_ceiling"]
        self.assert_verification_fails(data, "proof_record_path must map to exactly one case")

    def test_duplicate_proof_card_path_fails(self) -> None:
        data = self.load_index()
        data["entries"][1]["proof_card_path"] = data["entries"][0]["proof_card_path"]
        self.assert_verification_fails(data, "proof_card_path must map to exactly one case")

    def test_duplicate_proof_path_alias_fails(self) -> None:
        entries = {
            "ONE": {"proof_record_path": "proof/records/HO-DET-009.md", "proof_card_path": None, "public_safe_status": "NOT_PUBLIC_SAFE"},
            "TWO": {"proof_record_path": "proof/records/./HO-DET-009.md", "proof_card_path": None, "public_safe_status": "NOT_PUBLIC_SAFE"},
        }
        with self.assertRaisesRegex(verifier.VerificationError, "proof_record_path must map to exactly one case"):
            verifier.derive_current_counts(entries)

    def test_owned_paths_reject_cross_platform_absolute_and_encoded_forms(self) -> None:
        hostile = [
            r"C:\private\HO-DET-009.md",
            r"\\server\share\HO-DET-009.md",
            "/proof/records/HO-DET-009.md",
            r"proof\records/HO-DET-009.md",
            "proof/records/%2e%2e/cards/HO-DET-009.md",
            "proof/records/%252e%252e/cards/HO-DET-009.md",
            "proof/records/./HO-DET-009.md",
        ]
        for value in hostile:
            with self.subTest(value=value):
                with self.assertRaises(verifier.VerificationError):
                    verifier.canonical_owned_path(value, "proof_record_path", "HO-DET-009")

    def test_owned_artifact_rejects_body_only_identity_and_forged_ceiling(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        prior_root = verifier.ROOT
        self.addCleanup(setattr, verifier, "ROOT", prior_root)
        verifier.ROOT = Path(temp_dir.name)
        record_dir = verifier.ROOT / "proof" / "records"
        record_dir.mkdir(parents=True)
        record_path = record_dir / "EX-DET-001.md"
        entry = {"proof_ceiling": "CONTROLLED_TEST_VALIDATED"}
        record_path.write_text(
            "# OTHER-DET-001 Proof Record\ncase_id: EX-DET-001\nproof_ceiling: CONTROLLED_TEST_VALIDATED\npublic_safe_status: NOT_PUBLIC_SAFE\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(verifier.VerificationError, "heading does not exactly identify"):
            verifier.validate_owned_artifact(entry, "proof_record_path", "proof/records/EX-DET-001.md", "EX-DET-001", is_card=False)
        record_path.write_text(
            "# EX-DET-001 Proof Record\ncase_id: EX-DET-001\nproof_ceiling: CONTROLLED_TEST_VALIDATED_FORGED\npublic_safe_status: NOT_PUBLIC_SAFE\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(verifier.VerificationError, "malformed or ambiguous metadata"):
            verifier.validate_owned_artifact(entry, "proof_record_path", "proof/records/EX-DET-001.md", "EX-DET-001", is_card=False)

    def test_owned_artifact_rejects_conflicting_repeated_metadata(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        prior_root = verifier.ROOT
        self.addCleanup(setattr, verifier, "ROOT", prior_root)
        verifier.ROOT = Path(temp_dir.name)
        record_dir = verifier.ROOT / "proof" / "records"
        record_dir.mkdir(parents=True)
        (record_dir / "EX-DET-001.md").write_text(
            "# EX-DET-001 Proof Record\n"
            "detection_id: EX-DET-001\n"
            "detection_id: OTHER-DET-001\n"
            "proof_ceiling: CONTROLLED_TEST_VALIDATED\n"
            "runtime_status: NOT_PROVEN\n"
            "signal_status: NOT_PROVEN\n"
            "public_safe_status: NOT_PUBLIC_SAFE\n",
            encoding="utf-8",
        )
        entry = {
            "proof_ceiling": "CONTROLLED_TEST_VALIDATED",
            "runtime_status": "NOT_PROVEN",
            "signal_status": "NOT_PROVEN",
            "proof_record_path": "proof/records/EX-DET-001.md",
        }
        with self.assertRaisesRegex(verifier.VerificationError, "conflicting repeated metadata"):
            verifier.validate_owned_artifact(
                entry,
                "proof_record_path",
                "proof/records/EX-DET-001.md",
                "EX-DET-001",
                is_card=False,
            )

    def test_owned_artifact_rejects_inline_nested_authority_laundering(self) -> None:
        text = (
            "# EX-DET-001 Proof Record\n"
            "detection_id: EX-DET-001\n"
            "proof_ceiling: CONTROLLED_TEST_VALIDATED\n"
            "runtime_status: NOT_PROVEN\n"
            "signal_status: NOT_PROVEN\n"
            "public_safe_status: NOT_PUBLIC_SAFE\n"
            'extensions: {"review": {"analyst_approved": true}}\n'
        )
        with self.assertRaisesRegex(verifier.VerificationError, "unauthorized authority value"):
            verifier.validate_markdown_authority_metadata(text, "hostile proof record")

    def test_markdown_authority_variants_fail_closed(self) -> None:
        attacks = (
            "- **public_safe_status:** PUBLIC_SAFE",
            "> runtime_status: RUNTIME_ACTIVE",
            "| public_safe_status | PUBLIC_SAFE | extra |",
            "- `final_authorization`: FINAL_AUTHORIZED",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaises(verifier.VerificationError):
                    verifier.validate_markdown_authority_metadata(
                        attack, "hostile proof record"
                    )

    def test_unicode_confusable_authority_keys_fail_closed(self) -> None:
        attacks = (
            {"ｐｕｂｌｉｃ＿ｓａｆｅ": "approved"},
            {"ＡＩ＿ｄｉｓｐｏｓｉｔｉｏｎ＿ａｕｔｈｏｒｉｔｙ": "approved"},
            {"ｒｕｎｔｉｍｅ＿ａｃｔｉｖｅ": True},
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaisesRegex(
                    verifier.VerificationError, "unauthorized authority value"
                ):
                    verifier.validate_recursive_authority_boundaries(
                        attack, "hostile proof record"
                    )

    def test_unicode_confusable_markdown_metadata_fails_closed(self) -> None:
        attacks = (
            "ｐｕｂｌｉｃ＿ｓａｆｅ: approved",
            "ＡＩ＿ｄｉｓｐｏｓｉｔｉｏｎ＿ａｕｔｈｏｒｉｔｙ: approved",
            "ｒｕｎｔｉｍｅ＿ａｃｔｉｖｅ: true",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaises(verifier.VerificationError):
                    verifier.validate_markdown_authority_metadata(
                        attack, "hostile proof record"
                    )

    def test_normalized_authority_key_collision_fails_closed(self) -> None:
        with self.assertRaisesRegex(
            verifier.VerificationError, "normalized key collision"
        ):
            verifier.validate_recursive_authority_boundaries(
                {
                    "public_safe": False,
                    "ｐｕｂｌｉｃ＿ｓａｆｅ": "approved",
                },
                "hostile proof record",
            )

    def test_formatted_conflicting_identity_is_collected(self) -> None:
        text = (
            "case_id: EX-DET-001\n"
            "- **case_id:** OTHER-DET-001\n"
        )
        with self.assertRaisesRegex(
            verifier.VerificationError, "conflicting repeated metadata"
        ):
            verifier.unique_metadata_value(
                text,
                ("case_id",),
                ("Case ID",),
                label="hostile identity",
                required=True,
            )

    def test_affirmative_proof_prose_variants_fail_closed(self) -> None:
        attacks = (
            "customer deployment is active",
            "analyst approval granted",
            "SOCaaS deployment is live",
            "final authorization granted",
            "case closure approved",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaisesRegex(
                    verifier.VerificationError, "affirmative authority claim"
                ):
                    verifier.validate_recursive_authority_boundaries(
                        {"notes": attack}, "proof index"
                    )
                with self.assertRaisesRegex(
                    verifier.VerificationError, "affirmative authority claim"
                ):
                    verifier.validate_markdown_authority_metadata(
                        attack, "hostile proof record"
                    )

    def test_negation_is_clause_local(self) -> None:
        with self.assertRaisesRegex(
            verifier.VerificationError, "affirmative authority claim"
        ):
            verifier.validate_recursive_authority_boundaries(
                {"notes": "not historical; customer deployment is active"},
                "proof index",
            )
        verifier.validate_recursive_authority_boundaries(
            {"notes": "customer deployment is not active"}, "proof index"
        )

    def test_reverse_inventory_rejects_orphans_and_preserves_card_only_case(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        prior_root = verifier.ROOT
        self.addCleanup(setattr, verifier, "ROOT", prior_root)
        verifier.ROOT = Path(temp_dir.name)
        (verifier.ROOT / "proof" / "records").mkdir(parents=True)
        (verifier.ROOT / "proof" / "cards").mkdir(parents=True)
        (verifier.ROOT / "proof" / "records" / "HO-DET-999.md").write_text("# orphan\n", encoding="utf-8")
        (verifier.ROOT / "proof" / "cards" / "HO-NDR-001.md").write_text("# boundary\n", encoding="utf-8")
        entries = {
            "HO-NDR-001": {
                "proof_record_path": None,
                "proof_card_path": "proof/cards/HO-NDR-001.md",
            }
        }
        with self.assertRaisesRegex(verifier.VerificationError, "unindexed case artifacts"):
            verifier.verify_reverse_inventory(entries)
        (verifier.ROOT / "proof" / "records" / "HO-DET-999.md").unlink()
        verifier.verify_reverse_inventory(entries)

    def test_ho_ndr_001_record_promotion_fails(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        prior_root = verifier.ROOT
        self.addCleanup(setattr, verifier, "ROOT", prior_root)
        verifier.ROOT = Path(temp_dir.name)
        (verifier.ROOT / "proof" / "records").mkdir(parents=True)
        (verifier.ROOT / "proof" / "cards").mkdir(parents=True)
        (verifier.ROOT / "proof" / "records" / "HO-NDR-001.md").write_text("# record\n", encoding="utf-8")
        (verifier.ROOT / "proof" / "cards" / "HO-NDR-001.md").write_text("# card\n", encoding="utf-8")
        entries = {
            "HO-NDR-001": {
                "proof_record_path": "proof/records/HO-NDR-001.md",
                "proof_card_path": "proof/cards/HO-NDR-001.md",
            }
        }
        with self.assertRaisesRegex(verifier.VerificationError, "must remain card-only"):
            verifier.verify_reverse_inventory(entries)

    def test_historical_mislabel_fails(self) -> None:
        data = self.load_index()
        data["current_authority"]["historical_snapshot"] = True
        self.assert_verification_fails(data, "historical_snapshot must be false")

    def test_card_ceiling_cannot_exceed_record(self) -> None:
        data = self.load_index()
        data["entries"][1]["proof_ceiling"] = "PRIVATE_RUNTIME_EVIDENCE_CAPTURED"
        self.assert_verification_fails(data, "proof record ceiling mismatch")


if __name__ == "__main__":
    unittest.main()
