from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "verify_hoxline_gauntlet_proof_bridge",
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "verify-hoxline-gauntlet-proof-bridge.py",
)
assert SPEC and SPEC.loader
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


class HoxlineGauntletProofBridgeTests(unittest.TestCase):
    def good_bridge(self) -> dict:
        return verifier.load_bridge()

    def good_map(self) -> dict:
        return verifier.load_map()

    def test_current_bridge_passes(self) -> None:
        result = verifier.validate_bridge(self.good_bridge(), self.good_map())
        self.assertEqual(result["detection_id"], "HO-DET-001")
        self.assertEqual(result["primary_v1_run_path"], verifier.EXPECTED_V1_RUN)
        self.assertEqual(result["source_manifest_path"], verifier.EXPECTED_MANIFEST)
        self.assertFalse(result["public_safe"])
        self.assertTrue(result["human_review_required"])

    def test_public_safe_true_fails(self) -> None:
        data = copy.deepcopy(self.good_bridge())
        data["public_safe"] = True
        with self.assertRaisesRegex(verifier.VerificationError, "public_safe"):
            verifier.validate_bridge(data, self.good_map())

    def test_missing_validation_reference_fails(self) -> None:
        data = copy.deepcopy(self.good_bridge())
        data["validation_bridge_reference"] = {}
        with self.assertRaisesRegex(verifier.VerificationError, "validation bridge reference"):
            verifier.validate_bridge(data, self.good_map())

    def test_website_as_authority_fails(self) -> None:
        data = copy.deepcopy(self.good_bridge())
        data["website_rendering_boundary"]["website_is_proof_authority"] = True
        with self.assertRaisesRegex(verifier.VerificationError, "website"):
            verifier.validate_bridge(data, self.good_map())

    def test_missing_primary_v1_path_fails(self) -> None:
        data = copy.deepcopy(self.good_bridge())
        data["source_paths"]["hoxline_gauntlet_run_v1"] = verifier.EXPECTED_V0_RUN
        with self.assertRaisesRegex(verifier.VerificationError, "hoxline_gauntlet_run_v1"):
            verifier.validate_bridge(data, self.good_map())

    def test_v0_must_be_compatibility_only(self) -> None:
        data = copy.deepcopy(self.good_bridge())
        data["source_paths"]["compatibility_v0_paths"]["compatibility_role"] = "primary"
        with self.assertRaisesRegex(verifier.VerificationError, "compatibility-only"):
            verifier.validate_bridge(data, self.good_map())

    def test_source_manifest_path_is_required(self) -> None:
        data = copy.deepcopy(self.good_bridge())
        data["source_paths"]["source_manifest_path"] = "examples/gauntlet/missing.json"
        with self.assertRaisesRegex(verifier.VerificationError, "source manifest"):
            verifier.validate_bridge(data, self.good_map())

    def test_hoxline_root_checks_file_existence(self) -> None:
        data = self.good_bridge()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel_path in verifier.REQUIRED_HOXLINE_FILES:
                target = root / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}\n", encoding="utf-8")
            result = verifier.validate_bridge(data, self.good_map(), hoxline_root=root)
            self.assertEqual(result["primary_v1_schema_path"], verifier.EXPECTED_V1_SCHEMA)

    def test_hoxline_root_missing_file_fails(self) -> None:
        data = self.good_bridge()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(verifier.VerificationError, "referenced file missing"):
                verifier.validate_bridge(data, self.good_map(), hoxline_root=Path(tmp))

    def test_stale_work_path_fails_without_literal_fixture(self) -> None:
        data = copy.deepcopy(self.good_bridge())
        data["reviewer_commands"].append("C:" + "\\Raylee\\Work\\bad.md")
        with self.assertRaisesRegex(verifier.VerificationError, "Work"):
            verifier.validate_bridge(data, self.good_map())

    def test_map_primary_v1_path_must_agree(self) -> None:
        proof_map = copy.deepcopy(self.good_map())
        proof_map["hoxline_primary_v1_run_path"] = "HawkinsOperations/hoxline/" + verifier.EXPECTED_V0_RUN
        with self.assertRaisesRegex(verifier.VerificationError, "proof map primary v1 run"):
            verifier.validate_bridge(self.good_bridge(), proof_map)


if __name__ == "__main__":
    unittest.main()
