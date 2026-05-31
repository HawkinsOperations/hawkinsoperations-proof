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

    def test_missing_required_field_fails(self) -> None:
        data = self.load_index()
        del data["entries"][0]["proof_ceiling"]
        self.assert_verification_fails(data, "entry missing fields")

    def test_public_safe_promotion_fails(self) -> None:
        data = self.load_index()
        data["entries"][0]["public_safe_status"] = "PUBLIC_SAFE"
        self.assert_verification_fails(data, "public_safe_status must be NOT_PUBLIC_SAFE")

    def test_runtime_promotion_without_record_fails(self) -> None:
        data = self.load_index()
        for entry in data["entries"]:
            if entry["detection_id"] == "HO-DET-012":
                entry["runtime_status"] = "PRIVATE_RUNTIME_EVIDENCE_CAPTURED"
                break
        self.assert_verification_fails(data, "HO-DET-012 proof record does not support runtime_status")

    def test_signal_promotion_fails(self) -> None:
        data = self.load_index()
        data["entries"][0]["signal_status"] = "SIGNAL_OBSERVED"
        self.assert_verification_fails(data, "unsupported signal_status")

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


if __name__ == "__main__":
    unittest.main()
