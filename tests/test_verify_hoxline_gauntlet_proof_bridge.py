from __future__ import annotations

import copy
import importlib.util
import unittest


SPEC = importlib.util.spec_from_file_location(
    "verify_hoxline_gauntlet_proof_bridge",
    __import__("pathlib").Path(__file__).resolve().parents[1]
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


if __name__ == "__main__":
    unittest.main()
