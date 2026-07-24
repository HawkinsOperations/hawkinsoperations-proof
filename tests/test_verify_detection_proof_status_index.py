from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unicodedata
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


def run_workflow_vocabulary_guard(workflow_path: Path, files: dict[str, bytes]):
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    job = next(iter(workflow["jobs"].values()))
    step = next(
        item
        for item in job["steps"]
        if item.get("name") == "Reject retired fixture vocabulary"
    )
    source = step["run"].split("<<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
        for relative, content in files.items():
            (root / relative).write_bytes(content)
        subprocess.run(["git", "add", "--", *files], cwd=root, check=True)
        return subprocess.run(
            [sys.executable, "-c", source],
            cwd=root,
            capture_output=True,
            text=True,
        )


class DetectionProofStatusIndexTests(unittest.TestCase):
    def test_required_ci_uses_exact_authority_shas_and_rejects_retired_vocabulary(
        self,
    ) -> None:
        workflow_path = ROOT / ".github/workflows/proof-authority-integrity.yml"
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        job = workflow["jobs"]["proof-authority-integrity"]
        env_names = (
            "DETECTIONS_AUTHORITY_SHA",
            "VALIDATION_AUTHORITY_SHA",
            "PLATFORM_FIXTURE_SHA",
        )
        for env_name in env_names:
            self.assertRegex(job["env"][env_name], r"^[0-9a-f]{40}$")
        text = workflow_path.read_text(encoding="utf-8")
        for env_name in env_names:
            self.assertIn(f'rev-parse HEAD)" = "${env_name}"', text)
        self.assertIn('retired = "".join(("syn", "thetic"))', text)
        self.assertIn('unicodedata.normalize("NFKC"', text)
        self.assertIn('["git", "ls-files", "-z"]', text)
        self.assertIn('["git", "show", f":{relative}"]', text)
        self.assertIn("tracked non-binary content contains NUL", text)
        self.assertGreaterEqual(text.count("check=True"), 2)
        self.assertNotIn("git grep", text)
        self.assertNotIn("feature/hoxline-case-growth-convergence-v1", text)

    def test_required_ci_checks_pr_or_push_commit_range_for_whitespace(self) -> None:
        workflow_path = ROOT / ".github/workflows/proof-authority-integrity.yml"
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        steps = workflow["jobs"]["proof-authority-integrity"]["steps"]
        checkout = next(
            step for step in steps if step.get("name") == "Check out proof PR source"
        )
        self.assertEqual(0, checkout["with"]["fetch-depth"])
        self.assertIs(checkout["with"]["persist-credentials"], False)

        whitespace = next(
            step for step in steps if step.get("name") == "Reject whitespace errors"
        )
        source = whitespace["run"]
        self.assertIn("set -euo pipefail", source)
        self.assertIn('git diff --check "$PR_BASE_SHA...$PR_HEAD_SHA"', source)
        self.assertIn('git diff --check "$EVENT_BEFORE_SHA...$EVENT_SHA"', source)
        self.assertIn('git diff --check "$EVENT_SHA^...$EVENT_SHA"', source)
        self.assertIn('git diff-tree --check --root "$EVENT_SHA"', source)

    def test_required_vocabulary_guard_rejects_nfkc_utf16_and_git_errors(self) -> None:
        workflow_path = ROOT / ".github/workflows/proof-authority-integrity.yml"
        retired = "".join(("syn", "thetic"))
        fullwidth = "".join(chr(ord(character) + 0xFEE0) for character in retired)
        self.assertEqual(
            retired,
            unicodedata.normalize("NFKC", fullwidth).casefold(),
        )
        result = run_workflow_vocabulary_guard(
            workflow_path,
            {
                f"fixture-{fullwidth}.txt": b"controlled-test\n",
                "content-fixture.txt": f"{fullwidth}\n".encode(),
                "utf16-fixture.md": f"{retired}\n".encode("utf-16-le"),
            },
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("utf16-fixture.md", result.stderr + result.stdout)
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        step = next(
            item
            for item in next(iter(workflow["jobs"].values()))["steps"]
            if item.get("name") == "Reject retired fixture vocabulary"
        )
        source = step["run"].split("<<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
        with tempfile.TemporaryDirectory() as temp:
            operational = subprocess.run(
                [sys.executable, "-c", source],
                cwd=temp,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(0, operational.returncode)

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

    def test_candidate_review_state_cannot_grant_claim_authority_or_skip_human_review(
        self,
    ) -> None:
        for field, value, expected in (
            (
                "claim_authority",
                "GRANT_STRONGER_RUNTIME_SIGNAL_PUBLIC_SAFE_CLAIMS",
                "claim_authority must remain",
            ),
            (
                "human_review_required",
                False,
                "human_review_required must remain true",
            ),
        ):
            with self.subTest(field=field):
                data = self.load_index()
                entry = next(
                    item
                    for item in data["entries"]
                    if item.get("candidate_review_state") is not None
                )
                entry["candidate_review_state"][field] = value
                self.assert_verification_fails(data, expected)

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
            "deployed to customer",
            "customer deployed",
            "customer environment deployed",
            "production live",
            "analyst approved",
            "analyst approval granted",
            "SOCaaS deployment is live",
            "SOCaaS deployed",
            "final authorization granted",
            "final authorization received",
            "case closure approved",
            "case closure complete",
            "runtime active",
            "signal observed",
            "signal was observed",
            "public safe for release",
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

    def test_nfkc_affirmative_proof_prose_variants_fail_closed(self) -> None:
        attacks = (
            "ｐｒｏｄｕｃｔｉｏｎ ｌｉｖｅ",
            "ａｎａｌｙｓｔ ａｐｐｒｏｖｅｄ",
            "ｆｉｎａｌ ａｕｔｈｏｒｉｚａｔｉｏｎ ｒｅｃｅｉｖｅｄ",
            "ｐｕｂｌｉｃ ｓａｆｅ ｆｏｒ ｒｅｌｅａｓｅ",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaisesRegex(
                    verifier.VerificationError, "affirmative authority claim"
                ):
                    verifier.validate_recursive_authority_boundaries(
                        {"notes": attack}, "proof index"
                    )

    def test_boundary_containers_allow_only_exact_negative_shapes(self) -> None:
        verifier.validate_recursive_authority_boundaries(
            {"claim_boundary": {"blocked_claims": ["production-ready"]}},
            "proof index",
        )
        attacks = (
            "production live",
            "production-ready; customer deployed",
            "final authorization received",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaisesRegex(
                    verifier.VerificationError, "affirmative authority claim"
                ):
                    verifier.validate_recursive_authority_boundaries(
                        {"claim_boundary": {"blocked_claims": [attack]}},
                        "proof index",
                    )
        with self.assertRaisesRegex(
            verifier.VerificationError, "affirmative authority claim"
        ):
            verifier.validate_recursive_authority_boundaries(
                {
                    "claim_boundary": {
                        "blocked_claims": [
                            {"claim": "runtime-active public proof", "detail": "customer deployed"}
                        ]
                    }
                },
                "proof index",
            )

    def test_markdown_blocked_section_cannot_launder_affirmative_prose(self) -> None:
        verifier.validate_markdown_authority_metadata(
            "## Blocked Claims\n\n- production-ready\n- final authorization",
            "bounded proof record",
        )
        attacks = (
            "## Blocked Claims\n\n- production live",
            "## Blocked Claims\n\n- production-ready; customer deployed",
            "## Claim Boundary\n\n| detail | analyst approved |",
            "## Blocked Wording\n\n- public safe for release",
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaisesRegex(
                    verifier.VerificationError, "affirmative authority claim"
                ):
                    verifier.validate_markdown_authority_metadata(
                        attack, "hostile proof record"
                    )

    def test_negation_is_clause_local(self) -> None:
        attacks = (
            "not historical; customer deployment is active",
            "pending documentation, production is live",
            "unsupported note — customer environment deployed",
            "future issue: signal was observed",
            "missing receipt while production is live",
            "no proof currently, customer environment deployed",
            "not approved / production is live",
            "does not prove runtime, customer deployment is active",
            "does not prove runtime, AI authority is enabled",
            "does not prove runtime, analyst approval granted",
            "does not prove runtime, public safe is confirmed",
            "does not prove runtime, final authorization received",
            "does not prove runtime, case closure approved",
            "does not prove runtime and customer deployment is active",
            "not historical customer deployment is active",
            "does not prove runtime plus public safe is confirmed",
            "does not prove runtime though case closure is approved",
            "public\u200b safe is confirmed",
            "case\u200b closure approved",
            "AI\u200b authority is enabled",
            "runtime\u200b is active",
        )
        for attack in attacks:
            with self.subTest(attack=attack), self.assertRaisesRegex(
                verifier.VerificationError, "affirmative authority claim"
            ):
                verifier.validate_recursive_authority_boundaries(
                    {"notes": attack},
                    "proof index",
                )
        verifier.validate_recursive_authority_boundaries(
            {"notes": "customer deployment is not active"}, "proof index"
        )
        for control in (
            (
                "This does not prove runtime-active status, signal-observed "
                "status, production-ready status, public-safe status, "
                "AI-approved status, analyst-approved status, final "
                "authorization, or case closure."
            ),
            (
                "This does not prove customer deployment, public-safe status, "
                "final authorization, or case closure."
            ),
            (
                "Runtime, signal, public-safe, live IdP, production identity "
                "coverage, autonomous SOC, AI-approved disposition, and "
                "analyst-approved disposition claims remain blocked."
            ),
            "Café résumé – reviewer note.",
        ):
            with self.subTest(control=control):
                verifier.validate_recursive_authority_boundaries(
                    {"notes": control}, "proof index"
                )

    def test_combining_mark_obfuscation_in_nested_shapes_fails_closed(self) -> None:
        templates = (
            "public\\u{code} safe is confirmed",
            "case\\u{code} closure approved",
            "runtime\\u{code} is active",
            "AI\\u{code} authority is enabled",
        )
        for code in ("034f", "0301", "fe0f", "0000", "0008", "001f", "007f"):
            for template in templates:
                value = json.loads(
                    '{"extensions":[{"notes":[{"deep":"'
                    + template.format(code=code)
                    + '"}]}]}'
                )
                with self.subTest(code=code, template=template):
                    with self.assertRaisesRegex(
                        verifier.VerificationError, "affirmative authority claim"
                    ):
                        verifier.validate_recursive_authority_boundaries(
                            value, "proof index"
                        )

        verifier.validate_recursive_authority_boundaries(
            {
                "extensions": [
                    {
                        "notes": [
                            "Café résumé – reviewer note.",
                            {"deep": "Reviewer 👩‍💻️ note."},
                            {"multiline": "Reviewer note.\n\tStill bounded."},
                        ]
                    }
                ]
            },
            "proof index",
        )

    def test_connector_independent_and_trailing_negation_attacks_fail(self) -> None:
        connectors = (
            ",", "and", "plus", "though", "because", "therefore",
            "meanwhile", "furthermore", "also", "nevertheless",
            "nonetheless", "except", "despite that", "in fact", "so",
            "consequently", "moreover", "then", "still", "even though",
        )
        attacks = [
            (
                f"does not prove runtime{connector} customer deployment is active"
                if connector == ","
                else f"does not prove runtime {connector} customer deployment is active"
            )
            for connector in connectors
        ]
        attacks.extend(
            (
                "customer deployment is active and not a typo",
                "runtime is active and not simulated",
                "final authorization received and no objections",
                "AI authority is enabled and not revoked",
                "public safe is confirmed and not disputed",
                "case closure approved and not provisional",
                "production is ready and not delayed",
                "signal is observed and not inferred",
                "customer deployment is active without ambiguity",
            )
        )
        for attack in attacks:
            with self.subTest(attack=attack):
                with self.assertRaisesRegex(
                    verifier.VerificationError, "affirmative authority claim"
                ):
                    verifier.validate_recursive_authority_boundaries(
                        {"notes": attack}, "proof index"
                    )

    def test_compositional_promotion_keys_fail_closed(self) -> None:
        attacks = (
            ("production_active", True),
            ("production_live", {"enabled": True}),
            ("customer_deployment", True),
            ("socaas_deployment", True),
            ("runtime_status", "active"),
            ("signal_status", "observed"),
            ("approval_status", "approved"),
            ("closure_status", "closed"),
            ("case_status", "closed"),
            ("public_safe_runtime", True),
            ("final_authorized", True),
            ("%70roduction_active", True),
        )
        for key, value in attacks:
            with self.subTest(key=key), self.assertRaisesRegex(
                verifier.VerificationError, "authority"
            ):
                verifier.validate_recursive_authority_boundaries(
                    {"metadata": {key: value}},
                    "proof index",
                )

    def test_split_and_direct_authority_state_paths_fail_closed(self) -> None:
        attacks = (
            {"runtime": {"state": True}},
            {"signal": {"observed": True}},
            {"public": {"safe": True}},
            {"approval": {"status": True}},
            {"production": {"active": True}},
            {"customer": {"deployed": True}},
            {"socaas": {"deployed": True}},
            {"ai": {"authority": True}},
            {"analyst": {"approval": True}},
            {"review": {"disposition": "APPROVED"}},
            {"final": {"authorization": True}},
            {"case": {"closed": True}},
            {"extensions": [{"final": {"authorization": True}}]},
            {"runtime": {"metadata": {"state": True}}},
            {"final": {"review": {"authorization": True}}},
            {"ai": {"metadata": {"authority": True}}},
            {"customer": {"review": {"deployed": True}}},
            {"review": {"metadata": {"disposition": "APPROVED"}}},
            {"production_live": {"enabled": True}},
            {"ai_authority": {"enabled": True}},
            {"review_disposition": {"approved": True}},
            {"final_authorization": {"granted": True}},
            {"production_live": [True]},
            {"ai_authority": ["APPROVED"]},
            {"review_disposition": [True]},
            {"final_authorization": [1]},
            {"runtime": {"metadata": {"state": [True]}}},
            {"runtime_state": True},
            {"approval_state": True},
            {"production_state": True},
            {"customer_state": True},
            {"socaas_state": True},
            {"final_authority": True},
            {"case_state": True},
        )
        for attack in attacks:
            with self.subTest(attack=attack), self.assertRaisesRegex(
                verifier.VerificationError,
                "authority",
            ):
                verifier.validate_recursive_authority_boundaries(attack, "probe")

    def test_split_and_direct_authority_state_bounded_controls_pass(self) -> None:
        controls = (
            {"runtime": {"state": False}},
            {"signal": {"observed": False}},
            {"public": {"safe": "NOT_PUBLIC_SAFE"}},
            {"approval": {"status": "NOT_APPROVED"}},
            {"production": {"active": "BLOCKED"}},
            {"customer": {"deployed": False}},
            {"socaas": {"deployed": False}},
            {"ai": {"authority": False}},
            {"analyst": {"approval": "NOT_APPROVED"}},
            {"review": {"disposition": "NOT_APPROVED"}},
            {"final": {"authorization": "BLOCKED"}},
            {"case": {"closed": False}},
            {"extensions": [{"final": {"authorization": "BLOCKED"}}]},
            {"runtime_state": False},
            {"approval_state": "NOT_APPROVED"},
            {"production_state": "BLOCKED"},
            {"customer_state": False},
            {"socaas_state": False},
            {"final_authority": False},
            {"case_state": False},
            {"production_live": {"enabled": False}},
            {"ai_authority": {"enabled": False}},
            {"review_disposition": {"approved": "NOT_APPROVED"}},
            {"final_authorization": {"granted": "BLOCKED"}},
            {"production_live": [False]},
            {"ai_authority": ["BLOCKED"]},
            {"review_disposition": ["NOT_APPROVED"]},
            {"final_authorization": ["BLOCKED"]},
            {"runtime": {"metadata": {"state": [False]}}},
        )
        for control in controls:
            with self.subTest(control=control):
                verifier.validate_recursive_authority_boundaries(control, "probe")

    def test_compound_owned_context_names_remain_bounded(self) -> None:
        verifier.validate_recursive_authority_boundaries(
            {
                "runtime_truth_spine": {
                    "runtime_truth": {
                        "state": "RUNTIME_EVIDENCE_VERIFIED_PRIVATE"
                    },
                    "runtime_status": "PRIVATE_RUNTIME_BOUNDARY_CONTEXT_ONLY",
                }
            },
            "proof index",
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

    def test_reverse_inventory_rejects_aliased_artifact_from_internal_identity(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        prior_root = verifier.ROOT
        self.addCleanup(setattr, verifier, "ROOT", prior_root)
        verifier.ROOT = Path(temp_dir.name)
        record_dir = verifier.ROOT / "proof" / "records"
        card_dir = verifier.ROOT / "proof" / "cards"
        record_dir.mkdir(parents=True)
        card_dir.mkdir(parents=True)
        record_body = (
            "# HO-DET-009 Proof Record\n"
            "detection_id: HO-DET-009\n"
            "proof_ceiling: CONTROLLED_TEST_VALIDATED\n"
            "runtime_status: NOT_PROVEN\n"
            "signal_status: NOT_PROVEN\n"
            "public_safe_status: NOT_PUBLIC_SAFE\n"
        )
        (record_dir / "HO-DET-009.md").write_text(record_body, encoding="utf-8")
        aliased_body = record_body.replace(
            "# HO-DET-009 Proof Record", "# Controlled Review Copy"
        )
        (record_dir / "HO-DET-009-copy.md").write_text(aliased_body, encoding="utf-8")
        (card_dir / "HO-NDR-001.md").write_text(
            "# HO-NDR-001 ProofCard\ncase_id: HO-NDR-001\n",
            encoding="utf-8",
        )
        entries = {
            "HO-DET-009": {
                "proof_record_path": "proof/records/HO-DET-009.md",
                "proof_card_path": None,
            },
            "HO-NDR-001": {
                "proof_record_path": None,
                "proof_card_path": "proof/cards/HO-NDR-001.md",
            },
        }
        with self.assertRaisesRegex(
            verifier.VerificationError, "owned by multiple files"
        ):
            verifier.verify_reverse_inventory(entries)

    def test_reverse_inventory_scans_aliased_artifact_before_exclusion(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        prior_root = verifier.ROOT
        self.addCleanup(setattr, verifier, "ROOT", prior_root)
        verifier.ROOT = Path(temp_dir.name)
        record_dir = verifier.ROOT / "proof" / "records"
        card_dir = verifier.ROOT / "proof" / "cards"
        record_dir.mkdir(parents=True)
        card_dir.mkdir(parents=True)
        (record_dir / "HO-DET-009-copy.md").write_text(
            "# HO-DET-009 Proof Record\n"
            "detection_id: HO-DET-009\n"
            "notes: analyst approved\n",
            encoding="utf-8",
        )
        (card_dir / "HO-NDR-001.md").write_text(
            "# HO-NDR-001 ProofCard\ncase_id: HO-NDR-001\n",
            encoding="utf-8",
        )
        entries = {
            "HO-NDR-001": {
                "proof_record_path": None,
                "proof_card_path": "proof/cards/HO-NDR-001.md",
            }
        }
        with self.assertRaisesRegex(
            verifier.VerificationError, "affirmative authority claim"
        ):
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
