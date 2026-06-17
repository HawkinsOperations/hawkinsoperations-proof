from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "verify-ho-det-001-public-safe-candidate-review.py"

spec = importlib.util.spec_from_file_location("verify_ho_det_001_public_safe_candidate_review", SCRIPT_PATH)
verifier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verifier)


class HoDet001PublicSafeCandidateReviewTests(unittest.TestCase):
    def test_current_packet_and_index_pass(self) -> None:
        self.assertEqual(verifier.main(), 0)

    def test_blocked_wording_outside_blocked_section_fails(self) -> None:
        text = verifier.PACKET_PATH.read_text(encoding="utf-8")
        text = text.replace(
            "This packet exists to make the boundary reviewer-readable:",
            "runtime proven\n\nThis packet exists to make the boundary reviewer-readable:",
            1,
        )
        with self.assertRaises(verifier.VerificationError):
            verifier.verify_packet_text(text)


if __name__ == "__main__":
    unittest.main()
