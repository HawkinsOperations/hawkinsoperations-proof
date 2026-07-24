from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "verify_proof_integrity.py"

spec = importlib.util.spec_from_file_location("verify_proof_integrity", SCRIPT_PATH)
verifier = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verifier)


class ProofIntegrityStructuredParsingTests(unittest.TestCase):
    def write_json(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "record.json"
        path.write_text(text, encoding="utf-8")
        return path

    def test_duplicate_json_key_fails_closed(self) -> None:
        path = self.write_json('{"proof_id":"safe","proof_id":"forged"}')
        with patch.object(verifier, "fail", side_effect=RuntimeError) as fail:
            with self.assertRaises(RuntimeError):
                verifier.load_json(path, "hostile record")
        self.assertIn("duplicate JSON key", fail.call_args.args[0])

    def test_non_object_json_fails_closed(self) -> None:
        path = self.write_json('["not", "a", "record"]')
        with patch.object(verifier, "fail", side_effect=RuntimeError) as fail:
            with self.assertRaises(RuntimeError):
                verifier.load_json(path, "hostile record")
        self.assertIn("top-level JSON object", fail.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
